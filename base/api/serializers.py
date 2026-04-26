from rest_framework.serializers import ModelSerializer, SerializerMethodField
from base.models import Room, Message
from rest_framework import serializers

class RoomSerializer(serializers.ModelSerializer):
    topic = serializers.SerializerMethodField()
    class Meta:
        model = Room
        fields = '__all__'
        
    def get_topic(self, topic):
        return topic.topic.name

class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'