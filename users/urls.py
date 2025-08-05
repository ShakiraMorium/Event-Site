from django.urls import path
from . import views
from users.views import (
    SignUpView, CustomLoginView, SignOutView, activate_user,
    AdminDashboardView, AssignRoleView, CreateGroupView,
    GroupListView, ProfileView, EditProfileView,
    ChangePasswordReset, CustomPasswordResetView,
    CustomPasswordResetConfirmView,
)
app_name = 'users'
urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('sign-in/', CustomLoginView.as_view(), name='sign-in'),
    path('sign-out/', SignOutView.as_view(), name='sign-out'),

    # Account activation URL with user_id and token parameters
    path('activate/<int:user_id>/<str:token>/', activate_user, name='activate-user'),

    # Admin dashboard and management URLs
    path('dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('assign-role/<int:user_id>/', AssignRoleView.as_view(), name='assign-role'),
    path('create-group/', CreateGroupView.as_view(), name='create-group'),
    path('group-list/', GroupListView.as_view(), name='group-list'),

    # User profile URLs
    path('profile/', ProfileView.as_view(), name='profile'),
    path('edit-profile/', EditProfileView.as_view(), name='edit_profile'),

    # Password management
    path('password/change/', ChangePasswordReset.as_view(), name='password_change'),
    path('password/reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password/reset/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
