from django.core.files.base import ContentFile
from django.forms import ModelForm

from catalog.image_sources import RemoteImageError, import_instagram_image
from catalog.models import WorkItem, WorkItemImage, normalize_image_reference


class InstagramImageFormMixin:
    """Save a pasted Instagram photo into the file field."""

    image_file_field = "image"

    def clean(self):
        cleaned = super().clean()
        url = cleaned.get("image_url") or ""
        if url:
            cleaned["image_url"] = normalize_image_reference(url)
            url = cleaned["image_url"]
        if self.errors or not url:
            return cleaned
        if self.files.get(self.add_prefix(self.image_file_field)):
            return cleaned
        try:
            imported = import_instagram_image(url)
        except RemoteImageError as exc:
            self.add_error("image_url", str(exc))
            return cleaned
        if imported:
            self._imported_image = imported
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        imported = getattr(self, "_imported_image", None)
        if imported:
            filename, content = imported
            getattr(instance, self.image_file_field).save(
                filename,
                ContentFile(content),
                save=False,
            )
            instance.image_url = ""
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class WorkItemAdminForm(InstagramImageFormMixin, ModelForm):
    image_file_field = "cover_image"

    class Meta:
        model = WorkItem
        fields = "__all__"


class WorkItemImageForm(InstagramImageFormMixin, ModelForm):
    image_file_field = "image"

    class Meta:
        model = WorkItemImage
        fields = "__all__"
