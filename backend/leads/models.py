from django.db import models


class Lead(models.Model):
    room_type = models.CharField(
        max_length=64,
        default="kitchen",
        verbose_name="Тип приміщення",
        help_text="Значення з моделі «Тип кімнати» (RoomType.value)",
    )
    message = models.TextField(blank=True, verbose_name="Повідомлення")
    name = models.CharField(max_length=120, verbose_name="Ім'я")
    phone = models.CharField(max_length=64, verbose_name="Телефон")
    email = models.EmailField(blank=True, verbose_name="Email")
    telegram = models.CharField(max_length=120, blank=True, verbose_name="Telegram")
    attachment = models.FileField(
        upload_to="leads/%Y/%m/",
        blank=True,
        null=True,
        verbose_name="Фото або план",
        help_text="Фото «до» або план приміщення (JPG, PNG, WEBP, PDF).",
    )
    is_processed = models.BooleanField(default=False, verbose_name="Опрацьовано")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def room_type_label(self) -> str:
        from catalog.models import RoomType

        room = RoomType.objects.filter(value=self.room_type).first()
        return room.label if room else self.room_type

    def __str__(self):
        return f"{self.name} — {self.room_type_label()}"
