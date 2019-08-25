from django.contrib import admin
from .models import Stage,Major

# Register your models here.

# 布道师内联对象
class TeacherInline(admin.TabularInline):
    model = Stage.teacher.through
    extra = 0
    classes = ("collapse",)

# 阶段
@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    exclude = []
    inlines = [TeacherInline]
    list_display = ['name','major','hour','show_teacher']
    fieldsets = (("专业编辑",{
            'fields':('name','major','hour')
        },),)
    def show_teacher(self,obj):
        print(obj.teacher)
        return "this is teacher"

# 专业
@admin.register(Major)
class MojorAdmin(admin.ModelAdmin):
    exclude = []
    list_display = ['name']
