from django.contrib import admin
from .models import Note, Tag, SharedNoteAccess


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "is_pinned", "is_favorite", "is_shared", "created_at", "updated_at")
    list_filter = ("is_pinned", "is_favorite", "is_shared", "created_at")
    search_fields = ("title", "content", "owner__email")
    ordering = ("-is_pinned", "-updated_at")
    filter_horizontal = ("tags",)  # Better UI for ManyToMany fields


@admin.register(SharedNoteAccess)
class SharedNoteAccessAdmin(admin.ModelAdmin):
    list_display = ("note", "accessed_by", "accessed_at")
    list_filter = ("accessed_at",)
    search_fields = ("note__title", "accessed_by__email")
