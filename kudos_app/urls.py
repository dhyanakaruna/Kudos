from django.urls import path
from . import views

urlpatterns = [
    # User endpoints
    path('users/me/', views.current_user, name='current-user'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('organizations/', views.organizations_list, name='organizations-list'),
    path('organizations/<int:org_id>/users/', views.users_by_organization, name='users-by-organization'),
    
    # Kudo endpoints
    path('kudos/', views.KudoCreateView.as_view(), name='kudo-create'),
    path('kudos/received/', views.KudosReceivedView.as_view(), name='kudos-received'),
]
