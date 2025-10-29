from django import forms

from task_manager.labels.models import Label

from .models import Task


class TaskForm(forms.ModelForm):
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        required=False,
        label='Метки',
        widget=forms.SelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        executor_field = self.fields.get('executor')
        if executor_field:
            executor_field.label = 'Исполнитель'
            executor_field.label_from_instance = (
                lambda user: user.get_full_name() or user.username
            )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        labels = {
            'name': 'Имя',
            'description': 'Описание',
            'status': 'Статус',
            'executor': 'Исполнитель',
            'labels': 'Метки',
        }
