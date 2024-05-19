from django.urls import path,include
from .views import register_view, login_view, logout_view,edit_profile
from accounts import views

app_name = 'accounts'  # Add this line to specify the app namespace


urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('edit-profile/', edit_profile, name='edit_profile'),  # Add this line for editing profile

    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('send-verification-code/', views.send_verification_code, name='send_verification_code'),


]
