from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("leads", "0002_alter_lead_created_at_alter_lead_email_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="lead",
            name="attachment",
            field=models.FileField(
                blank=True,
                help_text="Фото «до» або план приміщення (JPG, PNG, WEBP, PDF).",
                null=True,
                upload_to="leads/%Y/%m/",
                verbose_name="Фото або план",
            ),
        ),
    ]
