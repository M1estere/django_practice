from django.http import HttpResponse, Http404
from django.shortcuts import render
from .models import Ingredient, Recipe, RecipeIngredients


def index(request):
    recipes = Recipe.objects.all()
    t_recipes = recipes
    context = {
        'recipes': t_recipes,
        'recipes_len': len(t_recipes)
    }

    return render(
        request=request,
        template_name='recipe_catalog/index.html',
        context=context
    )


def about(request):
    return render(
        request=request,
        template_name='recipe_catalog/about.html',
    )


def recipe_detail(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    if not recipe:
        return Http404("No such recipe found")

    ingredients = RecipeIngredients.objects.filter(recipe=recipe)

    target_ingredients = list()
    total_price = 0
    total_weight = 0
    for ingredient in ingredients:
        ingredient_price = ingredient.measure * ingredient.ingredient.price

        total_price += ingredient_price
        total_weight += ingredient.measure_weight * ingredient.measure

        target_ingredients.append({
            'id': ingredient.ingredient.id,
            'name': ingredient.ingredient.name,
            'measure_val': ingredient.ingredient.measure_val,
            'measure': ingredient.measure,
            'price': ingredient_price
        })

    context = {
        'recipe': recipe,
        'ingredients': target_ingredients,
        'total_price': total_price,
        'total_weight': total_weight
    }

    return render(
        request=request,
        template_name='recipe_catalog/recipe_desc.html',
        context=context
    )
