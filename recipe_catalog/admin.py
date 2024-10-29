from django.contrib import admin
from .models import Ingredient, Recipe, RecipeIngredients


class IngredientInline(admin.StackedInline):
    model = RecipeIngredients
    extra = 5


class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline]
    list_display = ["name"]


class IngredientAdmin(admin.ModelAdmin):
    list_display = ["name"]


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
