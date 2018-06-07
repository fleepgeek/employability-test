from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from django.conf import settings

from .models import Applicant

User = get_user_model()


class ApplicantInline(admin.StackedInline):
    model = Applicant
    can_delete = False
    verbose_name_plural = 'Applicant'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ApplicantInline, )
    list_display = ('username', 'email', 'is_staff')
    list_select_related = ('applicant', )
    # def get_validated(self, instance):
    #     return instance.author.email_validated
    # get_validated.short_description = 'Email Validated'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)