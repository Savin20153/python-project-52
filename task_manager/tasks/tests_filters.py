from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from .models import Task


User = get_user_model()


class TaskFilterTests(TestCase):
    def setUp(self):
        self.password = 'StrongPass123!'
        self.author = User.objects.create_user(username='author', password=self.password)
        self.other = User.objects.create_user(username='other', password=self.password)
        self.status_new = Status.objects.create(name='New')
        self.status_done = Status.objects.create(name='Done')
        self.label_bug = Label.objects.create(name='bug')
        self.label_ui = Label.objects.create(name='ui')

        self.task1 = Task.objects.create(
            name='T1', description='', status=self.status_new, author=self.author, executor=self.other
        )
        self.task1.labels.add(self.label_bug)

        self.task2 = Task.objects.create(
            name='T2', description='', status=self.status_done, author=self.other, executor=self.author
        )
        self.task2.labels.add(self.label_ui)

        self.url = reverse('tasks_index')

    def login(self):
        self.client.login(username='author', password=self.password)

    def test_filter_by_status(self):
        self.login()
        resp = self.client.get(self.url, {'status': self.status_new.id})
        self.assertEqual(resp.status_code, 200)
        tasks = list(resp.context['tasks'])
        self.assertEqual([t.name for t in tasks], ['T1'])

    def test_filter_by_executor(self):
        self.login()
        resp = self.client.get(self.url, {'executor': self.other.id})
        self.assertEqual(resp.status_code, 200)
        tasks = list(resp.context['tasks'])
        self.assertEqual([t.name for t in tasks], ['T1'])

    def test_filter_by_label(self):
        self.login()
        # accept both 'label' and 'labels'
        for key in ('label', 'labels'):
            resp = self.client.get(self.url, {key: self.label_ui.id})
            self.assertEqual(resp.status_code, 200)
            tasks = list(resp.context['tasks'])
            self.assertEqual([t.name for t in tasks], ['T2'])

    def test_filter_only_my_tasks(self):
        self.login()
        resp = self.client.get(self.url, {'self_tasks': 'on'})
        self.assertEqual(resp.status_code, 200)
        tasks = list(resp.context['tasks'])
        self.assertEqual({t.name for t in tasks}, {'T1'})

