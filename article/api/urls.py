from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

import api.views as views

urlpatterns = [
    path('articles/', views.ArticlesView.as_view(), name = 'articles'),
    path('articles/<uuid:art_uuid>/', views.ArticleView.as_view(), name = 'article'),
    path('articles/auth/', views.CustomObtainTokenView.as_view(), name = 'authenticate'),
]

urlpatterns = format_suffix_patterns(urlpatterns)