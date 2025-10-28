from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Label
from .forms import LabelForm


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/index.html'
    context_object_name = 'labels'


class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels_index')

    def form_valid(self, form):
        messages.success(self.request, _("Метка успешно создана"))
        return super().form_valid(form)


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels_index')

    def form_valid(self, form):
        messages.success(self.request, _("Метка успешно изменена"))
        return super().form_valid(form)


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels_index')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if hasattr(self.object, 'tasks') and self.object.tasks.exists():
            messages.error(self.request, _("Невозможно удалить метку, потому что она используется"))
            return HttpResponseRedirect(self.success_url)
        response = super().post(request, *args, **kwargs)
        messages.success(request, _("Метка успешно удалена"))
        return response
