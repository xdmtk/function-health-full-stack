from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import RegisterForm, TaskForm
from .models import Task


def home(request):
    if request.user.is_authenticated:
        return redirect("task_list")
    return redirect("login")


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("task_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Account created. You are now logged in.")
        return response


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Task created.")
        return super().form_valid(form)


class UserOwnedTaskMixin(LoginRequiredMixin):
    model = Task

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskUpdateView(UserOwnedTaskMixin, UpdateView):
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Task updated.")
        return super().form_valid(form)


class TaskDeleteView(UserOwnedTaskMixin, DeleteView):
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("task_list")

    def form_valid(self, form):
        messages.success(self.request, "Task deleted.")
        return super().form_valid(form)


class TaskToggleView(UserOwnedTaskMixin, View):
    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs["pk"], user=request.user)
        task.is_complete = not task.is_complete
        task.save(update_fields=["is_complete", "updated_at"])
        messages.success(request, "Task status updated.")
        return redirect("task_list")
