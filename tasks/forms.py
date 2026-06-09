from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Task


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username",)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("title", "description", "due_date", "is_complete")
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_title(self):
        title = self.cleaned_data.get("title", "")
        title = title.strip()
        if not title:
            raise forms.ValidationError("Title cannot be empty or whitespace only.")
        return title
