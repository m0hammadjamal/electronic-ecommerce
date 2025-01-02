from django.db import models

from users.models import User


class CommonModel(models.Model):

    """
    A common abstract class for inheriting some common fields
    """

    created_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_datetime = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, related_name='+', 
                                        blank=True, null=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='+',
                                        blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True
