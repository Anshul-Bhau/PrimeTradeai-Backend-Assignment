from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.

    Validation:
        - title must be at least 3 characters after stripping whitespace.

    Read-only fields: id, created_at, updated_at, owner_email.
    """
    owner_email = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'status', 'owner_email', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at', 'owner_email')

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError('Title must be at least 3 characters.')
        return value.strip()