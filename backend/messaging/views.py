from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from messaging.models import Message, Thread
from messaging.permissions import IsThreadParticipant
from messaging.serializers import ListOfIdSerializer, MessageSerializer, ThreadSerializer


class ThreadViewSet(ModelViewSet):
    serializer_class = ThreadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Thread.objects.filter(Q(participant1=user) | Q(participant2=user))

    def perform_create(self, serializer):
        participant1 = self.request.user
        participant2 = serializer.validated_data["participant2"]

        # Check if the user is trying to create a thread with themselves
        if participant1 == participant2:
            raise ValidationError("You cannot create a thread with yourself.")

        thread, created = Thread.objects.get_or_create(
            participant1=min(participant1, participant2, key=lambda u: u.id),
            participant2=max(participant1, participant2, key=lambda u: u.id),
        )

        return Response(ThreadSerializer(thread).data)


class MessageViewSet(ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsThreadParticipant]
    pagination_class = LimitOffsetPagination

    _thread = None

    def get_thread(self):
        if self._thread is not None:
            return self._thread
        thread_id = self.kwargs.get("thread_id")
        user = self.request.user
        self._thread = Thread.objects.filter(
            Q(participant1=user) | Q(participant2=user), pk=thread_id
        ).first()
        return self._thread

    def get_queryset(self):
        thread = self.get_thread()
        if not thread:
            return Message.objects.none()

        return Message.objects.filter(thread=thread)

    def perform_create(self, serializer):
        thread = self.get_thread()
        if not thread:
            raise NotFound("Thread not found.")
        serializer.save(sender=self.request.user, thread=thread)
        thread.save(update_fields=["modified"])

    @action(detail=False, methods=["post"])
    def bulk_mark_read(self, request, thread_id=None):
        serializer = ListOfIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        message_ids = serializer.validated_data["ids"]

        thread = self.get_thread()
        if not thread:
            return ValidationError("Thread not found.")

        if not message_ids:
            return ValidationError("No message IDs provided.")

        messages_to_update = Message.objects.filter(id__in=message_ids, thread=thread).exclude(sender_id=user.id)

        updated_count = messages_to_update.update(is_read=True)
        return self.list(request)


class AllThreadsUnreadedMessagesCountView(APIView):
    """
    API view to retrieve the count of unread messages for the authenticated user
    across all threads where they are a participant.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        unread_count = Message.objects.filter(
            Q(thread__participant1=user) | Q(thread__participant2=user), is_read=False
        ).exclude(sender_id=user.id).count()

        return Response({"unread_messages": unread_count})
