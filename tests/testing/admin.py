# -*- coding: utf-8 -*-
from django.contrib import admin

from . import models

admin.site.register(models.User)
admin.site.register(models.QuestionSet)
admin.site.register(models.Question)
admin.site.register(models.Option)
admin.site.register(models.Submission)
