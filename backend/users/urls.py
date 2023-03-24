from rest_framework import routers
from django.urls import path, include

from users.views import SubscribeView

from api.views import (GetSubscriptionsView, SubscriptionViewSet)


app_name = 'api'

router = routers.DefaultRouter()
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')

urlpatterns = [
    path('api/users/subscriptions/', GetSubscriptionsView.as_view(),),
    path('api/users/<int:id>/subscribe/', SubscribeView.as_view(),),
    path('api/', include(router.urls)),
]
