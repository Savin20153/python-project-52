from django import forms
import django_filters
from django.utils.translation import gettext_lazy as _

from .models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.contrib.auth import get_user_model


User = get_user_model()


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(), label=_('Status')
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(), label=_('Executor')
    )
    # Primary (singular) label field as in the demo
    label = django_filters.ModelChoiceFilter(
        field_name='labels', queryset=Label.objects.all(), label=_('Labels')
    )
    # Backward-compatible alias if tests expect "labels"
    labels = django_filters.ModelChoiceFilter(
        field_name='labels', queryset=Label.objects.all(), label=_('Labels')
    )

    self_tasks = django_filters.BooleanFilter(
        method='filter_self_tasks', widget=forms.CheckboxInput, label=_('Only my tasks')
    )

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label', 'labels', 'self_tasks']

