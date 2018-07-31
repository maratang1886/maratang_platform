from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import User
from django.utils import timezone as django_timezone


class TimeStampedModel(models.Model):
    created_on = models.DateTimeField()
    last_updated_on = models.DateTimeField()
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.created_on is None:
            self.created_on = django_timezone.now()
            self.last_updated_on = self.created_on
        else:
            if self.last_updated_on is None: self.last_updated_on = self.created_on
            else: self.last_updated_on = django_timezone.now()
        if self.is_deleted and self.deleted_on is not None:
            self.last_updated_on = self.deleted_on

        super(TimeStampedModel, self).save(*args, **kwargs)

    def mark_as_deleted(self):
        if not self.is_deleted:
            self.is_deleted = True
            self.deleted_on = django_timezone.now()
            self.save()
            return True
        else:
            return False

    class Meta:
        abstract = True


class MaraUser(AbstractUser):
    # objects = PennUserManager()

    def __str__(self):
        return self.first_name

    @classmethod
    def create(cls, **kwargs):
        return MaraUser.objects.create_user(**kwargs)

    class Meta:
        db_table = 'mara_user'
