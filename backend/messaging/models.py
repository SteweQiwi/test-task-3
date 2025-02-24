from django.db import models
from django.contrib.auth import get_user_model
from model_utils.models import TimeStampedModel


User = get_user_model()

class Thread(TimeStampedModel):
    participant1 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="thread_participant1"
    )
    participant2 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="thread_participant2"
    )


class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE) # or we can SET_Null for example
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
