from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator


class Ingredient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    measure_val = models.CharField(max_length=255)
    price = models.IntegerField()

    def __str__(self):
        return self.name


class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredients')

    def __str__(self):
        return self.name


class RecipeIngredients(models.Model):
    id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    measure = models.IntegerField(validators=[MinValueValidator(1)])
    measure_weight = models.IntegerField(validators=[MinValueValidator(1)])
