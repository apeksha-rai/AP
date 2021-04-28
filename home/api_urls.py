from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers
from .views import ItemViewSet
from .views import ItemListView


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'item', ItemViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('filter_item/', ItemListView.as_view(), name='filter_item'),
]