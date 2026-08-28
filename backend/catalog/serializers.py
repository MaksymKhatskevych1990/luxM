from rest_framework import serializers

from .models import (
    CraftDetail,
    Material,
    ProcessStep,
    Project,
    ProjectStage,
    SiteSettings,
    WorkshopImage,
    WorkshopStat,
)


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = (
            "id",
            "brand_name",
            "tagline",
            "founded_year",
            "phone",
            "email",
            "telegram",
            "address",
            "instagram_url",
            "telegram_url",
            "seo_title",
            "seo_description",
            "seo_keywords",
            "stats_projects",
            "stats_years",
            "stats_masters",
            "stats_production",
            "workshop_quote",
            "workshop_author",
            "workshop_text",
            "before_image_url",
            "after_image_url",
        )


class ProjectStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectStage
        fields = ("id", "title", "image_url", "order")


class ProjectSerializer(serializers.ModelSerializer):
    stages = ProjectStageSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = (
            "id",
            "title",
            "slug",
            "subtitle",
            "description",
            "materials_label",
            "category",
            "year",
            "area",
            "duration",
            "location",
            "image_url",
            "detail_image_url",
            "is_featured",
            "is_published",
            "order",
            "seo_title",
            "seo_description",
            "stages",
        )


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
