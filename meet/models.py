from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
import random
from django.core.mail import send_mail
from django.conf import settings

class Meeting(BaseModel):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    MEETING_TYPE_CHOICES = [
        ('in_person', 'In Person'),
        ('online', 'Online'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255)
    meeting_type = models.CharField(max_length=20, choices=MEETING_TYPE_CHOICES, default='in_person')
    start_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(help_text="Duration of the meeting in minutes")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_meetings')
    
    # OTP fields for verification upon completion
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    is_otp_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
    
    def generate_otp(self):
        self.otp_code = str(random.randint(100000, 999999))
        self.save()
        
        subject = f"Your Meeting Verification Code: {self.otp_code}"
        message = f"Hello,\n\nYour OTP for the meeting '{self.title}' is: {self.otp_code}\n\nPlease provide this code to the meeting organizer to verify your attendance.\n\nThank you,\nBBC Meet Team"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [self.created_by.email] # Send to organizer for now, logic can change based on requirements
        
        send_mail(subject, message, from_email, recipient_list)

    def verify_otp(self, otp_code):
        if self.otp_code == otp_code:
            self.is_otp_verified = True
            self.save()
            return True
        return False

class MeetingPhoto(BaseModel):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='photos')
    file = models.ImageField(upload_to='meeting_photos/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_photos')

    def __str__(self):
        return f"Photo for {self.meeting.title} - {self.created_at}"
