from rest_framework import routers, urlpatterns
from rest_framework.routers import DefaultRouter
from .views import ProductsViewSet


router = DefaultRouter()

router.register('',ProductsViewSet)
urlpatterns = router.urls;