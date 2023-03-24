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

router = routers.DefaultRouter()
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'recipes', RecipeViewSet, basename='recipe')
router.register(r'ingredients', IngredientViewSet, basename='ingredient')
router.register(r'favorites', FavoriteViewSet, basename='favorite')


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
    path('api/', include(router.urls)),
]
