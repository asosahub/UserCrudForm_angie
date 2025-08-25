from django.urls import path
from .views import create_user, update_user, user_list, delete_user

urlpatterns = [
    path('', user_list, name='user_list'),
    path('create/', create_user, name='create_user'),
    path('update_user/<int:user_id>/', update_user, name='update_user'),
    path('user/<int:user_id>/delete/', delete_user, name='delete_user'),
]