from django.contrib import admin

from .models import PersonalityQuestion, PersonalityType, TestQuestion, TestChoice

admin.site.register(PersonalityQuestion)
admin.site.register(PersonalityType)
admin.site.register(TestQuestion)
admin.site.register(TestChoice)