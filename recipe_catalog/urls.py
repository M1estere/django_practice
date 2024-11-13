from django.urls import path
from .views import index, recipe_detail, about

app_name = 'recipe_catalog'

urlpatterns = [
    path('', index, name='main'),
    path('recipe/<int:pk>/', recipe_detail, name='recipe'),
    path('about', about, name='about'),
]
