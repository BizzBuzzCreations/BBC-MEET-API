from rest_framework import serializers
from meet.models import Meeting, MeetingPhoto

class MeetingPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingPhoto
        fields = '__all__'

class MeetingSerializer(serializers.ModelSerializer):
    photos = MeetingPhotoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Meeting
        fields = '__all__'