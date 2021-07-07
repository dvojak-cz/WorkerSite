from django.contrib.auth import views as auth_view
from django.urls import path

from accounts import views

urlpatterns = [
    path('', views.login_page, name='login-AC'),
    path('logout/', views.logout_page, name="logout-AC"),

    path('reset_password/',
         auth_view.PasswordResetView.as_view(
                 template_name="accounts/password_change_form_email.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_view.PasswordResetDoneView.as_view(
                 template_name="accounts/password_change_email_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_view.PasswordResetConfirmView.as_view(
                 template_name="accounts/password_change_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_view.PasswordResetCompleteView.as_view(
                 template_name="accounts/password_change_done.html"),
         name="password_reset_complete"),
    ]
