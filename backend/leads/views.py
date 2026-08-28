from rest_framework.generics import CreateAPIView

from .models import Lead
from .serializers import LeadSerializer


class LeadCreateView(CreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
