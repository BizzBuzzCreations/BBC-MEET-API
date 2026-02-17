from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from meet.models import Meeting
from meet.serializers import MeetingSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.
class MeetingViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'uid'

    def list(self, request):
        """
        List all meetings
        Endpoint: GET /api/meet/
        """
        meetings = Meeting.objects.all()
        serializer = MeetingSerializer(meetings, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Create a new meeting
        Endpoint: POST /api/meet/
        Body: 
        {
            "title": "Meeting Title",
            "description": "Meeting Description",
            "location": "Meeting Location",
            "meeting_type": "Meeting Type",
            "start_time": "Meeting Start Time",
            "duration_minutes": "Meeting Duration",
            "status": "Meeting Status",
            "created_by": "Meeting Created By"
        }
        """
        serializer = MeetingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, uid=None):
        """
        Retrieve a meeting
        Endpoint: GET /api/meet/{uid}/
        """
        meeting = Meeting.objects.get(uid=uid)
        serializer = MeetingSerializer(meeting)
        return Response(serializer.data)
    
    def update(self, request, uid=None):
        """
        Update a meeting
        Endpoint: PUT /api/meet/{uid}/
        Body: 
        {
            "title": "Meeting Title",
            "description": "Meeting Description",
            "location": "Meeting Location",
            "meeting_type": "Meeting Type",
            "start_time": "Meeting Start Time",
            "duration_minutes": "Meeting Duration",
            "status": "Meeting Status",
            "created_by": "Meeting Created By"
        }
        """
        meeting = Meeting.objects.get(uid=uid)
        serializer = MeetingSerializer(meeting, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, uid=None):
        """
        Delete a meeting
        Endpoint: DELETE /api/meet/{uid}/
        """
        meeting = Meeting.objects.get(uid=uid)
        meeting.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'],url_path='generate-otp')
    def generate_otp(self, request, uid=None):
        """
        Generate OTP for a meeting
        Endpoint: POST /api/meet/{uid}/generate-otp/
        """
        meeting = Meeting.objects.get(uid=uid)
        meeting.generate_otp()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='verify-otp')
    def verify_otp(self, request, uid=None):
        """
        Verify OTP for a meeting
        Endpoint: POST /api/meet/{uid}/verify-otp/
        Body: 
        {
            "otp_code": "OTP Code"
        }
        """
        meeting = Meeting.objects.get(uid=uid)
        if meeting.verify_otp(request.data.get('otp_code')):
            return Response({'status': 'OTP Verified'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='upload-photo')
    def upload_photo(self, request, uid=None):
        """
            Upload a photo for a meeting
            Endpoint: POST /api/meet/{uid}/upload-photo/
            Body: multipart/form-data
            Key: file (image file)
        """
        meeting = Meeting.objects.get(uid=uid)
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        photo = MeetingPhoto.objects.create(meeting=meeting, file=file, uploaded_by=request.user)
        return Response({'status': 'Photo uploaded', 'photo_id': photo.id}, status=status.HTTP_201_CREATED)