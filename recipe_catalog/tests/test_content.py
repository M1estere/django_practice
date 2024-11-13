from django.test import TestCase, Client
from django.urls import reverse

from ..models import Ingredient, Recipe, RecipeIngredients


class TestRecipes(TestCase):
    """Тесты страницы с рецептами"""
    INGREDIENTS = [
        dict(name="Ingredient 1", price=10, weight=15, raw_weight=35),
        dict(name="Ingredient 2", price=15, weight=50, raw_weight=70),
        dict(name="Ingredient 3", price=25, weight=100, raw_weight=120)
    ]

    def setUp(self):
        self.ingredients = []
        self.recipe = Recipe.objects.create(name="Test")

        for ingredient in self.INGREDIENTS:
            self.ingredients.append(Ingredient.objects.create(name=ingredient["name"], weight=ingredient['weight'], raw_weight=ingredient['raw_weight'], price=ingredient["price"]))

        for ingredient, ingredient_class in zip(self.INGREDIENTS, self.ingredients):
            RecipeIngredients.objects.create(recipe=self.recipe, ingredient=ingredient_class)

        self.total_price = sum([ingredient['weight'] * ingredient['price'] for ingredient in self.INGREDIENTS])
        self.total_weight = sum([ingredient['weight'] for ingredient in self.INGREDIENTS])

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
