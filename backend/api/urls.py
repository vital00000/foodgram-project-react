from rest_framework import routers
from django.urls import path, include

from api.views import (
    TagViewSet,
    RecipeViewSet,
    IngredientViewSet,
    FavoriteViewSet,
    PostFavoriteView,
    ShoppingCartView,
    download_shopping_cart
)


app_name = 'api'

v1_router = routers.DefaultRouter()
v1_router.register(r'tags', TagViewSet, basename='tag')
v1_router.register(r'recipes', RecipeViewSet, basename='recipe')
v1_router.register(r'ingredients', IngredientViewSet, basename='ingredient')
v1_router.register(r'favorites', FavoriteViewSet, basename='favorite')


urlpatterns = [
    path('api/recipes/<int:id>/favorite/', PostFavoriteView.as_view(),),
    path(
        'api/recipes/<int:id>/shopping_cart/',
        ShoppingCartView.as_view(),
        name='shopping_cart'
    ),
    path(
        'api/recipes/download_shopping_cart/',
        download_shopping_cart,
        name='download_shopping_cart'
    ),
    path('api/', include(v1_router.urls)),
]
