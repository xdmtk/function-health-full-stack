from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "due_date", "is_complete", "created_at", "updated_at")
    list_filter = ("is_complete", "due_date")
    search_fields = ("title", "description", "user__username")
