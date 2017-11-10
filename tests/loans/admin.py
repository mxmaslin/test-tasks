from django.contrib import admin
from django import forms

from .models import Application
from .models import Questionnaire
from .models import Submission


class ApplicationAdminForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = '__all__'


class ApplicationAdmin(admin.ModelAdmin):
    form = ApplicationAdminForm
    list_display = [
        'created',
        'modified',
        'rotation_started',
        'rotation_ended',
        'applicaton_name',
        'application_type',
        'score_min',
        'score_max',
        'bank']
    readonly_fields = [
        'created',
        'modified',
        'rotation_started',
        'rotation_ended',
        'applicaton_name',
        'application_type',
        'score_min',
        'score_max',
        'bank']

admin.site.register(Application, ApplicationAdmin)


class QuestionnaireAdminForm(forms.ModelForm):

    class Meta:
        model = Questionnaire
        fields = '__all__'


class QuestionnaireAdmin(admin.ModelAdmin):
    form = QuestionnaireAdminForm
    list_display = [
        'created',
        'modified',
        'name',
        'birthday',
        'phone',
        'passport',
        'score']
    readonly_fields = [
        'created',
        'modified',
        'name',
        'birthday',
        'phone',
        'passport',
        'score']

admin.site.register(Questionnaire, QuestionnaireAdmin)


class SubmissionAdminForm(forms.ModelForm):

    class Meta:
        model = Submission
        fields = '__all__'


class SubmissionAdmin(admin.ModelAdmin):
    form = SubmissionAdminForm
    list_display = [
        'created',
        'submitted',
        'questionnaire',
        'application',
        'status']
    readonly_fields = [
        'created',
        'submitted',
        'questionnaire',
        'application',
        'status']

admin.site.register(Submission, SubmissionAdmin)
