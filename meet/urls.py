from django.urls import path
from rest_framework.routers import DefaultRouter
from meet.views import MeetingViewSet

router = DefaultRouter()
router.register(r'', MeetingViewSet, basename='meeting')

urlpatterns = [
    # Placeholder for future API endpoints
]

urlpatterns += router.urls
