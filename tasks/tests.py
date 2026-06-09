from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskAccessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="password12345")
        self.other_user = User.objects.create_user(username="bob", password="password12345")
        self.task = Task.objects.create(user=self.user, title="Alice task")
        self.other_task = Task.objects.create(user=self.other_user, title="Bob task")

    def test_anonymous_users_cannot_access_task_pages(self):
        urls = [
            reverse("task_list"),
            reverse("task_create"),
            reverse("task_edit", args=[self.task.pk]),
            reverse("task_delete", args=[self.task.pk]),
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn(reverse("login"), response["Location"])

    def test_logged_in_user_can_create_valid_task(self):
        self.client.login(username="alice", password="password12345")

        response = self.client.post(
            reverse("task_create"),
            {
                "title": "  Buy milk  ",
                "description": "Two percent",
                "due_date": "2026-07-01",
                "is_complete": "",
            },
        )

        self.assertRedirects(response, reverse("task_list"))
        task = Task.objects.get(user=self.user, title="Buy milk")
        self.assertEqual(task.description, "Two percent")
        self.assertEqual(task.due_date, date(2026, 7, 1))
        self.assertFalse(task.is_complete)

    def test_empty_or_whitespace_only_title_is_rejected(self):
        self.client.login(username="alice", password="password12345")

        for title in ("", "   "):
            with self.subTest(title=repr(title)):
                response = self.client.post(reverse("task_create"), {"title": title})
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "Title cannot be empty", status_code=200)

        self.assertFalse(Task.objects.filter(user=self.user, title="").exists())

    def test_user_cannot_see_another_users_tasks_in_list(self):
        self.client.login(username="alice", password="password12345")

        response = self.client.get(reverse("task_list"))

        self.assertContains(response, "Alice task")
        self.assertNotContains(response, "Bob task")

    def test_user_cannot_edit_another_users_task_by_guessing_url(self):
        self.client.login(username="alice", password="password12345")

        response = self.client.post(
            reverse("task_edit", args=[self.other_task.pk]),
            {"title": "Hacked", "description": "Nope", "due_date": "", "is_complete": "on"},
        )

        self.assertEqual(response.status_code, 404)
        self.other_task.refresh_from_db()
        self.assertEqual(self.other_task.title, "Bob task")
        self.assertFalse(self.other_task.is_complete)

    def test_user_cannot_delete_another_users_task_by_guessing_url(self):
        self.client.login(username="alice", password="password12345")

        response = self.client.post(reverse("task_delete", args=[self.other_task.pk]))

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Task.objects.filter(pk=self.other_task.pk, user=self.other_user).exists())

    def test_editing_task_preserves_ownership_and_updates_expected_fields(self):
        self.client.login(username="alice", password="password12345")

        response = self.client.post(
            reverse("task_edit", args=[self.task.pk]),
            {
                "title": "Updated task",
                "description": "Updated description",
                "due_date": "2026-08-15",
                "is_complete": "on",
            },
        )

        self.assertRedirects(response, reverse("task_list"))
        self.task.refresh_from_db()
        self.assertEqual(self.task.user, self.user)
        self.assertEqual(self.task.title, "Updated task")
        self.assertEqual(self.task.description, "Updated description")
        self.assertEqual(self.task.due_date, date(2026, 8, 15))
        self.assertTrue(self.task.is_complete)
