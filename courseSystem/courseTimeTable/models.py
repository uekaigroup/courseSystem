from django.db import models

# Create your models here.

# 课程表
class CourseTimetable(models.Model):
    date = models.CharField(max_length=200,verbose_name="课表数据")
    week = models.IntegerField(verbose_name="周数")
    status = models.IntegerField(verbose_name="排课状态") # 已排课 已生成
