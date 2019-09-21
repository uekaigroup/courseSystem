from django.contrib import admin
from .models import CourseTimetable


# Register your models here.

@admin.register(CourseTimetable)
class CourseTimetableAdmin(admin.ModelAdmin):
    exclude = []