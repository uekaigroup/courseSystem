from django.contrib import admin
from .models import Stage,Major,StagePriority,Classroom
from teachers.models import Teacher

# Register your models here.

# 布道师内联对象
class TeacherInline(admin.TabularInline):
    model = Stage.teacher.through
    extra = 0
    classes = ("collapse",)

# 阶段后台
@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    exclude = []
    inlines = [TeacherInline]
    list_display = ['name','major','hour','show_teacher']
    list_filter = ('name','major','hour')
    fieldsets = (("专业编辑",{
            'fields':('name','major','hour')
        },),)
    def show_teacher(self,obj):

        return [item for item in obj.teacher.all()]


# 方向阶段内联表对象
class MajorStageInline(admin.TabularInline):
    model = Stage
    extra = 6
    classes = ("collapse",)


# 专业后台
@admin.register(Major)
class MojorAdmin(admin.ModelAdmin):
    exclude = []
    list_display = ['name',"show_stage"]
    inlines = [MajorStageInline,]
    def show_stage(self,obj):
        print(obj.stage_set.all())
        return [ item for item in obj.stage_set.all()]

# 老师阶段优先级
@admin.register(StagePriority)
class StagePriorityAdmin(admin.ModelAdmin):
    exclude = []


# 教师
@admin.register(Classroom)
class StagePriorityAdmin(admin.ModelAdmin):
    exclude = []

