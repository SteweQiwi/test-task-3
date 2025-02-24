from django.urls import include, path
from rest_framework.routers import DefaultRouter

from messaging.views import AllThreadsUnreadedMessagesCountView, MessageViewSet, ThreadViewSet

router = DefaultRouter()
router.register(r"threads/(?P<thread_id>\d+)/messages", MessageViewSet, basename="messages")
router.register(r"threads", ThreadViewSet, basename="threads")

urlpatterns = [
    path("", include(router.urls)),
    path('unread_messages/count/', AllThreadsUnreadedMessagesCountView.as_view(), name='unread-message-count'),
]
