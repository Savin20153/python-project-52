from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

from .models import Label

User = get_user_model()


class LabelsCrudTests(TestCase):
    def setUp(self):
        self.password = 'StrongPass123!'
        self.user = User.objects.create_user(
            username='user1',
            password=self.password,
            first_name='U',
            last_name='One',
        )

    def test_list_requires_login(self):
        url = reverse('labels_index')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse('login'), resp.url)
        self.client.login(username='user1', password=self.password)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_create_requires_login(self):
        url = reverse('labels_create')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.client.login(username='user1', password=self.password)
        data = {"name": "bug"}
        resp = self.client.post(url, data)
        self.assertRedirects(resp, reverse('labels_index'))
        self.assertTrue(Label.objects.filter(name='bug').exists())

    def test_update_requires_login(self):
        label = Label.objects.create(name='old')
        url = reverse('labels_update', args=[label.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.client.login(username='user1', password=self.password)
        resp = self.client.post(url, {"name": "new"})
        self.assertRedirects(resp, reverse('labels_index'))
        label.refresh_from_db()
        self.assertEqual(label.name, 'new')

    def test_delete_requires_login_and_block_if_in_use(self):
        status = Status.objects.create(name='New')
        label = Label.objects.create(name='feature')
        url = reverse('labels_delete', args=[label.pk])
        # Not logged in -> redirect
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        # Logged in and not in use -> delete ok
        self.client.login(username='user1', password=self.password)
        resp = self.client.post(url)
        self.assertRedirects(resp, reverse('labels_index'))
        self.assertFalse(Label.objects.filter(pk=label.pk).exists())
        # Create again and link to task -> deletion blocked
        label = Label.objects.create(name='feature')
        task = Task.objects.create(
            name='T',
            description='',
            status=status,
            author=self.user,
        )
        task.labels.add(label)
        url = reverse('labels_delete', args=[label.pk])
        resp = self.client.post(url)
        self.assertRedirects(resp, reverse('labels_index'))
        self.assertTrue(Label.objects.filter(pk=label.pk).exists())
