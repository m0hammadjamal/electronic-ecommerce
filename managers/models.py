from django.db import models

from users.models import User
from main.models import CommonModel


class Manager(CommonModel):
    created_datetime = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'is_manager': True})

    class Meta:
        db_table = 'managers_manager'
        verbose_name = 'manager'
        verbose_name_plural = 'managers'
        ordering = ('id',)

    def __str__(self):

        return self.user.email


class Notification(CommonModel):
    title = models.CharField(max_length=256)
    description = models.TextField()

    class Meta:
        db_table = 'notification_table'
        verbose_name = 'notification'
        verbose_name_plural = 'notifications'
        ordering = ["-id"]

    def __str__(self):
        return self.title
    