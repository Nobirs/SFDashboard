import binascii
import os

from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.models import User, Permission
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView

from .forms import SignUpForm, SignUpTokenForm

from .models import Token


def generate_key():
    return binascii.hexlify(os.urandom(20)).decode()


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    success_url = '/accounts/confirm_token/'

    template_name = "accounts/sign_up.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        new_user = self.object
        new_user.is_active = False
        new_user.save()

        new_user_token = Token(token=generate_key(), user=new_user)
        new_user_token.save()

        send_mail(
            "Confirm authorization at Dashboard",
            f"Token: {new_user_token.token}",
            settings.EMAIL_HOST_USER,
            [new_user.email],
            fail_silently=False,
        )
        self.request.session['new_user'] = new_user.username
        self.request.session['new_user_token'] = new_user_token.token
        return HttpResponseRedirect(self.get_success_url())

    # def post(self, request, *args, **kwargs):
    #     form = self.get_form()
    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)


class ConfirmTokenView(CreateView):
    model = Token
    form_class = SignUpTokenForm
    success_url = '/accounts/login/'

    template_name = 'accounts/confirm_token.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        checking_token = self.object.token
        if checking_token == self.request.session['new_user_token']:
            token = Token.objects.get(token=checking_token)
            print(f"Token confirmed: {token.confirmed}")
            token.confirmed = True
            token.save()

            user = token.user
            print(f"User active: {user.is_active}")
            user.is_active = True
            # add basic permissions
            add_announcement = Permission.objects.get(codename='add_announcement')
            change_announcement = Permission.objects.get(codename='change_announcement')
            delete_announcement = Permission.objects.get(codename='delete_announcement')
            delete_resp = Permission.objects.get(codename='delete_resp')
            change_resp = Permission.objects.get(codename='change_resp')

            user.user_permissions.add(add_announcement)
            user.user_permissions.add(change_announcement)
            user.user_permissions.add(delete_announcement)
            user.user_permissions.add(delete_resp)
            user.user_permissions.add(change_resp)

            user.save()
            return HttpResponseRedirect(self.get_success_url())
        return super().form_invalid(form)
