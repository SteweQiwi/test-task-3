from rest_framework.permissions import BasePermission


class IsThreadParticipant(BasePermission):
    """
    Permission to check if the user is a participant in the thread.
    """

    def has_permission(self, request, view):
        user = request.user
        thread = view.get_thread()
        return thread and user.id in [thread.participant1_id, thread.participant2_id]
