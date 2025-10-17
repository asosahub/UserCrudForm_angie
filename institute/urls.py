from django.urls import path
from .views import login, logout, dashboard, dashboard_admin, dashboard_estudiante, dashboard_invitado, create_user, update_user, user_list, delete_user, career_list, create_career, club_list, create_club, delete_career, delete_club, update_carrer_modal, update_club_modal, genshin_api_view, api_update_user, api_create_career
from .reports import all_users_pdf_report, career_users_report

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/admin', dashboard_admin, name='dashboard_admin'),
    path('dashboard/estudiante', dashboard_estudiante, name='dashboard_estudiante'),
    path('dashboard/invitado', dashboard_invitado, name='dashboard_invitado'),

    path('', login, name='login'),
    path('user_list', user_list, name='user_list'),
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

    path('reports/all_users_pdf/', all_users_pdf_report, name='all_users_pdf_report'),

    path('reports/career_users_pdf/', career_users_report, name='career_users_report'),

    path('genshin/', genshin_api_view, name="genshin_api"),

    path('api/update_user/<int:user_id>/', api_update_user, name='api_update_user'),
    path('api/create_career', api_create_career, name='api_create_career')
]