from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,get_user_model
from student.models import*
from event_manager.models import*
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils import timezone


# Create your views here.

def home(request):
    today = timezone.now().date()
    events = Event.objects.filter(date__gte=today).order_by('date')
    return render(request,'common/home.html',{'e':events})


def login_users(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name="STUDENT").exists():
            return redirect('studenthome')
        elif request.user.groups.filter(name="EVENTMANAGER").exists():
            return redirect('manager_home')
        else:
            return redirect('adminhome')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:

            if user.groups.filter(name="STUDENT").exists():
                student = Student.objects.filter(user=user).first()

                if not student:
                    messages.error(request, "Student profile not found. Contact admin.")
                    return redirect('login_users')

                if student.status == "pending":
                    messages.error(request, "Your account is not approved yet!")
                    return redirect('login_users')

                login(request, user)
                return redirect('studenthome')

            elif user.groups.filter(name="EVENTMANAGER").exists():
                evmanager = EventManager.objects.filter(user=user).first()

                if not evmanager:
                    messages.error(request, "Event Manager profile not found. Contact admin.")
                    return redirect('login_users')

                if evmanager.status != "approved":
                    messages.error(request, "Your account is not approved yet!")
                    return redirect('login_users')

                login(request, user)
                return redirect('manager_home')

            else:
                login(request, user)
                return redirect('adminhome')

        else:
            messages.error(request, "User credentials are not correct")
            return redirect('login_users')

    return render(request, 'common/login.html')

def logoutuser(request):
     if request.user.is_authenticated:
           request.session.flush()
     return redirect('home')



def generate_token():
     return get_random_string(20)

def password_reset_request(request):
    if request.method == "POST":
         email = request.POST.get('email')
         try:
             user = User.objects.get(email=email)
         except User.DoesNotExist:
             messages.error(request, "User with this email does not exist.")
             return redirect('password_reset_request')

         token =default_token_generator.make_token(user)
         uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
         reset_url = request.build_absolute_uri(reverse('password_reset_confirm',kwargs={'uidb64':uidb64,'token':token}))
         subject = "Password Reset Request"
         message = render_to_string('common/password_reset_email.html', {
             'user': user,
             'reset_url': reset_url,
         })
         send_mail(subject, message,settings.DEFAULT_FROM_EMAIL, [user.email])
         messages.success(request, "A password reset link has been sent to your email.")
         return render(request,'common/password_reset_email.html')
    return render(request,'common/password_reset_form.html')
def password_reset_confirm(request, uidb64, token):
        User=get_user_model()
        try:
          uid = force_str(urlsafe_base64_decode(uidb64))
          user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None  
            print(user)
        if user is not None and default_token_generator.check_token(user,token):
             if request.method == 'POST':
                  password1=request.POST.get('password1')
                  password2=request.POST.get('password2')

                  if password1 == password2:
                      user.password = make_password(password1)
                      user.save()
                      messages.success(request,'your password has been reset')
                      return render(request,'common/password_reset_confirm.html')
                  else:
                      messages.error(request,'password do not match')
                      return render(request,'common/password_reset_form.html')
                          
             return render(request,'common/password_reset_confirm.html')
        else:
           return render(request,'common/password_reset_form.html')


def forgot_password_for_all(request):
    if request.method == 'POST':
        username = request.POST['username']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('forgot_password')

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password reset successful. Please login.")
            return redirect('login_users')
        except User.DoesNotExist:
            messages.error(request, "User not found")
            return redirect('forgot_password')

    return render(request, 'common/forgot_password.html')