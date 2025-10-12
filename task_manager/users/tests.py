from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()


class UsersCrudAuthTests(TestCase):
    def setUp(self):
        self.password = 'StrongPass123!'
        self.user1 = User.objects.create_user(
            username='user1', password=self.password, first_name='U', last_name='One'
        )
        self.user2 = User.objects.create_user(
            username='user2', password=self.password, first_name='U', last_name='Two'
        )

    def test_users_list_accessible(self):
        url = reverse('users_index')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'user1')
        self.assertContains(resp, 'user2')

    def test_registration_redirects_to_login(self):
        url = reverse('users_create')
        data = {
            'first_name': 'New',
            'last_name': 'User',
            'username': 'newuser',
            'password1': 'NewStrongPass123!',
            'password2': 'NewStrongPass123!',
        }
        resp = self.client.post(url, data)
        self.assertRedirects(resp, reverse('login'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_redirects_to_index(self):
        url = reverse('login')
        data = {'username': 'user1', 'password': self.password}
        resp = self.client.post(url, data)
        self.assertRedirects(resp, reverse('index'))

    def test_update_self_redirects(self):
        self.client.login(username='user1', password=self.password)
        url = reverse('users_update', args=[self.user1.pk])
        data = {
            'first_name': 'Updated',
            'last_name': 'One',
            'username': 'user1',
            'email': 'u1@example.com',
        }
        resp = self.client.post(url, data)
        self.assertRedirects(resp, reverse('users_index'))
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.first_name, 'Updated')

    def test_update_other_forbidden(self):
        self.client.login(username='user1', password=self.password)
        url = reverse('users_update', args=[self.user2.pk])
        resp = self.client.post(url, {'username': 'user2'})
        self.assertRedirects(resp, reverse('users_index'))

    def test_delete_self_redirects(self):
        self.client.login(username='user1', password=self.password)
        url = reverse('users_delete', args=[self.user1.pk])
        resp = self.client.post(url)
        self.assertRedirects(resp, reverse('users_index'))
        self.assertFalse(User.objects.filter(pk=self.user1.pk).exists())

    def test_delete_other_forbidden(self):
        self.client.login(username='user1', password=self.password)
        url = reverse('users_delete', args=[self.user2.pk])
        resp = self.client.post(url)
        self.assertRedirects(resp, reverse('users_index'))
        self.assertTrue(User.objects.filter(pk=self.user2.pk).exists())

