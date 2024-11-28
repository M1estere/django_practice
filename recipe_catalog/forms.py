from django import forms
from django.contrib.auth.models import User

from .models import Ingredient, Recipe, RecipeIngredients


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'measure_val', 'price']


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name']


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredients
        fields = ['ingredient', 'measure', 'measure_weight']


class RecipeIngredientEditForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredients
        fields = ['measure', 'measure_weight']


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают")
        return password_confirm