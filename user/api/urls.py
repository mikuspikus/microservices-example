from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

import api.views as views

urlpatterns = [
    path('info/', views.UserInfoView.as_view(), name = 'info'),
    path('register/', views.RegisterView.as_view(), name = 'register'), 
    path('users/', views.UsersView.as_view(), name = 'users'),
    path('users/<int:user_id>/', views.UserView.as_view(), name = 'user'),
    path('auth/', views.CustomAuthToken.as_view(), name = 'authorization'),
]


# html_urlpatterns = [
#     path('html/auth/', views.AuthHTMLView.as_view(), name = 'html-authorization'),
#     path('html/info/', views.InfoHTMLView.as_view(), name = 'html-info'),
#     path('html/register/', views.RegisterHTMLView.as_view(), name = 'html-register'),
#     path('html/users/<int: user_id>', views.RegisterHTMLView.as_view(), name = 'html-user'),
# ]

# urlpatterns += format_suffix_patterns(html_urlpatterns, allowed = ('html'))