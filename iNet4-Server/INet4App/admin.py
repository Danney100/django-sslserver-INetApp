# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import User
from .models import Job
from .models import Job_Task

# Register your models here.
admin.site.register(User)
admin.site.register(Job)
admin.site.register(Job_Task)
