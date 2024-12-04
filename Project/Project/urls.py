# idcard_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('id_card.urls')),
    path('', include('bulk_app.urls')),
]
