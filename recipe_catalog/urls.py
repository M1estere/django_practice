from django.urls import path
from .views import index, recipe_detail, about


urlpatterns = [
    path('', index, name='main'),
    path('recipe/<int:pk>/', recipe_detail, name='receipt'),
    path('about', about, name='about'),
]
