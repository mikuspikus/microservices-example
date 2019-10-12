from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

import api.views as views

urlpatterns = [
    path('info/', views.UserInfoView.as_view(), name = 'info'),
    path('register/', views.RegisterView.as_view(), name = 'register'), 
    path('users/', views.UsersView.as_view(), name = 'users'),
    path('users/<int:user_id>/', views.UserView.as_view(), name = 'user'),
    path('auth/', views.CustomAuthToken.as_view(), name = 'authorization')
]

urlpatterns = format_suffix_patterns(urlpatterns)