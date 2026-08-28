from django.db import models


class Lead(models.Model):
    ROOM_CHOICES = [
        ("kitchen", "Кухня"),
        ("wardrobe", "Гардеробна"),
        ("living", "Вітальня"),
        ("bedroom", "Спальня"),
        ("other", "Інше"),
    ]

    room_type = models.CharField(max_length=32, choices=ROOM_CHOICES, default="kitchen")
    message = models.TextField(blank=True)
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=64)
    email = models.EmailField(blank=True)
    telegram = models.CharField(max_length=120, blank=True)
    is_processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return f"{self.name} — {self.get_room_type_display()}"
