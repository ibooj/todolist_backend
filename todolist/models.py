from django.conf import settings
from django.db.models.signals import post_save
from django.db import models
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class AbstractTask(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Task(AbstractTask):
    pass


class SubTask(AbstractTask):
    task = models.ForeignKey(Task, related_name='sub_tasks')
    status = models.BooleanField()
