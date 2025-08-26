from django.urls import path
from .views import create_user, update_user, user_list, delete_user, career_list, create_career, club_list, create_club, delete_career, delete_club, update_carrer_modal, update_club_modal

urlpatterns = [
    path('', user_list, name='user_list'),
    path('create/', create_user, name='create_user'),
    path('update_user/<int:user_id>/', update_user, name='update_user'),
    path('user/<int:user_id>/delete/', delete_user, name='delete_user'),

    path('careers/', career_list, name='career_list'),
    path('create_career/', create_career, name='create_career'),
    path('delete_career/<int:career_id>/', delete_career, name='delete_career'),
    path('update_career/<int:career_id>/', update_carrer_modal, name='update_career'),

    path('clubs/', club_list, name='clubs_list'),
    path('create_club/', create_club, name='create_club'),
    path('delete_club/<int:club_id>/', delete_club, name='delete_club'),
    path('update_club/<int:club_id>/', update_club_modal, name='update_club'),
]