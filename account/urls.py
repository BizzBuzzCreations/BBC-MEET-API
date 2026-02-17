from django.urls import path
from .views import user_create, user_login, user_profile

urlpatterns = [
    path('create/', user_create),
    path('login/', user_login),
    path('profile/', user_profile),
]