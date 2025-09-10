from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=200)
    duration = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.duration}s)"
