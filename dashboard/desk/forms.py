from django import forms

from django_quill.forms import QuillFormField

from .models import Announcement, Resp


class AnnouncementForm(forms.ModelForm):

    class Meta:
        model = Announcement
        fields = (
            'title',
            'content',
            'category',
        )


class RespForm(forms.ModelForm):

    class Meta:
        model = Resp
        fields = (
            'content',
        )
