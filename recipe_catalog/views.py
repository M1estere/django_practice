from django.http import HttpResponse, Http404
from django.shortcuts import render
from .models import Ingredient, Recipe


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
    ingredients = recipe.ingredients.all()
    if not recipe:
        return Http404("No such recipe found")

    total_price = sum([ingredient.price * ingredient.weight for ingredient in ingredients])
    total_weight = sum([ingredient.weight for ingredient in ingredients])

    context = {
        'recipe': recipe,
        'ingredients': ingredients,
        'total_price': total_price,
        'total_weight': total_weight
    }

    return render(
        request=request,
        template_name='recipe_catalog/recipe_desc.html',
        context=context
    )
