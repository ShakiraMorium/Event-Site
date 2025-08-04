from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView,PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, FormView, UpdateView, ListView
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from users.forms import (
    CustomRegistrationForm, LoginForm, AssignRoleForm,
    CreateGroupForm, CustomPasswordChangeForm,
    CustomPasswordResetForm, CustomPasswordResetConfirmForm, EditProfileForm
)




User = get_user_model()

# Sign Up View
class SignUpView(FormView):
    template_name = 'users/sign_up.html'
    form_class = CustomRegistrationForm
    success_url = reverse_lazy('sign-in')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.is_active = False 
        user.save()
        messages.success(self.request, 'Account created. Please check your email to activate your account.')
        return super().form_valid(form)

# Custom Login View
class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    authentication_form = LoginForm
    
class SignOutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('login') 

# Activate User View
def activate_user(request, user_id, token):
    user = get_object_or_404(User, pk=user_id)
    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated. You can now log in.')
    else:
        messages.error(request, 'Activation link is invalid!')
    return redirect('sign-in')

# Admin Dashboard
class AdminDashboardView(TemplateView):
    template_name = 'users/admin_dashboard.html'

# Assign Role View
class AssignRoleView(View):
    def get(self, request, user_id):
        form = AssignRoleForm()
        return render(request, 'admin/assign_role.html', {'form': form})

    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            user.groups.clear()
            user.groups.add(role)
            messages.success(request, f"Assigned role '{role.name}' to user.")
            return redirect('admin-dashboard')
        return render(request, 'users/assign_role.html', {'form': form})

# Group Creation
class CreateGroupView(FormView):
    form_class = CreateGroupForm
    template_name = 'admin/create_group.html'
    success_url = reverse_lazy('users:group-list')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Group created successfully.")
        return super().form_valid(form)

# Group List
class GroupListView(ListView):
    template_name = 'admin/group_list.html'
    queryset = Group.objects.all()
    context_object_name = 'groups'

# Profile View
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['profile_image'] = user.profile_image  
        context['name'] = user.get_full_name()
        context['email'] = user.email
        context['username'] = user.username
        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login
        context['bio'] = "" 
        return context

    
    
# Edit Profile
class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/edit_profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user

# Change Password
class ChangePasswordReset(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('password_change_done')

# Reset Password
class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')

# Confirm Password Reset
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')
