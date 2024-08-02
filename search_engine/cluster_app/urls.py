from django.urls import path 
from .views import cluster_view,cluster_result

urlpatterns = [
    path('', cluster_view, name='cluster'),
    path('result/', cluster_result, name='cluster_result'),
]