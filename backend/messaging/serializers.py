from rest_framework.fields import IntegerField, ListField
from rest_framework.serializers import ModelSerializer, Serializer

from messaging.models import Message, Thread


class ListOfIdSerializer(Serializer):
    ids = ListField(child=IntegerField())


class ThreadSerializer(ModelSerializer):
    class Meta:
        model = Thread
        fields = ['id', 'participant1', 'participant2', 'created', 'modified']
        read_only_fields = ['participant1', 'created', 'modified']


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "sender", "text", "created", "is_read"]
        read_only_fields = ["sender", "created", "is_read"]
