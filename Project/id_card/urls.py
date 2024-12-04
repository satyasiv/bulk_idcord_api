from django.urls import path
from .views import Id_Creation

urlpatterns = [
    path('id_creation/', Id_Creation.as_view(), name='generate-id-card'),

]