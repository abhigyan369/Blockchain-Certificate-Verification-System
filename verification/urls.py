from django.urls import path
from . import views

urlpatterns = [
    path('verify/<str:certificate_id>/', views.verify_certificate, name='verify_certificate'),
]
