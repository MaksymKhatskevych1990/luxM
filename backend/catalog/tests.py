import io
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms import modelform_factory
from django.test import TestCase
from PIL import Image

from catalog.forms import WorkItemAdminForm, WorkItemImageForm
from catalog.image_sources import RemoteImageError, fetch_remote_image, import_instagram_image
from catalog.models import WorkCategory, WorkItem, WorkItemImage


class WorkGalleryApiTests(TestCase):
    def setUp(self):
        WorkCategory.objects.all().delete()

    def test_home_returns_published_items_inside_categories(self):
        kitchens = WorkCategory.objects.create(
            name="Кухні",
            slug="kitchens",
            description="Варіанти кухонь",
            order=1,
            is_published=True,
        )
        hidden_category = WorkCategory.objects.create(
            name="Чернетка",
            slug="draft",
            order=9,
            is_published=False,
        )
        corner = WorkItem.objects.create(
            category=kitchens,
            title="Кутова",
            slug="kutova",
            summary="Горіх і камінь",
            description="Тонкощі кутової кухні",
            order=1,
            is_published=True,
        )
        WorkItemImage.objects.create(
            item=corner,
            image_url="/works/2024-10-08-a.jpg",
            caption="Фасад",
            order=1,
            is_published=True,
        )
        WorkItemImage.objects.create(
            item=corner,
            image_url="/works/hidden.jpg",
            caption="Приховано",
            order=2,
            is_published=False,
        )
        WorkItem.objects.create(
            category=kitchens,
            title="Не показувати",
            slug="hidden-item",
            is_published=False,
        )
        WorkItem.objects.create(
            category=hidden_category,
            title="Чужий",
            slug="foreign",
            is_published=True,
        )

        response = self.client.get("/api/home/")
        self.assertEqual(response.status_code, 200)
        categories = response.json()["work_categories"]
        self.assertEqual([item["slug"] for item in categories], ["kitchens"])
        items = categories[0]["items"]
        self.assertEqual([item["slug"] for item in items], ["kutova"])
        self.assertEqual(items[0]["description"], "Тонкощі кутової кухні")
        self.assertEqual(items[0]["image_url"], "/works/2024-10-08-a.jpg")
        self.assertEqual(
            [(photo["url"], photo["caption"]) for photo in items[0]["gallery"]],
            [("/works/2024-10-08-a.jpg", "Фасад")],
        )

        listed = self.client.get("/api/work-categories/")
        self.assertEqual(listed.status_code, 200)
        self.assertEqual(listed.json()[0]["slug"], "kitchens")

        detail = self.client.get("/api/work-categories/kitchens/")
        self.assertEqual(detail.status_code, 200)
        self.assertEqual(detail.json()["items"][0]["category_name"], "Кухні")

    def test_cover_form_accepts_site_path_and_file(self):
        category = WorkCategory.objects.create(name="Кухні", slug="kitchens")
        CoverForm = modelform_factory(
            WorkItem,
            fields=["category", "title", "slug", "image_url", "cover_image"],
        )
        buffer = io.BytesIO()
        Image.new("RGB", (2, 2), color="white").save(buffer, format="PNG")
        upload = SimpleUploadedFile("cover.png", buffer.getvalue(), content_type="image/png")
        form = CoverForm(
            data={
                "category": category.pk,
                "title": "Кутова",
                "slug": "kutova",
                "image_url": "/works/2024-10-08-a.jpg",
            },
            files={"cover_image": upload},
        )
        self.assertTrue(form.is_valid(), form.errors)
        saved = form.save()
        self.assertEqual(saved.image_url, "/works/2024-10-08-a.jpg")
        self.assertIn("works/kutova/cover/cover", saved.cover_image.name)
        self.assertTrue(saved.cover_image.name.endswith(".png"))

        rejected = CoverForm(
            data={
                "category": category.pk,
                "title": "Кутова",
                "slug": "kutova-2",
                "image_url": "not a url",
            }
        )
        self.assertFalse(rejected.is_valid())
        self.assertIn("image_url", rejected.errors)

        PhotoForm = modelform_factory(WorkItemImage, fields=["image_url"])
        photo = PhotoForm(data={"image_url": "/works/before/before-walnut-kitchen.jpg"})
        self.assertTrue(photo.is_valid(), photo.errors)

    def test_three_photo_sources(self):
        category = WorkCategory.objects.create(name="Кухні", slug="kitchens")
        jpeg = _jpeg_bytes()

        with patch(
            "catalog.forms.import_instagram_image",
            return_value=("instagram-AbC123.jpg", jpeg),
        ) as imported:
            form = WorkItemAdminForm(
                data={
                    "category": category.pk,
                    "title": "З Instagram",
                    "slug": "z-instagram",
                    "image_url": "instagram.com/p/AbC123/",
                    "order": 0,
                    "is_published": True,
                }
            )
            self.assertTrue(form.is_valid(), form.errors)
            saved = form.save()
        imported.assert_called_once_with("https://instagram.com/p/AbC123/")
        self.assertEqual(saved.image_url, "")
        self.assertIn("instagram-AbC123", saved.cover_image.name)
        self.assertTrue(saved.cover_image.name.endswith(".jpg"))
        self.assertTrue(saved.cover_url)

        plain = WorkItemAdminForm(
            data={
                "category": category.pk,
                "title": "За адресою",
                "slug": "za-adresoiu",
                "image_url": "https://images.example.com/kitchen.jpg",
                "order": 0,
                "is_published": True,
            }
        )
        self.assertTrue(plain.is_valid(), plain.errors)
        by_url = plain.save()
        self.assertEqual(by_url.image_url, "https://images.example.com/kitchen.jpg")
        self.assertFalse(by_url.cover_image)

        upload = SimpleUploadedFile("local.png", _png_bytes(), content_type="image/png")
        with patch("catalog.forms.import_instagram_image") as skipped:
            local = WorkItemAdminForm(
                data={
                    "category": category.pk,
                    "title": "З комп'ютера",
                    "slug": "z-kompiutera",
                    "image_url": "https://www.instagram.com/p/AbC123/",
                    "order": 0,
                    "is_published": True,
                },
                files={"cover_image": upload},
            )
            self.assertTrue(local.is_valid(), local.errors)
            local.save()
        skipped.assert_not_called()

        profile = WorkItemAdminForm(
            data={
                "category": category.pk,
                "title": "Профіль",
                "slug": "profil",
                "image_url": "https://www.instagram.com/proprostir/",
                "order": 0,
                "is_published": True,
            }
        )
        self.assertFalse(profile.is_valid())
        self.assertIn("image_url", profile.errors)

        item = WorkItem.objects.create(category=category, title="Галерея", slug="halereia")
        with patch(
            "catalog.forms.import_instagram_image",
            return_value=("instagram-reel.jpg", jpeg),
        ):
            gallery = WorkItemImageForm(
                data={
                    "item": item.pk,
                    "image_url": "https://www.instagram.com/reel/ZyX987/",
                    "caption": "Ріл",
                    "order": 1,
                    "is_published": True,
                }
            )
            self.assertTrue(gallery.is_valid(), gallery.errors)
            photo = gallery.save()
        self.assertEqual(photo.image_url, "")
        self.assertIn("instagram-reel", photo.image.name)
        self.assertTrue(photo.image.name.endswith(".jpg"))

    def test_instagram_fetch_accepts_only_instagram_images(self):
        with self.assertRaises(RemoteImageError):
            fetch_remote_image("http://127.0.0.1/secret.jpg", allow_page=False)

        class Opener:
            def open(self, request, timeout=0):
                class Response:
                    headers = {"Content-Type": "image/jpeg"}

                    def geturl(self):
                        return "https://scontent-a.cdninstagram.com/v/a.jpg"

                    def read(self, n=-1):
                        return _jpeg_bytes()

                    def __enter__(self):
                        return self

                    def __exit__(self, *args):
                        return False

                return Response()

        extension, data = fetch_remote_image(
            "https://www.instagram.com/p/AbC123/media/?size=l",
            allow_page=True,
            opener=Opener(),
        )
        self.assertEqual(extension, "jpg")
        self.assertTrue(data.startswith(b"\xff\xd8"))
        self.assertIsNone(import_instagram_image("https://images.example.com/kitchen.jpg"))
        self.assertIsNone(import_instagram_image("/works/2024-10-08-a.jpg"))


def _jpeg_bytes() -> bytes:
    buffer = io.BytesIO()
    Image.new("RGB", (2, 2), color="white").save(buffer, format="JPEG")
    return buffer.getvalue()


def _png_bytes() -> bytes:
    buffer = io.BytesIO()
    Image.new("RGB", (2, 2), color="white").save(buffer, format="PNG")
    return buffer.getvalue()
