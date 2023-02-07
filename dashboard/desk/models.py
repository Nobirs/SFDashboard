from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from django_quill.fields import QuillField
from django_lifecycle import LifecycleModel, hook, AFTER_CREATE


class Category(LifecycleModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Announcement(LifecycleModel):
    GAME_CLASSES = (
        ('00', "Танки"),
        ('01', "Хилы"),
        ('02', "ДД"),
        ('03', "Торговцы"),
        ('04', "Гилдмастеры"),
        ('05', "Квестгиверы"),
        ('06', "Кузнецы"),
        ('07', "Кожевники"),
        ('08', "Зельевары"),
        ('09', "Мастера Заклинаний"),
    )

    title = models.CharField(max_length=150)
    content = QuillField()
    creation_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=2, choices=GAME_CLASSES, default='00')

    @hook(AFTER_CREATE)
    def send_mass_email_to_users(self):
        from .tasks import send_mass_emails_to_users
        send_mass_emails_to_users.delay(self.id, self.author.id)

    def __str__(self):
        return self.title[:20]

    def get_absolute_url(self):
        reverse_url = reverse('announcement', args=[str(self.id)])
        return reverse_url

    class Meta:
        verbose_name_plural = "Announcements"


class Resp(LifecycleModel):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.content[:20]

    class Meta:
        verbose_name = "Announcement Response"
        verbose_name_plural = "Announcement Responses"

