from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

import api.views as views

urlpatterns = [
    path('journals/', views.JournalsView.as_view()),
    path('journals/<uuid:j_uuid>/', views.JournalView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)