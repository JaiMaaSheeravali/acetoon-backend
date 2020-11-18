from django.db import models
from acetoon_backend.models import Team, Contest
from django.core.validators import MaxValueValidator, MinValueValidator
from ckeditor.fields import RichTextField

def upload_path(instance, filename):
    return '/'.join(['submissions', str(instance.team.name), filename])

class Submission(models.Model):

    team = models.ForeignKey(
        to=Team,
        on_delete=models.CASCADE,
        related_name='team_submissions'
    )
    feedback = RichTextField(blank=True)
    contest = models.ForeignKey(
        to=Contest,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    rating = models.PositiveIntegerField(
        blank=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )
    timestamp = models.DateTimeField(
        auto_now_add=True
    )
    link = models.URLField(blank=True)
    file = models.FileField(
        upload_to=upload_path,
        blank=True,
    )

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        contest = self.contest
        team = self.team

        return f'Submission: {team} | Contest: {contest}'