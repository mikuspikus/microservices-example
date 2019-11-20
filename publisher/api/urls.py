from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

import api.views as views

urlpatterns = [
    path('publishers/', views.PublishersView.as_view(), name = 'publishers'),
    path('publishers/<uuid:p_uuid>/', views.PublisherView.as_view(), name = 'publisher'),
]

urlhtmlonlypatterns = [
    path('publishers/html/', views.PublisherHTMLView.as_view(), name = 'html-publisher'),
]

urlpatterns += format_suffix_patterns(urlhtmlonlypatterns, allowed=('html'))