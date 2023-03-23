from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from users.models import User
from recopes.models import (
    Tag,
    Recipe,
    Ingredient,
    Subscription,
    IngredientInRecipe,
    Favorite,
    ShopCart
)
from rest_framework.validators import UniqueTogetherValidator
from drf_extra_fields.fields import Base64ImageField


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=request.user, author=obj
        ).exists()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.Serializer):
    id = serializers.CharField(allow_blank=True)
    name = serializers.CharField(allow_blank=True)
    measurements_unit = serializers.CharField(allow_blank=True)

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurements_unit',)


class IngredientRecipeGetRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurements_unit = serializers.ReadOnlyField(
        source='ingredient.measurements_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurements_unit', 'amount')
        validators = [
            UniqueTogetherValidator(
                queryset=IngredientInRecipe.objects.all(),
                fields=['ingredient', 'recipe']
            )
        ]


class IngredientRecipeSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(read_only=True)
    amount = serializers.IntegerField(write_only=True, min_value=1)
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount', 'recipe')


class GetRecipeSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    ingredients = serializers.SerializerMethodField()
    author = CustomUserSerializer()
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'name',
            'text',
            'ingredients',
            'tags',
            'cooking_time',
            'image'
        )
        read_only_fields = ('id', 'author',)

    def get_ingredients(self, obj):
        recipe_ingredients = IngredientInRecipe.objects.filter(recipe=obj)
        return IngredientRecipeGetRecipeSerializer(
            recipe_ingredients, many=True).data


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientRecipeSerializer(many=True)
    author = UserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    image = Base64ImageField(max_length=None, use_url=True)
    cooking_time = serializers.IntegerField(min_value=1)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'name',
            'text',
            'ingredients',
            'tags',
            'cooking_time',
            'image'
        )
        read_only_fields = ('id', 'author', 'tags')

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        ingredients_list = [ingredient['id'] for ingredient in ingredients]
        if len(ingredients_list) != len(set(ingredients_list)):
            raise serializers.ValidationError(
                'Проверьте, какой-то ингредиент был выбран более 1 раза'
            )
        return data

    def recipe_ingredient_create(self, ingredients_data, models, recipe):
        bulk_create_data = (
            models(
                recipe=recipe,
                ingredient=ingredient_data['ingredient'],
                amount=ingredient_data['amount'])
            for ingredient_data in ingredients_data
            )
        models.objects.bulk_create(bulk_create_data)

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags_data)
        self.recipe_ingredient_create(
            ingredients_data, IngredientInRecipe, recipe
            )
        return recipe

    def update(self, instance, validated_data):
        if 'tags' in self.validated_data:
            tags_data = validated_data.pop('tags')
            instance.tags.set(tags_data)
        if 'ingredients' in self.validated_data:
            ingredients_data = validated_data.pop('ingredients')
            amount_set = IngredientInRecipe.objects.filter(
                recipe__id=instance.id)
            amount_set.delete()
            self.recipe_ingredient_create(
                ingredients_data, IngredientInRecipe, instance
                )
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        self.fields.pop('ingredients')
        self.fields.pop('tags')
        representation = super().to_representation(instance)
        representation['ingredients'] = IngredientRecipeGetRecipeSerializer(
            IngredientInRecipe.objects.filter(recipe=instance), many=True
        ).data
        representation['tags'] = TagSerializer(
            instance.tags, many=True
        ).data
        return representation


class SubscriptionSerializer(serializers.ModelSerializer):
    """ Сериализатор подписок. """

    class Meta:
        model = Subscription
        fields = ['user', 'author']
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=['user', 'author'],
                message='Вы уже подписаны на автора',
            )
        ]

    def to_representation(self, instance):
        return GetSubscriptionSerializer(instance.author, context={
            'request': self.context.get('request')
        }).data


class GetSubscriptionSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=request.user, author=obj
        ).exists()


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор избранного."""
    class Meta:
        model = Favorite
        fields = ['user', 'recipe']
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['user', 'recipe'],
                message='Этот рецепт уже есть в избранном',
            )
        ]

    def to_representation(self, instance):
        return PostFavoriteSerializer(instance.recipe, context={
            'request': self.context.get('request')
        }).data


class PostFavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class ShoppingCartSerializer(serializers.ModelSerializer):
    """ Сериализатор для списка покупок. """
    class Meta:
        model = ShopCart
        fields = ['user', 'recipe']

    def to_representation(self, instance):
        return PostFavoriteSerializer(instance.recipe, context={
            'request': self.context.get('request')
        }).data