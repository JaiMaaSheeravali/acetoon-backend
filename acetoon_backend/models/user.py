from django.db import models

from django.contrib.auth.models import AbstractUser


def upload_path(instance, filename):
    return '/'.join(['profile', str(instance.id), filename])


class User(AbstractUser):

    gender_choices = (
        ('M', 'male'),
        ('F', 'female'),
        ('O', 'other'),
    )
    age = models.PositiveIntegerField()
    gender = models.CharField(
        choices=gender_choices,
        max_length=1,
    )
    designation = models.CharField(
        max_length=255,
        blank=True,
    )
    bio = models.TextField(
        blank=True,
    )
    profile_pic = models.ImageField(
        blank=True,
        upload_to=upload_path
    )


class Organizer(models.Model):

    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name='user',
    )
    contact_no = models.CharField(
        max_length=12,
    )
    email_id = models.EmailField()
    address = models.TextField()
    is_organizer = models.BooleanField(
        default=False,
    )
    timestamp = models.DateTimeField(
        auto_now_add=True
    )
    reason = models.TextField(
        default='Help Nation'
    )

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        person = self.user
        is_organizer = self.is_organizer

        return f'{person} | Organizer: {is_organizer}'
