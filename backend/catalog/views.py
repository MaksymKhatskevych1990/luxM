from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import (
    CraftDetail,
    HeroStat,
    Material,
    NavItem,
    PageSection,
    ProcessStep,
    Project,
    RoomType,
    SiteSettings,
    WorkshopImage,
    WorkshopStat,
)
from .serializers import (
    CraftDetailSerializer,
    HeroStatSerializer,
    MaterialSerializer,
    NavItemSerializer,
    PageSectionSerializer,
    ProcessStepSerializer,
    ProjectSerializer,
    RoomTypeSerializer,
    SiteSettingsSerializer,
    WorkshopImageSerializer,
    WorkshopStatSerializer,
)


def resolve_featured_project(settings, projects):
    featured = settings.featured_project
    if featured is not None and featured.is_published:
        return featured

    for project in projects:
        if project.show_in_detail_section:
            return project

    for project in projects:
        if project.stages.all():
            return project

    return None


class SiteSettingsView(RetrieveAPIView):
    serializer_class = SiteSettingsSerializer

    def get_object(self):
        return SiteSettings.load()


class ProjectViewSet(ReadOnlyModelViewSet):
    serializer_class = ProjectSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
    queryset = Project.objects.filter(is_published=True).prefetch_related(
        "stages", "gallery"
    )

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx


class MaterialViewSet(ReadOnlyModelViewSet):
    serializer_class = MaterialSerializer
    queryset = Material.objects.filter(is_published=True)


class ProcessStepViewSet(ReadOnlyModelViewSet):
    serializer_class = ProcessStepSerializer
    queryset = ProcessStep.objects.filter(is_published=True)


class CraftDetailViewSet(ReadOnlyModelViewSet):
    serializer_class = CraftDetailSerializer
    queryset = CraftDetail.objects.filter(is_published=True)


class WorkshopStatViewSet(ReadOnlyModelViewSet):
    serializer_class = WorkshopStatSerializer
    queryset = WorkshopStat.objects.all()


class WorkshopImageViewSet(ReadOnlyModelViewSet):
    serializer_class = WorkshopImageSerializer
    queryset = WorkshopImage.objects.all()


class HomePageAPIView(APIView):
    def get(self, request):
        settings = SiteSettings.load()
        projects = list(
            Project.objects.filter(is_published=True).prefetch_related(
                "stages", "gallery"
            )
        )
        featured = resolve_featured_project(settings, projects)
        ctx = {"request": request}
        return Response(
            {
                "settings": SiteSettingsSerializer(settings).data,
                "hero_stats": HeroStatSerializer(
                    HeroStat.objects.all(), many=True
                ).data,
                "sections": PageSectionSerializer(
                    PageSection.objects.filter(is_visible=True), many=True
                ).data,
                "navigation": NavItemSerializer(
                    NavItem.objects.filter(is_visible=True), many=True
                ).data,
                "room_types": RoomTypeSerializer(
                    RoomType.objects.filter(is_active=True), many=True
                ).data,
                "projects": ProjectSerializer(
                    projects, many=True, context=ctx
                ).data,
                "materials": MaterialSerializer(
                    Material.objects.filter(is_published=True), many=True
                ).data,
                "process_steps": ProcessStepSerializer(
                    ProcessStep.objects.filter(is_published=True), many=True
                ).data,
                "craft_details": CraftDetailSerializer(
                    CraftDetail.objects.filter(is_published=True), many=True
                ).data,
                "workshop_stats": WorkshopStatSerializer(
                    WorkshopStat.objects.all(), many=True
                ).data,
                "workshop_images": WorkshopImageSerializer(
                    WorkshopImage.objects.all(), many=True
                ).data,
                "featured_project_slug": featured.slug if featured else None,
            }
        )
