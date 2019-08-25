from django.db import models
from django.utils import timezone
# Create your models here.

# 上课模式表
class Mode(models.Model):
    name=models.CharField(
        max_length=20,
        verbose_name='模式名'
    )
    mode=models.CharField(
        max_length=20,
        verbose_name='上课模式'
    )
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = '模式表'
        verbose_name = '模式表'


# 班级表
class Classes(models.Model):
    name=models.CharField(
        max_length=20,
        verbose_name='班级名称'
    )
    p_id=models.ForeignKey(
        to="direction.Major",
        on_delete=models.CASCADE,
        verbose_name='班级方向'
    )
    stu_num=models.IntegerField(
        verbose_name='班级人数',
        default=0
    )
    room=models.ForeignKey(
        to='direction.Classroom',
        on_delete=models.CASCADE,
        verbose_name='教室',
    )
    now_stage=models.ForeignKey(
        to="direction.Stage",
        on_delete=models.CASCADE,
        verbose_name='当前阶段',
        default=None
    )
    now_long_time = models.IntegerField(
        verbose_name='当前阶段已上课时',
        default=0
    )
    education = models.IntegerField(choices=(
        (0, '非本科'),
        (1, '本科')),
        default=0, verbose_name='学历'
    )
    benke_num=models.IntegerField(
        verbose_name='本科人数',
        default=0
    )
    dazhuan_num = models.IntegerField(
        verbose_name='大专人数',
        default=0
    )
    zhongzhuan_num = models.IntegerField(
        verbose_name='中专人数',
        default=0
    )
    gaozhong_num = models.IntegerField(
        verbose_name='高中人数',
        default=0
    )
    now_teacher=models.ForeignKey(
        to='teachers.Teacher',
        on_delete=models.CASCADE,
        verbose_name='当前代课老师名字',
    )
    is_teacher2 = models.IntegerField(choices=(
        (0, '不需要助教'),
        (1, '必须要助教')),
        default=0, verbose_name='是否需要助教'
    )
    is_outside = models.IntegerField(choices=(
        (0, '不是校外课程'),
        (1, '是校外课程')),
        default=0, verbose_name='是否校外课程'
    )
    now_mode=models.ForeignKey(
        to=Mode,
        on_delete=models.CASCADE,
        verbose_name='目前上课模式'
    )
    is_end = models.IntegerField(choices=(
        (0, '未结训'),
        (1, '已结训')),
        default=0, verbose_name='是否校外课程'
    )
    endstages=models.CharField(
        max_length=50,
        verbose_name='已完成阶段',
        help_text='例如:ps-软件设计'
    )
    now_week=models.IntegerField(
        verbose_name='周数',
        default=0,
        help_text='例如:201934,表示2019年第34周'
    )
    start_time=models.DateTimeField('开班时间',default=timezone.now)
    add_date_time = models.DateTimeField(auto_now_add=True)
    update_date_time = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural='正常班级'


# 校外班级
class OutClasses(models.Model):
    name=models.CharField(
        max_length=20,
        verbose_name='校外班级表'
    )
    time=models.DateField('开始时间',default=timezone.now)
    data=models.CharField(
        max_length=50,
        verbose_name='课程内容'
    )
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural='校外班级'


# 班级信息记录表
class ClassRecord(models.Model):
    classes=models.ForeignKey(
        to=Classes,
        on_delete=models.CASCADE,
        verbose_name='对应班级'
    )
    endstages=models.CharField(
        max_length=50,
        verbose_name='已完成阶段',
        default=' '
    )
    now_stage = models.ForeignKey(
        to="direction.Stage",
        on_delete=models.CASCADE,
        verbose_name='当前阶段',
        default=None
    )
    now_long_time = models.IntegerField(
        verbose_name='当前阶段已上课时',
        default=0
    )
    now_week = models.IntegerField(
        verbose_name='第几周',
        default=0
    )
    def __str__(self):
        return self.classes.name
    class Meta:
        verbose_name_plural='班级每周信息'

