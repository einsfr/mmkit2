from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'items', views.ItemViewSet)
router.register(r'categories', views.CategoryViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
