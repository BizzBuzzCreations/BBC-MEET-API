from django.contrib import admin
from .models import Meeting, MeetingPhoto

class MeetingPhotoInline(admin.TabularInline):
    model = MeetingPhoto
    extra = 1

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'meeting_type', 'start_time', 'duration_minutes', 'status', 'is_otp_verified')
    list_filter = ('status', 'meeting_type', 'start_time', 'is_otp_verified')
    search_fields = ('title', 'description', 'location', 'created_by__username', 'created_by__email')
    ordering = ('-start_time',)
    inlines = [MeetingPhotoInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'created_by', 'meeting_type')
        }),
        ('Schedule & Location', {
            'fields': ('location', 'start_time', 'duration_minutes')
        }),
        ('Status & Verification', {
            'fields': ('status', 'otp_code', 'is_otp_verified')
        }),
    )

@admin.register(MeetingPhoto)
class MeetingPhotoAdmin(admin.ModelAdmin):
    list_display = ('meeting', 'uploaded_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('meeting__title', 'uploaded_by__username')
