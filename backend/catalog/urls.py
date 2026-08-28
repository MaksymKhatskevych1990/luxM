from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CraftDetailViewSet,
    HomePageAPIView,
    MaterialViewSet,
    ProcessStepViewSet,
    ProjectViewSet,
    SiteSettingsView,
    WorkshopImageViewSet,
    WorkshopStatViewSet,
)

router = DefaultRouter()
router.register("projects", ProjectViewSet, basename="project")
router.register("materials", MaterialViewSet, basename="material")
router.register("process-steps", ProcessStepViewSet, basename="process-step")
router.register("craft-details", CraftDetailViewSet, basename="craft-detail")
router.register("workshop-stats", WorkshopStatViewSet, basename="workshop-stat")
router.register("workshop-images", WorkshopImageViewSet, basename="workshop-image")

urlpatterns = [
    path("", HomePageAPIView.as_view(), name="homepage"),
    path("home/", HomePageAPIView.as_view(), name="homepage-alt"),
    path("settings/", SiteSettingsView.as_view(), name="site-settings"),
    path("", include(router.urls)),
]
