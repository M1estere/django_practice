from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Recipe, Ingredient, RecipeIngredients


class RecipeLogicTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username='author', password='password123')
        self.other_user = User.objects.create_user(username='other_user', password='password123')

        self.ingredient = Ingredient.objects.create(name='Сахар', measure_val='грамм', price=10)

        self.recipe = Recipe.objects.create(name='Пирог', author=self.author)
        self.recipe_ingredient = RecipeIngredients.objects.create(
            recipe=self.recipe, ingredient=self.ingredient, measure=2, measure_weight=100
        )

    # Тесты для создания рецептов
    def test_create_recipe_requires_authentication(self):
        """Создание рецепта неавторизованным"""
        response = self.client.post(reverse('recipe_catalog:add_recipe'), {'name': 'Торт'})
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('recipe_catalog:login'), response.url)

    def test_create_recipe_authorized(self):
        """"Создание рецепта авторизованным"""
        self.client.login(username='author', password='password123')
        response = self.client.post(reverse('recipe_catalog:add_recipe'), {'name': 'Торт'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Recipe.objects.count(), 2)

    def test_edit_recipe_requires_authentication(self):
        """Редактирование рецепта неавторизованным"""
        response = self.client.get(reverse('recipe_catalog:edit_recipe', kwargs={'recipe_id': self.recipe.id}))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('recipe_catalog:login'), response.url)

    def test_edit_recipe_authorized(self):
        """Редактирование рецепта авторизованным"""
        self.client.login(username='author', password='password123')
        response = self.client.post(
            reverse('recipe_catalog:edit_recipe', kwargs={'recipe_id': self.recipe.id}),
            {'name': 'Обновленный Пирог'}
        )
        self.assertEqual(response.status_code, 302)
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.name, 'Обновленный Пирог')

    def test_edit_recipe_other_user(self):
        """Редактирование чужого рецепта"""
        self.client.login(username='other_user', password='password123')
        response = self.client.post(
            reverse('recipe_catalog:edit_recipe', kwargs={'recipe_id': self.recipe.id}),
            {'name': 'Обновленный Пирог'}
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_recipe_requires_authentication(self):
        """Удаление рецепта неавторизованным"""
        response = self.client.post(reverse('recipe_catalog:delete_recipe', kwargs={'recipe_id': self.recipe.id}))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('recipe_catalog:login'), response.url)

    def test_delete_recipe_authorized(self):
        """Удаление рецепта авторизованным"""
        self.client.login(username='author', password='password123')
        response = self.client.post(reverse('recipe_catalog:delete_recipe', kwargs={'recipe_id': self.recipe.id}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Recipe.objects.count(), 0)

    def test_delete_recipe_other_user(self):
        """Удаление чужого рецепта"""
        self.client.login(username='other_user', password='password123')
        response = self.client.post(reverse('recipe_catalog:delete_recipe', kwargs={'recipe_id': self.recipe.id}))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Recipe.objects.count(), 1)

    def test_add_ingredient_requires_authentication(self):
        """Добавление ингредиента неавторизованным"""
        response = self.client.post(reverse('recipe_catalog:add_ingredient'), {
            'name': 'Мука',
            'measure_val': 'грамм',
            'price': 5
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('recipe_catalog:login'), response.url)

    def test_add_ingredient_authorized(self):
        """Добавление ингредиента авторизованным"""
        self.client.login(username='author', password='password123')
        response = self.client.post(reverse('recipe_catalog:add_ingredient'), {
            'name': 'Мука',
            'measure_val': 'грамм',
            'price': 5
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Ingredient.objects.count(), 2)

    def test_edit_recipe_ingredient(self):
        """Редактирование ингредиента рецепта"""
        self.client.login(username='author', password='password123')
        response = self.client.post(
            reverse('recipe_catalog:edit_recipe_ingredient', kwargs={
                'recipe_id': self.recipe.id, 'recipe_ingredient_id': self.recipe_ingredient.id
            }),
            {'measure': 3, 'measure_weight': 150}
        )
        self.assertEqual(response.status_code, 302)
        self.recipe_ingredient.refresh_from_db()
        self.assertEqual(self.recipe_ingredient.measure, 3)
        self.assertEqual(self.recipe_ingredient.measure_weight, 150)

    def test_edit_recipe_ingredient_other_user(self):
        """Редактирование ингредиента чужого рецепта"""
        self.client.login(username='other_user', password='password123')
        response = self.client.post(
            reverse('recipe_catalog:edit_recipe_ingredient', kwargs={
                'recipe_id': self.recipe.id, 'recipe_ingredient_id': self.recipe_ingredient.id
            }),
            {'measure': 3, 'measure_weight': 150}
        )
        self.assertEqual(response.status_code, 404)
        self.recipe_ingredient.refresh_from_db()
        self.assertNotEqual(self.recipe_ingredient.measure, 3)

    def test_delete_recipe_ingredient(self):
        """Удаление ингредиента рецепта"""
        self.client.login(username='author', password='password123')
        response = self.client.post(reverse('recipe_catalog:delete_recipe_ingredient', kwargs={
            'recipe_id': self.recipe.id, 'recipe_ingredient_id': self.recipe_ingredient.id
        }))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(RecipeIngredients.objects.count(), 0)

    def test_delete_recipe_ingredient_other_user(self):
        """Удаление ингредиента чужого рецепта"""
        self.client.login(username='other_user', password='password123')
        response = self.client.post(reverse('recipe_catalog:delete_recipe_ingredient', kwargs={
            'recipe_id': self.recipe.id, 'recipe_ingredient_id': self.recipe_ingredient.id
        }))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(RecipeIngredients.objects.count(), 1)
