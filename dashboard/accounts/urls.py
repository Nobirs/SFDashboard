from django.urls import path, include

from .views import SignUpView, ConfirmTokenView


urlpatterns = [
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    path('confirm_token/', ConfirmTokenView.as_view(), name='confirm_token'),
]