from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from users.forms import CustomRegistrationForm  

User = get_user_model()

class UserRegisterView(CreateView):
    model = User
    form_class = CustomRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)  # save user
        user = self.object

        # Assign user role
        user_group, _ = Group.objects.get_or_create(name='User')
        user.groups.add(user_group)
        user.save()

        # Send activation email
        token = default_token_generator.make_token(user)
        activation_url = f"{settings.FRONTEND_URL}/users/activate/{user.id}/{token}/"
        subject = 'Activate Your Account'
        message = f'Hi {user.username},\n\nPlease activate your account by clicking the link below:\n{activation_url}\n\nThank You!'
        recipient_list = [user.email]
        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
        except Exception as e:
            print(f"Failed to send email to {user.email}: {str(e)}")

        return response
