from django.urls import path, include
from .views import CustomResetPasswordRequestToken

urlpatterns = [
    path('password_reset/', CustomResetPasswordRequestToken.as_view(), name='password-reset'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]