# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import *

# Register your models here.

admin.site.register(teacher)
admin.site.register(student)

admin.site.register(FE1)

admin.site.register(SE1)

admin.site.register(TE1)

admin.site.register(BE1)
admin.site.register(parent)

admin.site.register(total_lectures)
admin.site.register(dates)
admin.site.register(head)