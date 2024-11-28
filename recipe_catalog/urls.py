from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import index, recipe_detail, about, add_ingredient, my_recipes, add_recipe, edit_recipe, delete_recipe, \
    add_recipe_ingredient, delete_recipe_ingredient, edit_recipe_ingredient, register

app_name = 'recipe_catalog'

urlpatterns = [
    path('', index, name='main'),
    path('login/', LoginView.as_view(template_name="recipe_catalog/login.html"), name='login'),
    path('logout/', LogoutView.as_view(next_page='recipe_catalog:main'), name='logout'),
    path('register/', register, name='register'),
    path('recipe/<int:pk>/', recipe_detail, name='recipe'),
    path('about', about, name='about'),
    path('ingredients/add/', add_ingredient, name='add_ingredient'),
    path('my_recipe/', my_recipes, name='my_recipes'),
    path('my_recipe/add/', add_recipe, name='add_recipe'),
    path('my_recipe/edit/<int:recipe_id>/', edit_recipe, name='edit_recipe'),
    path('my_recipe/delete/<int:recipe_id>/', delete_recipe, name='delete_recipe'),
    path('recipe/<int:recipe_id>/ingredients/add/', add_recipe_ingredient, name='add_recipe_ingredient'),
    path('recipe/<int:recipe_id>/ingredients/delete/<int:recipe_ingredient_id>/', delete_recipe_ingredient, name='delete_recipe_ingredient'),
    path('recipe/<int:recipe_id>/ingredients/edit/<int:recipe_ingredient_id>/', edit_recipe_ingredient, name='edit_recipe_ingredient'),
]
