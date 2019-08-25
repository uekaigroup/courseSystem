from django.contrib import admin
from .models import Teacher,TeacherStage
# Register your models here.

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    exclude = []
    list_display = ['name']

@admin.register(TeacherStage)
class TeacherStage(admin.ModelAdmin):
    exclude = []
    list_display = ['teacher','stage','priority','num']

