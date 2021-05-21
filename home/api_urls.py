from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers
from .views import ProductViewSet
from .views import ProductListView


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'item', ProductViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('filter_item/', ProductListView.as_view(), name='filter_item'),
]