from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from ..models import Ingredient, Recipe, RecipeIngredients


class TestRecipes(TestCase):
    """Тесты страницы с рецептами"""
    INGREDIENTS = [
        dict(name="Ingredient 1", price=10, measure=10, measure_weight=15),
        dict(name="Ingredient 2", price=15, measure=15, measure_weight=3),
        dict(name="Ingredient 3", price=25, measure=22, measure_weight=17)
    ]

    def setUp(self):
        self.ingredients = []
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client = Client()
        self.client.login(username="testuser", password="testpassword")
        self.recipe = Recipe.objects.create(name="Test", author=self.user)

        for ingredient in self.INGREDIENTS:
            self.ingredients.append(Ingredient.objects.create(name=ingredient["name"], price=ingredient["price"], measure_val=ingredient["measure"]))

        for ingredient, ingredient_class in zip(self.INGREDIENTS, self.ingredients):
            RecipeIngredients.objects.create(recipe=self.recipe, ingredient=ingredient_class, measure=ingredient['measure'], measure_weight=ingredient['measure_weight'])

        self.total_price = sum([ingredient['measure'] * ingredient['price'] for ingredient in self.INGREDIENTS])
        self.total_weight = sum([ingredient['measure_weight'] * ingredient['measure'] for ingredient in self.INGREDIENTS])

        self.client = Client()

    def get_response(self):
        """Получение ответа со страницы рецепта"""
        response = self.client.get(reverse('recipe_catalog:recipe', kwargs={'pk': self.recipe.id}))
        return response

    def test_context(self):
        """Проверка наличия всех нужных ключей в контексте"""
        response = self.get_response()

        page_fields = (
            "recipe",
            "ingredients",
            "total_price",
            "total_weight",
        )

        length = sum([1 for key in page_fields if key in response.context])
        self.assertEqual(length, len(page_fields))

    def test_total_weight_calculation(self):
        """Проверка расчета суммарного веса"""
        response = self.get_response()
        self.assertEqual(response.context['total_weight'], self.total_weight)

    def test_total_cost_calculation(self):
        """Проверка расчета суммарной стоимости"""
        response = self.get_response()
        self.assertEqual(response.context['total_price'], self.total_price)


