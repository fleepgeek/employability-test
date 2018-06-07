from django.contrib import admin

from .models import PersonalityQuestion, PersonalityType, TestQuestion, TestChoice

class PersonalityQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'category')

admin.site.register(PersonalityQuestion, PersonalityQuestionAdmin)

admin.site.register(PersonalityType)


class TestChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text', 'question')

admin.site.register(TestChoice, TestChoiceAdmin)

admin.site.register(TestQuestion)