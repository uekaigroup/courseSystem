from django.db import models

# Create your models here.

# 课程表
# class CourseTimetable(models.Model):
#     data = models.CharField(max_length=200,verbose_name="课表数据")
#     week = models.IntegerField(verbose_name="周数",default=0)
#     # status = models.IntegerField(verbose_name="排课状态") # 已排课 已生成
#     def __str__(self):
#         return self.week

class CourseTimeTable(models.Model):
    data = models.CharField(max_length=200,verbose_name="课表数据")
    week = models.IntegerField(verbose_name="周数",default=0)
    # status = models.IntegerField(verbose_name="排课状态") # 已排课 已生成
    # def __str__(self):
    #     return str(self.week)