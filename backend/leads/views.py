from rest_framework.generics import CreateAPIView

from .models import Lead
from .serializers import LeadSerializer
from .telegram import notify_telegram


class LeadCreateView(CreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

    def perform_create(self, serializer):
        lead = serializer.save()
        notify_telegram(lead)
