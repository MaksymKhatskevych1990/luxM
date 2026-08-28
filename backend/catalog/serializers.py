from rest_framework import serializers

from .models import (
    CraftDetail,
    HeroStat,
    Material,
    NavItem,
    PageSection,
    ProcessStep,
    Project,
    ProjectImage,
    ProjectStage,
    RoomType,
    SiteSettings,
    WorkshopImage,
    WorkshopStat,
)


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        exclude = ("created_at", "updated_at")


class HeroStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroStat
        fields = ("id", "value", "label", "order")


class PageSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageSection
        fields = (
            "id",
            "key",
            "section_id",
            "eyebrow",
            "title",
            "title_line2",
            "title_emphasis",
            "subtitle",
            "cta_text",
            "cta_href",
            "is_visible",
            "order",
        )


class NavItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavItem
        fields = ("id", "label", "href", "location", "order", "is_visible")


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ("id", "value", "label", "order", "is_active")


class ProjectStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectStage
        fields = ("id", "title", "image_url", "order")


class ProjectImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = ProjectImage
        fields = ("id", "url", "caption", "order")

    def get_url(self, obj):
        url = obj.resolved_url
        if not url:
            return ""
        request = self.context.get("request")
        if url.startswith("http"):
            return url
        if request:
            return request.build_absolute_uri(url)
        return url


class ProjectSerializer(serializers.ModelSerializer):
    stages = ProjectStageSerializer(many=True, read_only=True)
    gallery = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    video_src = serializers.SerializerMethodField()
    video_poster = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = (
            "id",
            "title",
            "slug",
            "subtitle",
            "description",
            "short_description",
            "materials_label",
            "category",
            "year",
            "area",
            "duration",
            "location",
            "image_url",
            "detail_image_url",
            "video_src",
            "video_poster",
            "is_featured",
            "is_published",
            "show_in_detail_section",
            "order",
            "seo_title",
            "seo_description",
            "seo_keywords",
            "stages",
            "gallery",
        )

    def _abs(self, url: str) -> str:
        if not url:
            return ""
        if url.startswith("http"):
            return url
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(url)
        return url

    def get_image_url(self, obj):
        return self._abs(obj.cover_url)

    def get_video_src(self, obj):
        return self._abs(obj.resolved_video_url)

    def get_video_poster(self, obj):
        poster = obj.video_poster_url or obj.cover_url or obj.detail_image_url
        return self._abs(poster)

    def get_gallery(self, obj):
        images = obj.gallery.filter(is_published=True)
        return ProjectImageSerializer(images, many=True, context=self.context).data


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = (
            "id",
            "name_uk",
            "name_en",
            "description",
            "image_url",
            "order",
            "is_published",
        )


class ProcessStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessStep
        fields = (
            "id",
            "title",
            "description",
            "duration",
            "image_url",
            "order",
            "is_published",
        )


class CraftDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CraftDetail
        fields = ("id", "title", "image_url", "order", "is_published")


class WorkshopStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkshopStat
        fields = ("id", "value", "label", "order")


class WorkshopImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkshopImage
        fields = ("id", "title", "image_url", "order")
