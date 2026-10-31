from django.db import migrations


def point_at_work_pages(apps, schema_editor):
    NavItem = apps.get_model("catalog", "NavItem")
    PageSection = apps.get_model("catalog", "PageSection")
    NavItem.objects.filter(href="#gallery").update(href="/works")
    PageSection.objects.filter(cta_href="#gallery").update(cta_href="/works")
    WorkCategory = apps.get_model("catalog", "WorkCategory")
    for category in WorkCategory.objects.all():
        if "Відкрийте картку" in (category.description or ""):
            category.description = category.description.replace(
                "Відкрийте картку — там кілька фото",
                "На сторінці варіанту — кілька фото",
            )
            category.save(update_fields=["description"])


def point_at_gallery_anchor(apps, schema_editor):
    NavItem = apps.get_model("catalog", "NavItem")
    PageSection = apps.get_model("catalog", "PageSection")
    NavItem.objects.filter(href="/works").update(href="#gallery")
    PageSection.objects.filter(cta_href="/works").update(cta_href="#gallery")


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0015_work_gallery"),
    ]

    operations = [
        migrations.RunPython(point_at_work_pages, point_at_gallery_anchor),
    ]
