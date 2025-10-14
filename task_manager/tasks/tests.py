from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from task_manager.statuses.models import Status
from .models import Task


User = get_user_model()


class TasksCrudTests(TestCase):
    def setUp(self):
        self.password = 'StrongPass123!'
        self.author = User.objects.create_user(
            username='author', password=self.password, first_name='A', last_name='User'
        )
        self.other = User.objects.create_user(
            username='other', password=self.password, first_name='O', last_name='User'
        )
        self.status = Status.objects.create(name='New')

    def test_list_requires_login(self):
        url = reverse('tasks_index')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse('login'), resp.url)
        self.client.login(username='author', password=self.password)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_create_requires_login(self):
        url = reverse('tasks_create')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.client.login(username='author', password=self.password)
        data = {
            'name': 'My Task',
            'description': 'Desc',
            'status': self.status.pk,
            'executor': self.other.pk,
        }
        resp = self.client.post(url, data)
        self.assertRedirects(resp, reverse('tasks_index'))
        self.assertTrue(Task.objects.filter(name='My Task', author=self.author).exists())

    def test_update_requires_login(self):
        task = Task.objects.create(
            name='Old', description='', status=self.status, author=self.author, executor=self.other
        )
        url = reverse('tasks_update', args=[task.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.client.login(username='other', password=self.password)
        resp = self.client.post(url, {
            'name': 'Updated',
            'description': 'Changed',
            'status': self.status.pk,
            'executor': self.other.pk,
        })
        self.assertRedirects(resp, reverse('tasks_index'))
        task.refresh_from_db()
        self.assertEqual(task.name, 'Updated')

    def test_delete_requires_author(self):
        task = Task.objects.create(
            name='To Delete', description='', status=self.status, author=self.author, executor=self.other
        )
        url = reverse('tasks_delete', args=[task.pk])
        # requires login
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        # logged in but not author -> should not delete
        self.client.login(username='other', password=self.password)
        resp = self.client.post(url)
        self.assertRedirects(resp, reverse('tasks_index'))
        self.assertTrue(Task.objects.filter(pk=task.pk).exists())
        # author can delete
        self.client.logout()
        self.client.login(username='author', password=self.password)
        resp = self.client.post(url)
        self.assertRedirects(resp, reverse('tasks_index'))
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())

    def test_show_requires_login(self):
        task = Task.objects.create(
            name='View Me', description='Look', status=self.status, author=self.author
        )
        url = reverse('tasks_show', args=[task.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.client.login(username='other', password=self.password)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_user_deletion_protected_when_linked_to_tasks(self):
        # author has a task, cannot delete self
        Task.objects.create(name='Linked', description='', status=self.status, author=self.author)
        self.client.login(username='author', password=self.password)
        url = reverse('users_delete', args=[self.author.pk])
        # GET delete page
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        # Attempt delete -> protected
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(User.objects.filter(pk=self.author.pk).exists())

