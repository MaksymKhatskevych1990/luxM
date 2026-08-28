from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import (
    CraftDetail,
    Material,
    ProcessStep,
    Project,
    SiteSettings,
    WorkshopImage,
    WorkshopStat,
)
from .serializers import (
    CraftDetailSerializer,
    MaterialSerializer,
    ProcessStepSerializer,
    ProjectSerializer,
    SiteSettingsSerializer,
    WorkshopImageSerializer,
    WorkshopStatSerializer,
)


class SiteSettingsView(RetrieveAPIView):
    serializer_class = SiteSettingsSerializer

    def get_object(self):
        return SiteSettings.load()


class ProjectViewSet(ReadOnlyModelViewSet):
    serializer_class = ProjectSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
    queryset = Project.objects.filter(is_published=True).prefetch_related("stages")


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
        projects = Project.objects.filter(is_published=True).prefetch_related("stages")
        materials = Material.objects.filter(is_published=True)
        process_steps = ProcessStep.objects.filter(is_published=True)
        craft_details = CraftDetail.objects.filter(is_published=True)
        workshop_stats = WorkshopStat.objects.all()
        workshop_images = WorkshopImage.objects.all()
        return Response(
            {
                "settings": SiteSettingsSerializer(settings).data,
                "projects": ProjectSerializer(projects, many=True).data,
                "materials": MaterialSerializer(materials, many=True).data,
                "process_steps": ProcessStepSerializer(process_steps, many=True).data,
                "craft_details": CraftDetailSerializer(craft_details, many=True).data,
                "workshop_stats": WorkshopStatSerializer(workshop_stats, many=True).data,
                "workshop_images": WorkshopImageSerializer(
                    workshop_images, many=True
                ).data,
            }
        )
