from django.db import models

# Create your models here.

# 教师
class Teacher(models.Model):
    name = models.CharField(max_length=8,verbose_name="布道师")
    status = models.BinaryField(max_length=14, default=b"00000000000000",verbose_name='本周上课情况')
    major = models.ForeignKey(to='direction.Major', on_delete=models.CASCADE,verbose_name="方向")
    class Meta:
        verbose_name_plural = '布道师表'
        # 末尾加s
        verbose_name='布道师表'
    def __str__(self):
        return self.name

# 老师阶段表
class TeacherStage(models.Model):
    teacher = models.ForeignKey(to='Teacher', on_delete=models.CASCADE,verbose_name="布道师")
    stage = models.ForeignKey(to='direction.Stage', on_delete=models.CASCADE,verbose_name='阶段')
    priority = models.IntegerField(default=0,verbose_name="权重")
    num = models.IntegerField(default=0,verbose_name="实施数量",editable=False)
    class Meta:
        verbose_name_plural = '布道师带课阶段表'
        # 末尾加s
        verbose_name='布道师带课阶段表'
    def __str__(self):
        return "[%s-%s-%s-%s]"%(self.teacher,self.stage,self.priority,self.num)

