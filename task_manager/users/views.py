from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import SignupForm, UserUpdateForm


User = get_user_model()


class UsersListView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'


class OnlySelfMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_authenticated and obj.pk == self.request.user.pk

    def handle_no_permission(self):
        messages.error(self.request, _("You do not have permission to modify another user."))
        return self.get_no_permission_redirect()

    def get_no_permission_redirect(self):
        from django.shortcuts import redirect

        return redirect('users_index')


class UserCreateView(CreateView):
    form_class = SignupForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, _("User registered successfully."))
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, OnlySelfMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users_index')

    def form_valid(self, form):
        messages.success(self.request, _("User updated successfully."))
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, OnlySelfMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users_index')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _("User deleted successfully."))
        return super().delete(request, *args, **kwargs)

