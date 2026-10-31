from rest_framework import status
from rest_framework.exceptions import Throttled
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from .models import Lead
from .serializers import LeadSerializer
from .telegram import notify_telegram


class LeadAnonThrottle(AnonRateThrottle):
    scope = "leads"


class LeadCreateView(CreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    throttle_classes = [LeadAnonThrottle]

    def throttled(self, request, wait):
        raise Throttled(detail="Забагато запитів. Зателефонуйте або спробуйте трохи пізніше.")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if getattr(serializer, "spam_honeypot", False):
            return Response({"status": "accepted"}, status=status.HTTP_201_CREATED)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        lead = serializer.save()
        notify_telegram(lead)
