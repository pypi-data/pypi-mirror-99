from django.conf.urls  import url, include
from . import views
from django.conf import settings
#voir signets
from django.contrib.auth.views import (
    LoginView, LogoutView,
    PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView,PasswordResetDoneView, PasswordResetConfirmView,PasswordResetCompleteView,
)
from rest_framework.authtoken import views as vw
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token, verify_jwt_token
from django.conf.urls.static import static


urlpatterns = [


    url(r'^auth/get-token', obtain_jwt_token),
    url(r'^auth/refresh-token', refresh_jwt_token),
    url(r'^auth/verify-token', verify_jwt_token),
    url(r'^token-auth/', views.LoginToken.as_view()),

    url(r'^auth/login/$', obtain_jwt_token),
    url(r'^auth/register/$', views.UserRegisterView.as_view()),
    url(r'^auth/social/$', views.GoogleView.as_view()),
    url(r'^auth/registersocial/$', views.UserRegisterSocialView.as_view()),
    url(r'^auth/me$', views.UserRetrieveView.as_view()),

    url(r'^reset-password/$', views.PasswordResetView.as_view()),
    url(r'^request-password-reset/$', views.PasswordResetRequestView.as_view()),
    url(r'^changepassword/$', views.ChangePasswordView.as_view()),

    url(r'^user/(?P<id>[0-9]+)/$', views.UserAPIView.as_view()),
    url(r'^user/$', views.UserAPIListView.as_view()),
    url(r'^me/$', views.UserRetrieveView.as_view()),


]
