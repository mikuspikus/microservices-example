from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from api.views import UserView, ArticlesView, JournalsView, PublisherView, ComplexView, BasicViews

urlpatterns = [
    path(r'', BasicViews.HomeView.as_view(), name = 'index'),
    path(r'logout/', BasicViews.LogoutView.as_view(), name = 'logout'),

    path('auth/', UserView.AuthenticateView.as_view(), name = 'authenticate'),
    path('info/', UserView.UserInfoView.as_view(), name = 'info'),
    path('register/', UserView.RegisterView.as_view(), name = 'register'), 
    path('users/', UserView.UsersView.as_view(), name = 'users'),
    path('users/<int:user_id>/', UserView.UserView.as_view(), name = 'user'),

    path('articles/', ArticlesView.ArticlesView.as_view(), name = 'articles'),
    path('articles/<uuid:art_uuid>/', ArticlesView.ArticleView.as_view(), name = 'article'),
    
    path('journals/', JournalsView.JournalsView.as_view(), name = 'journals'),
    path('journals/<uuid:j_uuid>/', JournalsView.JournalView.as_view(), name = 'journal'),
    
    path('publishers/', PublisherView.PublishersView.as_view(), name = 'publishers'),
    path('publishers/<uuid:p_uuid>/', PublisherView.PublisherView.as_view(), name = 'publisher'),

    path('users/<int:user_id>/articles/', ComplexView.UserArticlesView.as_view(), name = 'user-articles'),
    path('users/<int:user_id>/journals/', ComplexView.UserJournalsView.as_view(), name = 'user-journals'),
]

urlpatterns = format_suffix_patterns(urlpatterns)