from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0013_alter_sitesettings_jsonld_area_served_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sitesettings",
            name="email",
            field=models.EmailField(
                blank=True, default="", max_length=254, verbose_name="Email"
            ),
        ),
    ]
