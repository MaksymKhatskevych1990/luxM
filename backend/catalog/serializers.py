from rest_framework import serializers

from .models import (
    CraftDetail,
    HeroScene,
    HeroStat,
    HeroZone,
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


def public_media_url(url: str) -> str:
    """Keep same-origin /media paths so Next/ngrok can proxy files."""
    if not url:
        return ""
    if url.startswith("http://") or url.startswith("https://"):
        return url
    return url


class SiteSettingsSerializer(serializers.ModelSerializer):
    whatsapp_url = serializers.SerializerMethodField()
    telegram_url = serializers.SerializerMethodField()
    header_logo_url = serializers.SerializerMethodField()
    hero_background_image_url = serializers.SerializerMethodField()
    hero_floorplan_image_url = serializers.SerializerMethodField()
    og_image_url = serializers.SerializerMethodField()
    drawing_sketch_image_url = serializers.SerializerMethodField()
    before_image_url = serializers.SerializerMethodField()
    after_image_url = serializers.SerializerMethodField()

    class Meta:
        model = SiteSettings
        exclude = (
            "created_at",
            "telegram_bot_token",
            "telegram_notify_chat_id",
            "telegram_notify_enabled",
            "header_logo",
            "hero_background",
            "hero_floorplan_image",
            "og_image",
            "drawing_sketch",
            "before_image",
            "after_image",
        )

    def get_whatsapp_url(self, obj: SiteSettings) -> str:
        return obj.resolved_whatsapp_url

    def get_telegram_url(self, obj: SiteSettings) -> str:
        return obj.resolved_telegram_url

    def get_header_logo_url(self, obj: SiteSettings) -> str:
        return public_media_url(obj.resolved_logo_url)

    def get_hero_background_image_url(self, obj: SiteSettings) -> str:
        return public_media_url(obj.resolved_hero_background_url)

    def get_hero_floorplan_image_url(self, obj: SiteSettings) -> str:
        return public_media_url(obj.resolved_hero_floorplan_url)

    def get_og_image_url(self, obj: SiteSettings) -> str:
        return public_media_url(obj.resolved_og_image_url)

    def get_drawing_sketch_image_url(self, obj: SiteSettings) -> str:
        return public_media_url(obj.resolved_drawing_sketch_url)

    def get_before_image_url(self, obj: SiteSettings) -> str:
        return public_media_url(obj.resolved_before_image_url)

    def get_after_image_url(self, obj: SiteSettings) -> str:
        return public_media_url(obj.resolved_after_image_url)


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
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProjectStage
        fields = ("id", "title", "image_url", "order")

    def get_image_url(self, obj: ProjectStage):
        return public_media_url(obj.resolved_image_url)


class ProjectImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = ProjectImage
        fields = ("id", "url", "caption", "order")

    def get_url(self, obj):
        return public_media_url(obj.resolved_url)


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
        return public_media_url(url)

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
    image_url = serializers.SerializerMethodField()

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

    def get_image_url(self, obj: Material):
        return public_media_url(obj.resolved_image_url)


class ProcessStepSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

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

    def get_image_url(self, obj: ProcessStep):
        return public_media_url(obj.resolved_image_url)


class CraftDetailSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = CraftDetail
        fields = ("id", "title", "image_url", "order", "is_published")

    def get_image_url(self, obj: CraftDetail):
        return public_media_url(obj.resolved_image_url)


class WorkshopStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkshopStat
        fields = ("id", "value", "label", "order")


class WorkshopImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = WorkshopImage
        fields = ("id", "title", "image_url", "order")

    def get_image_url(self, obj: WorkshopImage):
        return public_media_url(obj.resolved_image_url)


class HeroZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroZone
        fields = (
            "id",
            "name",
            "service",
            "materials",
            "tag",
            "x",
            "y",
            "width",
            "height",
            "order",
        )


class HeroSceneSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    zones = serializers.SerializerMethodField()

    class Meta:
        model = HeroScene
        fields = (
            "id",
            "title",
            "image_url",
            "hint",
            "idle_eyebrow",
            "idle_title",
            "idle_body",
            "zones",
        )

    def get_image_url(self, obj: HeroScene) -> str:
        return public_media_url(obj.resolved_image_url)

    def get_zones(self, obj: HeroScene):
        zones = obj.zones.filter(is_published=True)
        return HeroZoneSerializer(zones, many=True).data
