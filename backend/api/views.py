from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import IngredientFilter, RecipeFilter
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (FavoriteSerializer, GetRecipeSerializer,
                             GetSubscriptionSerializer, IngredientSerializer,
                             PostFavoriteSerializer, RecipeSerializer,
                             ShoppingCartSerializer, SubscriptionSerializer,
                             TagSerializer, IngredientRecipeSerializer)
from recopes.models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                            ShopCart, Subscription, Tag)
from users.models import User


class CreateListRetrieveViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    pass


class TagViewSet(CreateListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny, )
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientRecipeSerializer
    filterset_class = IngredientFilter
    permission_classes = (AllowAny, )


class IngredientforRecipeViewSet(viewsets.ModelViewSet):
    queryset = IngredientInRecipe.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter
    permission_classes = (AllowAny, )


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        is_favorited = self.request.query_params.get('is_favorited')
        if is_favorited is not None and int(is_favorited) == 1:
            return Recipe.objects.filter(favorite__user=self.request.user)
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart')
        if is_in_shopping_cart is not None and int(is_in_shopping_cart) == 1:
            return Recipe.objects.filter(shopping_cart__user=self.request.user)
        return Recipe.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response('Рецепт успешно удален',
                        status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetRecipeSerializer
        return RecipeSerializer

    def get_permissions(self):
        if self.action != 'create':
            return (IsAuthorOrReadOnly(),)
        return super().get_permissions()


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated, )


class GetSubscriptionsView(generics.ListAPIView):
    """ Получение списка подписчиков. """
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated, )

    @action(
        detail=False,
        methods=['get'],
    )
    def get(self, request):
        queryset = User.objects.filter(subscribes__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = GetSubscriptionSerializer(
            page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated, )


class PostFavoriteView(APIView):
    """ Добавление рецепта в Избранное. """
    serializer_class = PostFavoriteSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, id):
        data = {
            'user': request.user.id,
            'recipe': id
        }
        if not Favorite.objects.filter(
           user=request.user, recipe__id=id).exists():
            serializer = FavoriteSerializer(
                data=data, context={'request': request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        if Favorite.objects.filter(
            user=request.user,
            recipe__id=id
        ).exists():
            subscription = get_object_or_404(
                Favorite, user=request.user, recipe__id=id
            )
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ShoppingCartView(APIView):
    """ Добавление рецепта в корзину или его удаление. """
    serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, id):
        data = {
            'user': request.user.id,
            'recipe': id
        }
        recipe = get_object_or_404(Recipe, id=id)
        if not ShopCart.objects.filter(
           user=request.user, recipe=recipe).exists():
            serializer = ShoppingCartSerializer(
                data=data, context={'request': request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        if ShopCart.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists():
            subscription = get_object_or_404(
                ShopCart, user=request.user, recipe=recipe
            )
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_shopping_cart(request):
    """ Скачивание списка покупок с сайта. """
    ingredient_list = "Cписок покупок:"
    ingredients = IngredientInRecipe.objects.filter(
        recipe__shopping_cart__user=request.user
    ).values(
        'ingredient__name', 'ingredient__measurements_unit'
    ).annotate(amount=Sum('amount'))
    for num, i in enumerate(ingredients):
        ingredient_list += (
            f"\n{i['ingredient__name']} - "
            f"{i['amount']} {i['ingredient__measurements_unit']}"
        )
        if num < ingredients.count() - 1:
            ingredient_list += ', '
    file = 'shopping_list'
    response = HttpResponse(ingredient_list, 'Content-Type: application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{file}.pdf"'
    return response
