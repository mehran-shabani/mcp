from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "name", "duration", "created_at"]

    def validate_duration(self, value: float):
        if value < 0 or value > 3600:
            raise serializers.ValidationError("duration باید بین 0 تا 3600 باشد.")
        return value
