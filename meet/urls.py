from django.urls import path
from rest_framework.routers import DefaultRouter
from meet.views import MeetingViewSet, MeetingStatusViewSet

router = DefaultRouter()
router.register(r'', MeetingViewSet, basename='meeting')
router.register(r'', MeetingStatusViewSet, basename='meeting-status')

urlpatterns = [
    # Placeholder for future API endpoints
]

urlpatterns += router.urls
