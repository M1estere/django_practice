from django.test import TestCase
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
        recipe = Recipe.objects.create(
            name='Test'
        )
        response = self.client.get(reverse('recipe_catalog:recipe', args=[recipe.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, recipe.name)

    def test_about_page_view(self):
        """Проверка доступности страницы 'о сайте'"""
        response = self.client.get(reverse('recipe_catalog:about'))
        self.assertEqual(response.status_code, 200)
