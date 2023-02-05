from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import Announcement, Resp


@shared_task
def inform_about_response(resp_user, resp_content, announcement_id):
    email = Announcement.objects.get(id=announcement_id).author.email
    send_mail(
        subject="Inform about response to your announcement",
        message=f"User {resp_user} send you {resp_content} to your announcement",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False
    )


@shared_task
def accept_user_response(resp_id, announcement_title):
    email = Resp.objects.get(id=resp_id).author.email
    send_mail(
        subject="Your response was accepted",
        message=f"Your response to announcement <{announcement_title}> was accepted",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False
    )


@shared_task
def send_mass_emails_to_users(announcement_id, author_id):
    announcement = Announcement.objects.get(id=announcement_id)
    announcement_author = User.objects.get(id=author_id)
    all_authors = User.objects.all()
    mass_emails = []
    for user in all_authors:
        if user != announcement_author and user.email != '':
            mass_emails.append(user.email)
    mass_emails = list(set(mass_emails))
    print(f"Emails: {mass_emails}")
    html_message = render_to_string('mails/new_announcement.html', {'announcement': announcement})
    send_mail(
        subject="New announcement in WoW",
        message=strip_tags(html_message),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=mass_emails,
        html_message=html_message,
        fail_silently=False
    )


