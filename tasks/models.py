from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(blank=True, null=True)
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["is_complete", "due_date", "-created_at"]

    def clean(self):
        super().clean()
        if not self.title or not self.title.strip():
            raise ValidationError({"title": "Title cannot be empty or whitespace only."})
        self.title = self.title.strip()

    def __str__(self):
        return self.title
