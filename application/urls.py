from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

app_name = 'accounts'

urlpatterns = [   
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register-user/', views.RegisterView.as_view(), name='register user'),
    path('all-users/', views.UserProfileView.as_view(), name='all users'),
    path('update-position/', views.UpdatePositionView.as_view()),
    
    path('missions/<str:name>', views.DetailMissionView.as_view()),
    path('register-mission/', views.RegisterMissionView.as_view(), name='register mission'),
    path('all-missions/', views.ListMissionView.as_view(), name='profile'),
    path('near-postchi/', views.FindNearPostchiView.as_view()),
    
]