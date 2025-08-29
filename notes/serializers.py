from rest_framework import serializers
from .models import Note, Tag, SharedNoteAccess


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.email")
    # tags = serializers.PrimaryKeyRelatedField(
    #     queryset=Tag.objects.all(), many=True, required=False
    # )
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, write_only=True, required=False
    )

    class Meta:
        model = Note
        fields = [
            "id",
            "owner",
            "title",
            "content",
            "tags",
            "tag_ids",
            "is_pinned",
            "is_favorite",
            "is_shared",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def create(self, validated_data):
        tags = validated_data.pop("tags", [])
        note = Note.objects.create(**validated_data)
        if tags:
            note.tags.set(tags)
        return note

    def update(self, instance, validated_data):
        tags = validated_data.pop("tag_ids", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tags is not None:
            instance.tags.set(tags)
        return instance


class SharedNoteAccessSerializer(serializers.ModelSerializer):
    note = serializers.StringRelatedField()
    accessed_by = serializers.StringRelatedField()

    class Meta:
        model = SharedNoteAccess
        fields = ["id", "note", "accessed_by", "accessed_at"]
