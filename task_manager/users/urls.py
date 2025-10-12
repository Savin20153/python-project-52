from django.urls import path

from .views import (
    UsersListView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
)


urlpatterns = [
    path('', UsersListView.as_view(), name='users_index'),
    path('create/', UserCreateView.as_view(), name='users_create'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='users_update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='users_delete'),
]

