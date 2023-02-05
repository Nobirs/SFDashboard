from django.db import models
from django.contrib.auth.models import User
from django_lifecycle import LifecycleModel, hook, BEFORE_UPDATE, AFTER_UPDATE


class Token(LifecycleModel):
    token = models.CharField(max_length=100)
    confirmed = models.BooleanField(default=False)
    generation_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = "Tokens"
