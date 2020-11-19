from django.db import models
from acetoon_backend.models.user import Organizer


class Contest(models.Model):

    organizer = models.ForeignKey(
        to=Organizer,
        on_delete=models.CASCADE,
        related_name='contests',
    )
    contest_type = (
        ('PT', 'Painting'),
        ('SI', 'Singing'),
        ('HT', 'Hackathon'),
        ('DN', 'Dancing'),
        ('PT', 'Photography'),
        ('OT', 'Other'),
    )
    name = models.CharField(
        max_length=255,
    )
    type = models.CharField(
        max_length=2,
        choices=contest_type,
    )
    start_date = models.DateField()
    expiry_date = models.DateField()
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    eligibility = models.TextField(
        blank=True
    )
    rules = models.TextField()
    prizes = models.TextField(
        blank=True,
    )

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        contest = self.name
        organizer = self.organizer

        return f'{contest} by {organizer}'


class Announcement(models.Model):

    text = models.TextField()
    timestamp = models.DateTimeField(
        auto_now_add=True
    )
    contest = models.ForeignKey(
        to=Contest,
        on_delete=models.CASCADE,
        related_name='announcements'
    )

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        contest = self.contest
        timestamp = self.timestamp

        return f'Announcement: {contest} | {timestamp}'

    class Meta:
        ordering = ['-timestamp']
