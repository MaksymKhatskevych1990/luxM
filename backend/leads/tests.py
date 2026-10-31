from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase

from catalog.models import RoomType

from .models import Lead


class LeadApiTests(APITestCase):
    def setUp(self):
        RoomType.objects.create(value="kitchen", label="Кухня", is_active=True)

    def _payload(self, **overrides):
        data = {
            "room_type": "kitchen",
            "name": "Іван",
            "phone": "+38 (097) 208 00 74",
            "message": "Кухня 3 метри",
        }
        data.update(overrides)
        return data

    def test_creates_lead_with_formatted_phone(self):
        response = self.client.post("/api/leads/", self._payload(), format="multipart")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Lead.objects.count(), 1)
        self.assertEqual(Lead.objects.get().phone, "+38 (097) 208 00 74")

    def test_rejects_short_phone(self):
        response = self.client.post(
            "/api/leads/",
            self._payload(phone="12345"),
            format="multipart",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Lead.objects.count(), 0)

    def test_honeypot_is_accepted_without_saving(self):
        response = self.client.post(
            "/api/leads/",
            self._payload(hp_field="https://spam.example"),
            format="multipart",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Lead.objects.count(), 0)

    def test_rejects_disallowed_attachment_extension(self):
        upload = SimpleUploadedFile(
            "plan.exe",
            b"not-a-photo",
            content_type="application/octet-stream",
        )
        response = self.client.post(
            "/api/leads/",
            self._payload(attachment=upload),
            format="multipart",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Lead.objects.count(), 0)
