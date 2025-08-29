from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.


class Tag(models.Model):
    """Tags for categorizing notes (e.g. work, personal, etc)"""
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Note(models.Model):
    """Main Note Model"""
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='notes')

    # Flags
    is_pinned = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)
    is_shared = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_pinned', '-updated_at']
        indexes = [
            models.Index(fields=["owner", "is_shared"]),
            models.Index(fields=["is_pinned"]),
            models.Index(fields=["is_favorite"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
            models.Index(fields=["title"]),
        ]

    def __str__(self):
        return f"{self.title} (by {self.owner.email})"


class SharedNoteAccess(models.Model):
    """
    Optional: Track who accessed a shared note (if you want analytics later).
    """
    note = models.ForeignKey(
        Note, on_delete=models.CASCADE, related_name='shared_access')
    accessed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    accessed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.accessed_by} accessed {self.note.title}"
