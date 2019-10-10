from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from api.views import UserView, ArticlesView, JournalsView, PublisherView

urlpatterns = [
    path('auth/', UserView.AuthenticateView.as_view(), name = 'authenticate'),
    path('info/', UserView.UserInfoView.as_view(), name = 'info'),
    path('register/', UserView.RegisterView.as_view(), name = 'register'), 
    path('users/', UserView.UsersView.as_view(), name = 'users'),
    path('users/<int:user_id>/', UserView.UserView.as_view(), name = 'user'),

    path('articles/', ArticlesView.ArticlesView.as_view(), name = 'articles'),
    path('articles/<uuid:art_uuid>/', ArticlesView.ArticleView.as_view(), name = 'article'),
    
    path('journals/', JournalsView.JournalsView.as_view(), name = 'journals'),
    path('journals/<uuid:j_uuid>/', JournalsView.JournalView.as_view(), name = 'journal'),
    
    path('publisher/', PublisherView.PublishersView.as_view(), name = 'publishers'),
    path('publisher/<uuid:p_uuid>/', PublisherView.PublisherView.as_view(), name = 'publisher'),
]

urlpatterns = format_suffix_patterns(urlpatterns)