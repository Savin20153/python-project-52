from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Status


User = get_user_model()


class StatusesCrudAuthTests(TestCase):
    def setUp(self):
        self.password = 'StrongPass123!'
        self.user = User.objects.create_user(
            username='user1', password=self.password, first_name='U', last_name='One'
        )

    def test_list_requires_login(self):
        url = reverse('statuses_index')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse('login'), resp.url)

    def test_create_requires_login(self):
        url = reverse('statuses_create')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.client.login(username='user1', password=self.password)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = {"name": "New"}
        resp = self.client.post(url, data)
        self.assertRedirects(resp, reverse('statuses_index'))
        self.assertTrue(Status.objects.filter(name='New').exists())

    def test_update_requires_login(self):
        status = Status.objects.create(name='Old')
        url = reverse('statuses_update', args=[status.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.client.login(username='user1', password=self.password)
        resp = self.client.post(url, {"name": "Updated"})
        self.assertRedirects(resp, reverse('statuses_index'))
        status.refresh_from_db()
        self.assertEqual(status.name, 'Updated')

    def test_delete_requires_login(self):
        status = Status.objects.create(name='Temp')
        url = reverse('statuses_delete', args=[status.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.client.login(username='user1', password=self.password)
        resp = self.client.post(url)
        self.assertRedirects(resp, reverse('statuses_index'))
        self.assertFalse(Status.objects.filter(pk=status.pk).exists())

