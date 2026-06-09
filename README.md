# Task Manager

A small Django task management app built for a scoped take-home exercise. It is optimized for complete end-to-end task CRUD, authentication, ownership enforcement, validation, and a simple reviewer-friendly setup.

This is not production-ready. It intentionally keeps the architecture boring and direct.

## What it does

Authenticated users can manage their own tasks. Each task has a title, optional description, optional due date, completion status, and timestamps.

Users can:

- Register, log in, and log out
- View only their own task list
- Create tasks
- Edit tasks
- Delete tasks after a confirmation page
- Mark tasks complete or incomplete from the list

Ownership is enforced in the Django views, so guessing another user's edit/delete/toggle URL returns a 404 instead of exposing or changing that task.

## Tech stack

- Python 3
- Django
- Django templates
- Django built-in auth
- Django forms / ModelForms
- SQLite for local development
- Django `TestCase`

## Setup from a fresh clone

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run migrations

```bash
python manage.py migrate
```

## Create a user and run the app

You can register through the browser at `/accounts/register/`, or create an admin user:

```bash
python manage.py createsuperuser
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

Unauthenticated users are redirected to login. Authenticated users are redirected to their task list.

## Run tests

```bash
python manage.py test
```

## Features complete

- Registration, login, and POST-based logout using Django auth
- Per-user task CRUD with database persistence through SQLite
- Ownership filtering on list pages
- Ownership enforcement on edit, delete, and toggle actions
- Required title validation, including whitespace-only rejection
- Optional due date handled as a `DateField`
- User-visible form errors in templates
- Success messages for create, edit, delete, toggle, and registration
- Focused tests for authentication, validation, ownership isolation, and editing behavior

## Deliberately left out

- React, DRF, API endpoints, Docker, CI/CD, service layers, repository layers, and background jobs. They are unnecessary for this scope.
- Production settings, deployment configuration, password reset email, and advanced account management. The goal here is a local reviewer-friendly CRUD app, not a production system.
- Pagination and search. They would be straightforward additions, but they are not needed for a small take-home implementation.

## What I would improve with another day

- Add pagination and simple filtering for complete/incomplete tasks.
- Improve styling while keeping templates server-rendered.
- Add password reset and email configuration for a more complete auth flow.
- Add more tests around registration, toggle behavior, and due-date form rendering.
- Split settings for local/test/production if this were moving beyond the take-home scope.
