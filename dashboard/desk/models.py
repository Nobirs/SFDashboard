from django.db import models
from django.contrib.auth.models import User

from django_quill.fields import QuillField
from django_lifecycle import LifecycleModel, hook


class Category(LifecycleModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Announcement(LifecycleModel):
    title = models.CharField(max_length=150)
    content = QuillField()
    creation_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.title[:20]

    class Meta:
        verbose_name_plural = "Announcements"


class Resp(LifecycleModel):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:20]

    class Meta:
        verbose_name = "Announcement Response"
        verbose_name_plural = "Announcement Responses"

