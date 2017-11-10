from django.contrib import admin
from django import forms

from .models import Application
from .models import Questionnaire
from .models import Submission


class ApplicationAdmin(admin.ModelAdmin):
    pass
    exclude = ('bank', )

admin.site.register(Application, ApplicationAdmin)


class QuestionnaireAdmin(admin.ModelAdmin):
    pass

admin.site.register(Questionnaire, QuestionnaireAdmin)


class SubmissionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Submission, SubmissionAdmin)
