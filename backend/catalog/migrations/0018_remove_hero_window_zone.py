from django.db import migrations


def remove_window_zone(apps, schema_editor):
    HeroZone = apps.get_model("catalog", "HeroZone")
    HeroScene = apps.get_model("catalog", "HeroScene")
    HeroZone.objects.filter(name__iregex=r"^(вікно|окно)$").delete()
    HeroZone.objects.filter(tag__iregex=r"^(вікно|окно)$").delete()
    HeroScene.objects.filter(
        idle_body__icontains="саме вікно",
    ).update(
        idle_body=(
            "Стелаж, тумби, диван, стіл, крісло чи тумба — "
            "наведіть і побачите, що це за предмет."
        )
    )


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0017_work_image_site_paths"),
    ]

    operations = [
        migrations.RunPython(remove_window_zone, migrations.RunPython.noop),
    ]
