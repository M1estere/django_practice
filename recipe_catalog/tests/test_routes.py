from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from ..models import Ingredient, Recipe, RecipeIngredients


class RecipeViewsTests(TestCase):
    def test_recipes_list_view(self):
        """Проверка доступности страницы списка рецептов"""
        response = self.client.get(reverse('recipe_catalog:main'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_view(self):
        """Проверка доступности страницы деталей конкретного рецепта"""
        # Создаем тестовый рецепт
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client = Client()
        self.client.login(username="testuser", password="testpassword")
        recipe = Recipe.objects.create(
            name='Test', author=self.user
        )
        response = self.client.get(reverse('recipe_catalog:recipe', args=[recipe.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, recipe.name)

    def test_about_page_view(self):
        """Проверка доступности страницы 'о сайте'"""
        response = self.client.get(reverse('recipe_catalog:about'))
        self.assertEqual(response.status_code, 200)
