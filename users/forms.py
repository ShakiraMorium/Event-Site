from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, AuthenticationForm, PasswordChangeForm,
    PasswordResetForm, SetPasswordForm
)
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from users.models import CustomUser  

User = get_user_model()

# Sign Up Form
class CustomRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

# Login Form
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username', 'class': 'input input-bordered w-full'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password', 'class': 'input input-bordered w-full'
    }))

# Role Assignment Form
class AssignRoleForm(forms.Form):
    role = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label="Select a role")

# Group Creation Form
class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']

# Edit Profile Form
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'profile_image','phone']  

# Password Change Form
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input input-bordered w-full'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input input-bordered w-full'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input input-bordered w-full'}))

# Password Reset Form (Forgot Password)
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input input-bordered w-full'}))

# Set New Password (After Email Link)
class CustomPasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input input-bordered w-full'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input input-bordered w-full'}))
