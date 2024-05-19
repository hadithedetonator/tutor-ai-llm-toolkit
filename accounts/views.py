from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.views.decorators.csrf import csrf_protect

def register_view(request):
    if request.user.is_authenticated:
        return redirect('app:home')  # Redirect if already authenticated

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_teacher = form.cleaned_data['is_teacher']
            user.save()
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
@csrf_protect
def login_view(request):
    if request.user.is_authenticated:
        return redirect('app:home')  # Redirect if already authenticated

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('app:home')  # Change 'home' to your desired home page URL
            else:
                form.add_error(None, 'Invalid username or password.')  # Fix the typo here
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')  # Change 'home' to your desired home page URL

from .forms import EditProfileForm
from django.contrib.auth.decorators import login_required

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('app:home')  # Redirect to the home page after saving
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'accounts/edit.html', {'form': form})


from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy

class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'




from django.core.mail import send_mail
from django.http import JsonResponse
import random
import string
# Function to generate 6-digit alphanumeric code
def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


# View to send the verification code to the user's email
def send_verification_code(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        verification_code = generate_code()  # Generate verification code
        request.session['verification_code'] = verification_code  # Store code in session

        # Send verification email to the user's email address
        send_mail(
            'Verification Code for Registration',
            f'Your verification code is: {verification_code}',
            'sender@example.com',
            [email],
            fail_silently=False,
        )

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})
