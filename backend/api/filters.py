import django_filters
from django_filters import rest_framework as filter

from recopes.models import Ingredient, Recipe, Tag
from users.models import User


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    author = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = filter.BooleanFilter(method='get_favorite')
    is_in_shopping_cart = filter.BooleanFilter(
        method='get_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')


class IngredientFilter(django_filters.FilterSet):
    ingredient = django_filters.ModelChoiceFilter(queryset=Ingredient.objects.all())

    class Meta:
        model = Ingredient
        fields = ('ingredient', )
