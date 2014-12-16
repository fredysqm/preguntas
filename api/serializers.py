from rest_framework import serializers

from app.models import tag

class tag_serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = tag
        fields = ('nombre','slug',)