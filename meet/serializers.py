from rest_framework import serializers
from meet.models import Meeting, MeetingPhoto
from account.serializers import UserSerializer

class MeetingPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingPhoto
        fields = '__all__'

class MeetingSerializer(serializers.ModelSerializer):
    photos = MeetingPhotoSerializer(many=True, read_only=True)
    next_status = serializers.SerializerMethodField()
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Meeting
        fields = ['photos', 'uid', 'created_at', 'updated_at', 'title', 'description', 'location', 'meeting_type', 'start_time', 'duration_minutes', 'status', 'next_status', 'created_by','recipient_emails']
    
    def get_next_status(self, obj):
        from meet.choices import VALID_STATUS_CHANGE
        print(obj.status)
        return VALID_STATUS_CHANGE.get(obj.status, None)