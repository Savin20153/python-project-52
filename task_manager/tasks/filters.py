from django import forms
import django_filters

from .models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.contrib.auth import get_user_model


User = get_user_model()


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(), label='Статус'
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(), label='Исполнитель'
    )
    # Единственное поле выбора метки, отображается в форме
    label = django_filters.ModelChoiceFilter(
        field_name='labels', queryset=Label.objects.all(), label='Метка'
    )

    self_tasks = django_filters.BooleanFilter(
        method='filter_self_tasks',
        widget=forms.CheckboxInput,
        label='Только свои задачи',
    )

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        # Принимаем параметр labels как синоним label, но не дублируем поле в форме
        if data and 'labels' in data and 'label' not in data:
            data = data.copy()
            data['label'] = data.get('labels')
        super().__init__(data=data, queryset=queryset, request=request, prefix=prefix)

        executor_field = self.form.fields.get('executor')
        if executor_field:
            executor_field.label_from_instance = (
                lambda user: user.get_full_name() or user.username
            )

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label', 'self_tasks']
