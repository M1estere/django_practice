class Ingredient:
    def __init__(self, name, weight, raw_weight, price):
        self._name = name
        self._weight = weight
        self._raw_weight = raw_weight
        self._price = price

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        self._name = name

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, weight):
        if not isinstance(weight, (int, float)):
            raise TypeError("Weight must be a number.")
        self._weight = weight

    @property
    def raw_weight(self):
        return self._raw_weight

    @weight.setter
    def raw_weight(self, weight):
        if not isinstance(weight, (int, float)):
            raise TypeError("Weight must be a number.")
        self._weight = weight

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        if not isinstance(price, (int, float)):
            raise TypeError("Price must be a number.")
        self._price = price


class Recipe:
    def __init__(self, id, name, ingredients):
        self.id = id
        self.name = name
        self.ingredients = ingredients

        self._set_ingredients()

    def _set_ingredients(self):
        self.ingredients = [Ingredient(element[0], element[1], element[2], element[3]) for element in self.ingredients]

    def calc_cost(self, portions=1):
        return sum([element.price for element in self.ingredients]) * portions

    def calc_weight(self, portions=1, raw=True):
        return sum([element.raw_weight if raw else element.weight for element in self.ingredients]) * portions

    def __str__(self):
        return f'Рецепт {self.name} содержит:\n' + '\n'.join(
            [f'- {ingredient.name} - {ingredient.weight}г, {ingredient.price}₽' for ingredient in self.ingredients])


def get_recipe_by_id(recipe_id, recipe_list):
    return next(filter(lambda x: x.id == recipe_id, recipe_list), None)
