from django.urls import path
from .views import Bulkprocess

urlpatterns = [

    path('bulk_upload/',Bulkprocess.as_view(), name= "bulk_upload"),
]