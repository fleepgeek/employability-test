from django.db import models
from django.db.models.signals import post_save
from django.conf import settings

from personality.models import PersonalityType

User = settings.AUTH_USER_MODEL

class Applicant(models.Model):
    user                    = models.OneToOneField(User, on_delete=models.CASCADE)
    personality             = models.ManyToManyField(PersonalityType, blank=True)
    test_score              = models.PositiveIntegerField(default=0)
    taken_apt_test          = models.BooleanField(default=False)
    taken_personality_test  = models.BooleanField(default=False)
    is_employable           = models.BooleanField(default=False)
    date_joined             = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username