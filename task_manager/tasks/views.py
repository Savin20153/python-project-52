from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from .models import Task
from .forms import TaskForm


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/show.html'
    context_object_name = 'task'


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks_index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, _("Task created successfully."))
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks_index')

    def form_valid(self, form):
        messages.success(self.request, _("Task updated successfully."))
        return super().form_valid(form)


class OnlyAuthorDeleteMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_authenticated and obj.author_id == self.request.user.id

    def handle_no_permission(self):
        messages.error(self.request, _("You do not have permission to delete this task."))
        from django.shortcuts import redirect

        return redirect('tasks_index')


class TaskDeleteView(LoginRequiredMixin, OnlyAuthorDeleteMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks_index')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _("Task deleted successfully."))
        return super().delete(request, *args, **kwargs)

