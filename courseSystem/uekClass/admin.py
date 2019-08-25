from django.contrib import admin
from .models import Classes,Mode,OutClasses,ClassRecord
# Register your models here.

@admin.register(ClassRecord)
class ClassRecordAdmin(admin.ModelAdmin):
    exclude = []

@admin.register(OutClasses)
class OutClassesAdmin(admin.ModelAdmin):
    exclude = []

@admin.register(Mode)
class ModeAdmin(admin.ModelAdmin):
    exclude = []

@admin.register(Classes)
class ClassesAdmin(admin.ModelAdmin):
    exclude = []