from django.contrib import admin
from .models import Teacher,TeacherStage

# Register your models here.

# 布道师阶段内联

class TeacherStageInline(admin.TabularInline):
    model = TeacherStage
    extra = 3
    classes = ("collapse",)

# 布道师后台
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    exclude = []
    list_display = ['name','major','status','show_stage']
    list_filter = ['major',"major__name"]
    inlines = [TeacherStageInline]
    def show_stage(self,obj):
        return [ item.stage for item in obj.teacherstage_set.all()]


# 布道师阶段后台
@admin.register(TeacherStage)
class TeacherStage(admin.ModelAdmin):
    exclude = []
    list_display = ['teacher','stage','priority','num']
    list_filter = ['stage',"priority",'num']

# 老师阶段优先级
# @admin.register(StagePriority)


