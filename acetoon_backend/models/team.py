from django.db import models

from acetoon_backend.models import User, Contest


class Team(models.Model):

    owner = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='team'
    )
    members = models.ManyToManyField(
        to=User,
        blank=True,
        related_name='teams',
    )
    name = models.CharField(
        max_length=255,
    )
    token = models.CharField(
        max_length=64,
        blank=True
    )
    email = models.EmailField()
    contest = models.ForeignKey(
        to=Contest,
        on_delete=models.CASCADE,
        related_name='participants',
    )
    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        contest = self.contest
        name = self.name

        return f'{name} | Contest: {contest}'

    class Meta:
        unique_together = ('name', 'contest')
        ordering = ['-timestamp']
