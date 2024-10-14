from django.http import HttpResponse, Http404
from django.shortcuts import render
from .constants import recipes
from .utils import get_recipe_by_id


def index(request):
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
    recipe = get_recipe_by_id(pk, recipes)
    if not recipe:
        return Http404("No such recipe found")

    context = {
        'recipe': recipe,
    }

    return render(
        request=request,
        template_name='recipe_catalog/recipe_desc.html',
        context=context
    )
