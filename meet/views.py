from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from meet.models import Meeting
from meet.serializers import MeetingSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from base.views import logger

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
            "created_by": "Meeting Created By",
            "recipient_emails": "Meeting Recipient Emails list"
        }
        """
        try:
            serializer = MeetingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating meeting: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def retrieve(self, request, uid=None):
        """
        Retrieve a meeting
        Endpoint: GET /api/meet/{uid}/
        """
        try:
            meeting = Meeting.objects.get(uid=uid)
            serializer = MeetingSerializer(meeting)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Meeting not found for uid: {e}")
            return Response({"error": "Meeting not found"}, status=status.HTTP_404_NOT_FOUND)
    
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
            "created_by": "Meeting Created By",
            "recipient_emails": "Meeting Recipient Emails list"
        }
        """
        try:
            meeting = Meeting.objects.get(uid=uid)
            serializer = MeetingSerializer(meeting, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Meeting not found for uid: {e}")
            return Response({"error": "Meeting not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, uid=None):
        """
        Delete a meeting
        Endpoint: DELETE /api/meet/{uid}/
        """
        try:
            meeting = Meeting.objects.get(uid=uid)
            meeting.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"Meeting not found for uid: {e}")
            return Response({"error": "Meeting not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], url_path='upload-photo')
    def upload_photo(self, request, uid=None):
        """
            Upload a photo for a meeting
            Endpoint: POST /api/meet/{uid}/upload-photo/
            Body: multipart/form-data
            Key: file (image file)
        """
        try:
            meeting = Meeting.objects.get(uid=uid)
            file = request.FILES.get('file')
            if not file:
                return Response({'status': False, 'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
            
            photo = MeetingPhoto.objects.create(meeting=meeting, file=file, uploaded_by=request.user)
            return Response({'status': True, 'photo_id': photo.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Meeting not found for uid: {e}")
            return Response({"error": "Meeting not found"}, status=status.HTTP_404_NOT_FOUND)

class MeetingStatusViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'uid'

    @action(detail=True, methods=['post'], url_path='mark-in-progress')
    def mark_in_progress(self, request, uid=None):
        """
        Mark a meeting as in progress
        Endpoint: POST /api/meet/{uid}/mark-in-progress/
        Body: None
        """
        try:
            meeting = Meeting.objects.get(uid=uid)
            meeting.status_update_in_progress()
            serializer = MeetingSerializer(meeting)
            return Response({'status': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Meeting not found for uid: {e}")
            return Response({'status': False, 'error': 'Meeting not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], url_path='mark-completed')
    def mark_completed(self, request, uid=None):
        """
        Mark a meeting as completed
        Endpoint: POST /api/meet/{uid}/mark-completed/
        Body: 
        {
            "otp_code": "OTP Code"
        }
        """
        meeting = Meeting.objects.get(uid=uid)
        otp_code = request.data.get('otp_code')

        try:
            if otp_code:
                if meeting.verify_otp(otp_code):
                    meeting.status_update_completed()
                    serializer = MeetingSerializer(meeting)
                    return Response({'status': True, 'data': serializer.data}, status=status.HTTP_200_OK)
                else:
                    return Response({'status': False, 'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                meeting.generate_otp()
                return Response({'status': True, 'Message': 'Meeting OTP sent to the recipient.'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Meeting not found for uid: {e}")
            return Response({'status': False, 'error': 'Meeting not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], url_path='mark-cancelled')
    def mark_cancelled(self, request, uid=None):
        """
        Mark a meeting as cancelled
        Endpoint: POST /api/meet/{uid}/mark-cancelled/
        Body: None
        """
        try:
            meeting = Meeting.objects.get(uid=uid)
            meeting.status_update_cancelled(request.user)
            serializer = MeetingSerializer(meeting)
            return Response({'status': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Meeting not found for uid: {e}")
            return Response({'status': False, 'error': 'Meeting not found'}, status=status.HTTP_404_NOT_FOUND)