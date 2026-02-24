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

    def create(self, validated_data, user):
        meeting = Meeting.objects.create(**validated_data, created_by=user)
        return meeting

    def get_next_status(self, obj):
        from meet.choices import VALID_STATUS_CHANGE
        return VALID_STATUS_CHANGE.get(obj.status, None)

class MeetingCreatSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=100)
    location = serializers.CharField(max_length=100)
    start_time = serializers.DateTimeField()
    duration_minutes = serializers.IntegerField()
    meeting_type = serializers.CharField(max_length=100)
    recipient_emails = serializers.ListField(child=serializers.EmailField())

    def validate(self, attrs):
        from django.utils import timezone
        if attrs['start_time'] < timezone.now():
            raise serializers.ValidationError("Start time cannot be in the past")
        if len(attrs['recipient_emails']) == 0:
            raise serializers.ValidationError("Recipient emails cannot be empty")
        if len(attrs['recipient_emails']) > 10:
            raise serializers.ValidationError("Recipient emails cannot be more than 10")
        return attrs

    def create(self, validated_data, user):
        meeting = Meeting.objects.create(**validated_data, created_by=user)
        return meeting