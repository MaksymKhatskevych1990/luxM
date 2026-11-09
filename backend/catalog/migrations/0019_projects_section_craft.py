from django.db import migrations


def retitle_projects_section(apps, schema_editor):
    PageSection = apps.get_model("catalog", "PageSection")
    PageSection.objects.filter(key="projects").update(
        eyebrow="Майстерність",
        title="Збірка",
        title_line2="",
        title_emphasis="зблизька.",
        subtitle=(
            "Наведіть на фото — побачите руку збирача: "
            "зазори фасадів, фурнітуру і підгонку до стіни."
        ),
        cta_text="",
        cta_href="",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0018_remove_hero_window_zone"),
    ]

    operations = [
        migrations.RunPython(retitle_projects_section, migrations.RunPython.noop),
    ]
