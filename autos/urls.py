from django.urls import path
from . import views
from django.views.generic import TemplateView

# https://docs.djangoproject.com/en/3.0/topics/http/urls/
app_name = 'autos'
urlpatterns = [
    path('', views.MainView.as_view(), name='all'),
    path('main/create/', views.AutoCreate.as_view(), name='auto_create'),
    path('main/<int:pk>/update/', views.AutoUpdate.as_view(), name='auto_update'),
    path('main/<int:pk>/delete/', views.AutoDelete.as_view(), name='auto_delete'),
    path('lookup/', views.BrandView.as_view(), name='brand_list'),
    path('lookup/create/', views.BrandCreate.as_view(), name='brand_create'),
    path('lookup/<int:pk>/update/', views.BrandUpdate.as_view(), name='brand_update'),
    path('lookup/<int:pk>/delete/', views.BrandDelete.as_view(), name='brand_delete'),
]

# Note that brand_ and auto_ give us uniqueness within this application
