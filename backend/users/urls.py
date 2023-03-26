from api.views import GetSubscriptionsView, SubscriptionViewSet
from django.urls import include, path
from rest_framework import routers
from users.views import SubscribeView

v1_router = routers.DefaultRouter()
v1_router.register(
    r'subscriptions', SubscriptionViewSet, basename='subscription'
)

urlpatterns = [
    path('api/users/subscriptions/', GetSubscriptionsView.as_view(),),
    path('api/users/<int:id>/subscribe/', SubscribeView.as_view(),),
    path('api/', include(v1_router.urls)),
]
