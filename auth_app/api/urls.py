from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from .views import RegistrationView, CustomLoginView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
]
