from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

import api.views as views

urlpatterns = [
    path('publishers/', views.PublishersView.as_view(), name = 'publisher'),
    path('publishers/<uuid:p_uuid>/', views.PublisherView.as_view(), name = 'concrete_publisher'),
]

urlpatterns = format_suffix_patterns(urlpatterns)