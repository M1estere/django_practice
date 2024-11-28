from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

from .forms import IngredientForm, RecipeForm, RecipeIngredientForm, RecipeIngredientEditForm, UserRegistrationForm
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
        ingredient_weight = ingredient.measure_weight * ingredient.measure

        total_price += ingredient_price
        total_weight += ingredient_weight

        target_ingredients.append({
            'id': ingredient.ingredient.id,
            'name': ingredient.ingredient.name,
            'measure_val': ingredient.ingredient.measure_val,
            'measure': ingredient_weight,
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


@login_required
def add_ingredient(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recipe_catalog:main')
    else:
        form = IngredientForm()

    return render(request, 'recipe_catalog/add_ingredient.html', {'form': form})


@login_required
def my_recipes(request):
    recipes = Recipe.objects.filter(author=request.user)
    return render(request, 'recipe_catalog/my_recipes.html', {'recipes': recipes})


@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user  # Устанавливаем автора текущим пользователем
            recipe.save()
            return redirect('recipe_catalog:my_recipes')
    else:
        form = RecipeForm()

    return render(request, 'recipe_catalog/add_recipe.html', {'form': form})


@login_required
def edit_recipe(request, recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id, author=request.user)
    except Recipe.DoesNotExist:
        raise Http404("Рецепт не найден или недоступен.")

    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_catalog:edit_recipe', recipe_id=recipe_id)
    else:
        form = RecipeForm(instance=recipe)

    ingredients = RecipeIngredients.objects.filter(recipe=recipe)

    context = {
        'form': form,
        'recipe': recipe,
        'ingredients': ingredients,
    }
    return render(request, 'recipe_catalog/edit_recipe.html', context)


@login_required
def delete_recipe(request, recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id, author=request.user)
    except Recipe.DoesNotExist:
        raise Http404("Рецепт не найден или недоступен.")

    if request.method == 'POST':
        recipe.delete()
        return redirect('recipe_catalog:my_recipes')

    return render(request, 'recipe_catalog/delete_recipe.html', {'recipe': recipe})


@login_required
def add_recipe_ingredient(request, recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id, author=request.user)
    except Recipe.DoesNotExist:
        raise Http404("Рецепт не найден или недоступен.")

    if request.method == 'POST':
        form = RecipeIngredientForm(request.POST)
        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.recipe = recipe
            ingredient.save()
            return redirect('recipe_catalog:edit_recipe', recipe_id=recipe_id)
    else:
        form = RecipeIngredientForm()

    return render(request, 'recipe_catalog/add_recipe_ingredient.html', {'form': form, 'recipe': recipe})


@login_required
def delete_recipe_ingredient(request, recipe_id, recipe_ingredient_id):
    try:
        ingredient = RecipeIngredients.objects.get(
            id=recipe_ingredient_id, recipe__id=recipe_id, recipe__author=request.user
        )
        ingredient.delete()
    except RecipeIngredients.DoesNotExist:
        raise Http404("Ингредиент не найден или недоступен.")

    return redirect('recipe_catalog:edit_recipe', recipe_id=recipe_id)


@login_required
def edit_recipe_ingredient(request, recipe_id, recipe_ingredient_id):
    try:
        ingredient = RecipeIngredients.objects.get(
            id=recipe_ingredient_id, recipe__id=recipe_id, recipe__author=request.user
        )
    except RecipeIngredients.DoesNotExist:
        raise Http404("Ингредиент не найден или недоступен.")

    if request.method == 'POST':
        form = RecipeIngredientEditForm(request.POST, instance=ingredient)
        if form.is_valid():
            form.save()
            return redirect('recipe_catalog:edit_recipe', recipe_id=recipe_id)
    else:
        form = RecipeIngredientEditForm(instance=ingredient)

    return render(request, 'recipe_catalog/edit_recipe_ingredient.html', {'form': form, 'recipe': ingredient.recipe, 'ingredient': ingredient})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'recipe_catalog/register.html', {'form': form})
