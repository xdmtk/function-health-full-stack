from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from tasks.views import (
    RegisterView,
    TaskCreateView,
    TaskDeleteView,
    TaskListView,
    TaskToggleView,
    TaskUpdateView,
    home,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("accounts/register/", RegisterView.as_view(), name="register"),
    path("accounts/login/", LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
    path("tasks/", TaskListView.as_view(), name="task_list"),
    path("tasks/new/", TaskCreateView.as_view(), name="task_create"),
    path("tasks/<int:pk>/edit/", TaskUpdateView.as_view(), name="task_edit"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task_delete"),
    path("tasks/<int:pk>/toggle/", TaskToggleView.as_view(), name="task_toggle"),
]
