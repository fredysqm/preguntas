from django.conf.urls import patterns, include, url

from rest_framework import routers
from .views import tag_viewset

router = routers.DefaultRouter()
router.register(r'tags', tag_viewset)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
)