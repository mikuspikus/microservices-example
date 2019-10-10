from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

import api.views as views

urlpatterns = [
    path('articles/', views.ArticlesView.as_view()),
    path('articles/<uuid:art_uuid>/', views.ArticleView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)