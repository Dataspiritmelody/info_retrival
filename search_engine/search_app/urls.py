from django.urls import path 
from .views import search_view, index_view

urlpatterns = [
    path('search/', search_view, name='search'),
    path('',index_view,name = 'index')
]