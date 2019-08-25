from django.db import models

# Create your models here.

# 专业
class Major(models.Model):
    name = models.CharField(max_length=10,verbose_name="专业")
    class Meta:
        verbose_name_plural = '专业方向表'
        # 末尾加s
        verbose_name='专业方向表'
    def __str__(self):
        return self.name

# 阶段
class Stage(models.Model):
    major = models.ForeignKey(to='Major', on_delete=models.CASCADE,verbose_name="专业")
    name = models.CharField(max_length=10,verbose_name="阶段")
    hour = models.IntegerField(default=40,verbose_name="课时")
    teacher = models.ManyToManyField(to="teachers.Teacher", through='teachers.TeacherStage')
    class Meta:
        verbose_name_plural="阶段表"
        verbose_name="阶段表"
    def __str__(self):
        return self.name

# 阶段优先级
class StagePriority(models.Model):
    pre_course = models.ForeignKey(to='Stage',verbose_name="前导阶段",on_delete=models.CASCADE,related_name='pre_course')
    next_course = models.ForeignKey(to="Stage",verbose_name="后续阶段",on_delete=models.CASCADE,related_name="next_course")
    priority = models.IntegerField(default=0,verbose_name="优先级")


# 教室
class Classroom(models.Model):
    name = models.CharField(max_length=20,verbose_name="教室",unique=True)
