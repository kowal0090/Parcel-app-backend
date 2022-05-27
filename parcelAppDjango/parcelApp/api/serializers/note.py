from rest_framework import serializers
from api.models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'title', "content", "created_at", "updated_at", "content_type")