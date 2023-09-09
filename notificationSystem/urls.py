from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.events.viewsets import EventViewSet
from apps.accounts.views import UserViewSet



router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
]
urlpatterns += router.urls