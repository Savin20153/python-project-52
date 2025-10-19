from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import update_session_auth_hash
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
        messages.error(self.request, _("У вас нет прав для изменения другого пользователя"))
        return self.get_no_permission_redirect()

    def get_no_permission_redirect(self):
        from django.shortcuts import redirect

        return redirect('users_index')


class UserCreateView(CreateView):
    form_class = SignupForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, _("Пользователь успешно зарегистрирован"))
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, OnlySelfMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users_index')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Смена пароля, если введён
        password = form.cleaned_data.get("password1")
        if password:
            self.object.set_password(password)
            self.object.save(update_fields=["password"])
            update_session_auth_hash(self.request, self.object)
        messages.success(self.request, _("Пользователь успешно изменён"))
        return response


class UserDeleteView(LoginRequiredMixin, OnlySelfMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users_index')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            response = super().post(request, *args, **kwargs)
            messages.success(self.request, _("Пользователь успешно удалён"))
            return response
        except ProtectedError:
            messages.error(self.request, _("Невозможно удалить пользователя, потому что он используется"))
            return self.get(request, *args, **kwargs)
