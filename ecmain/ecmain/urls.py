"""
URL configuration for ecmain project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from users import views as users_views

from django.contrib.auth import views as auth_views
from users.forms import LoginForm, ChangePasswordForm, ResetPasswordForm, NewPasswordForm

from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('app.urls')),

    #login authentications
    path('registration/', users_views.CustomerRegistrationView.as_view(), name="customer_registration"),
    path('profile/', users_views.ProfileView.as_view(), name="profile"),
    path('address/', users_views.address, name="address"),
    path('updateaddress/<int:pk>', users_views.UpdateAddress.as_view(), name="updateaddress"),

    path('accounts/login/', auth_views.LoginView.as_view(template_name="users/login.html", authentication_form=LoginForm), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page='login'), name="logout"),

    path('password-change/', auth_views.PasswordChangeView.as_view(template_name="users/password_change.html", form_class=ChangePasswordForm, success_url='/password-change-done'), name="password_change"),
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"), name="password_change_done"),
    
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name="users/password_reset.html", form_class=ResetPasswordForm), name="password_reset"),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name = 'users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = 'users/password_reset_confirm.html', form_class =NewPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'users/password_reset_complete.html'), name='password_reset_complete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)