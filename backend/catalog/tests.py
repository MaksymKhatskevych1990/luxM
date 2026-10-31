from django.test import TestCase

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
