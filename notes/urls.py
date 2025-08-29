from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoteViewSet, TagViewSet, SharedNoteAccessViewSet

router = DefaultRouter()
router.register(r"notes", NoteViewSet, basename="note")
router.register(r"tags", TagViewSet, basename="tag")
router.register(r"shared-access", SharedNoteAccessViewSet, basename="shared-access")

urlpatterns = [
    path("", include(router.urls)),
]
