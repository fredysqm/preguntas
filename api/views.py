from .serializers import tag_serializer
from rest_framework import viewsets
from app.models import tag

class tag_viewset(viewsets.ModelViewSet):
    queryset = tag.objects.all()
    serializer_class = tag_serializer