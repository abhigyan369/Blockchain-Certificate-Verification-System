from django.urls import path
from . import views

urlpatterns = [
    path('', views.certificate_list, name='certificate_list'),
    path('create/', views.certificate_create, name='certificate_create'),
    path('update/<str:certificate_id>/', views.certificate_update, name='certificate_update'),
    path('delete/<str:certificate_id>/', views.certificate_delete, name='certificate_delete'),
]
