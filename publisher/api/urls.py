from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

import api.views as views

urlpatterns = [
    path('publishers/', views.PublishersView.as_view()),
    path('publishers/<uuid:p_uuid>/', views.PublisherView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)