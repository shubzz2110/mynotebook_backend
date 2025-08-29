from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Note, Tag, SharedNoteAccess
from .serializers import NoteSerializer, TagSerializer, SharedNoteAccessSerializer
from rest_framework.pagination import LimitOffsetPagination
from django.db.models import Q


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission: only the note owner can edit/delete.
    Shared notes can be read by others if is_shared=True.
    """

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS = GET, HEAD, OPTIONS (read-only methods)
        if request.method in permissions.SAFE_METHODS:
            return obj.is_shared or obj.owner == request.user
        return obj.owner == request.user


class NotePagination(LimitOffsetPagination):
    default_limit = 9
    max_limit = 100


class NoteViewSet(viewsets.ModelViewSet):
    """
    Full CRUD API for Notes.
    /api/notes/ [GET, POST]
    /api/notes/{id}/ [GET, PUT, PATCH, DELETE]
    """
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = NotePagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "updated_at", "title"]
    filterset_fields = ["is_pinned", "is_favorite", "is_shared", "tags"]

    def get_queryset(self):
        # Users should only see their own notes, unless the note is shared
        return (
            Note.objects.filter(Q(owner=self.request.user) | Q(is_shared=True))
            .prefetch_related("tags")
        )

    def perform_create(self, serializer):
        # Attach the logged-in user as the note owner
        serializer.save(owner=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    """
    CRUD API for Tags.
    /api/tags/ [GET, POST]
    /api/tags/{id}/ [PUT, PATCH, DELETE]
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None


class SharedNoteAccessViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API for tracking shared note access (analytics).
    /api/shared-access/
    """
    queryset = SharedNoteAccess.objects.all()
    serializer_class = SharedNoteAccessSerializer
    permission_classes = [permissions.IsAdminUser]  # only admins can see this
