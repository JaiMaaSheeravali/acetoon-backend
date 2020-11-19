from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

from acetoon_backend.models import (
    User,
    Organizer,
    Team,
    Submission,
    Contest,
    Announcement
)
# Register your models here.

models = [
    User,
    Organizer,
    Team,
    Submission,
    Contest,
    Announcement
]

for model in models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
