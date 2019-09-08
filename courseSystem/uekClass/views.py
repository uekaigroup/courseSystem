from django.shortcuts import render
import time,numpy as np
from .models import Classes,OutClasses
from direction.models import Stage,StagePriority,Major
from orderCla.order_classes import model
from teachers.models import Teacher,TeacherStage

classes=Classes.objects.all()
stage=Stage.objects.all()
outclasses=OutClasses.objects.all()
stagePriority=StagePriority.objects.all()
teachers=Teacher.objects.all()
teacherstage=TeacherStage.objects.all()


def getWeek():
    week=time.strftime('%W')
    week=int(week)+1
    return week

# Create your views here.
def index(request):
    week=getWeek()
    goon=classes.exclude(now_long_time=0) #当前阶段未结束班级
    gonext=classes.filter(now_long_time=0) #当前阶段已结束班级
    aa=outclasses.filter(week=week)
    a=orderOutside()
    b=orderNormal()
    print(a)
    print(b)
    lt=teachers.filter(name='刘涛').first()
    ydh=teachers.filter(name='杨登辉').first()
    hnz=teachers.filter(name='候宁州').first()
    print(lt.name,lt.status)
    print(ydh.name,ydh.status)
    print(hnz.name,ydh.status)
    ydh.status='00000000000000'
    lt.status='00000000000000'
    hnz.status='00000000000000'
    lt.save()
    ydh.save()
    hnz.save()
    return render(request,'uekClass/index.html')

# 班级分类
def orderClass(classes):
    order = []
    for i in classes:
        order.append(model.predict([[i.education, i.stu_num,i.benke_num,i.dazhuan_num,i.zhongzhuan_num,i.gaozhong_num,i.is_outside]])[0][0])
    sortclass = list(reversed(np.argsort(np.array(order))))
    return sortclass

# 根据前置课程获取阶段优先级排序列表stages,sortarr
def bToA(nowstage):
    stages=stagePriority.filter(pre_course=nowstage)
    levelarr=[i.priority for i in stages]
    nparr=np.array(levelarr)
    sortarr=list(reversed(np.argsort(nparr)))
    return stages,sortarr

# 返回对于某阶段的老师以及排序下标teacherarr,sortteacher
def sort_teacher(stage):
    teacherstage=TeacherStage.objects.all()
    tss=teacherstage.filter(stage=stage)
    teacherarr=[i.teacher for i in tss]
    sortteacher=list(reversed(np.argsort(np.array([i.priority for i in tss]))))
    return teacherarr,sortteacher

# 对当前阶段未完成班级排课
def orderGoOn():
    goon = classes.exclude(now_long_time=0)  # 筛选符合条件班级
    next_week = getWeek()                    # 获得下周的周数
    sortList=orderClass(goon)                # 进行优先级排序获得排序下标
    class_sheet_list = []                    # 用来存放最终数据
    for a in sortList:                       # 按顺序选择班级
        a=int(a)                             # 把numpy元素转换成int
        # print(goon[a].now_long_time)
        class_sheet = {}                     # 某个班的排课数据
        class_a = goon[a]                    # 选中某一个班级
        class_sheet['classname'] = class_a.name         # 班名
        class_sheet['croom'] = class_a.croom.name       # 教室
        class_sheet['course'] = []                      # 具体每天的课程
        teacher2=class_a.is_teacher2                    # 是否有助教
        now_mode=list(class_a.now_mode.mode)            # 目前上课模式
        # around=now_mode.count('1')
        is_end=class_a.is_end                           # 是否结训
        week=class_a.week                               # 班级下次上课周数
        nowstage = class_a.now_stage  # 当前阶段
        longtime = int(stage.filter(name=nowstage.name).first().hour)  # 当前阶段总共时长
        now_long_time = int(class_a.now_long_time)
        if is_end:                                      # 是否结训
            break
        if week!=next_week:                             # 是否符合上课周数
            break
        if now_long_time==longtime:                     # 阶段进行时长等于阶段时长
            break
        for b in range(14):                             # 对14个半天进行排课
            if now_mode[b]=='0':                        # 如果此半天不上课则返回空数据
                halfday = {}
                class_sheet['course'].append(halfday)
                continue
            halfday = {}                                # 半天的阶段和老师
            nowstage = class_a.now_stage  # 当前阶段
            longtime = int(stage.filter(name=nowstage.name).first().hour)  # 当前阶段总共时长
            now_long_time = int(class_a.now_long_time) # 保证每半天的数据更新
            now_teacher=class_a.now_teacher                 # 目前代课老师
            # 如果还没有进入下一个阶段
            if longtime - now_long_time >= 4:           #如果课时差值大于四
                halfday['stage'] = nowstage.name
                halfday['teacher'] = now_teacher.name
                class_sheet['course'].append(halfday)
                state = list(now_teacher.status)
                state[b] = '1'
                str=now_teacher.state = ''.join(state)
                now_teacher.status=str
                now_teacher.save()
                class_a.now_long_time = int(class_a.now_long_time) + 4
                class_a.save()
            else:                                       # 如果不够半天课时
                stages,sortarr = bToA(nowstage)         # 获得下一阶段的优先级排序下标
                if not len(stage):                      # 不存在后置阶段说明结训
                    class_a.is_end = 1
                    class_a.save()
                    break
                afterstage = stages[int(sortarr[0])].next_course # 获取优先级最高的下一阶段
                halfday['stage'] = afterstage.name
                endstages=class_a.endstages.split('-')                     # 已完成阶段
                print(endstages)
                if endstages[0]=='暂无':
                    class_a.endstages=class_a.now_stage.name
                else:
                    endstages.append(class_a.now_stage.name)
                    new_endstages='-'.join(endstages)
                    class_a.endstages=new_endstages
                class_a.save()
                class_a.now_stage = afterstage
                class_a.save()
                class_a.now_long_time = 4
                class_a.save()
                teacherarr, sortteacher = sort_teacher(afterstage)
                for c in sortteacher:
                    c = int(c)
                    if teacherarr[c].status[b] == '1':
                        continue
                    teachersdate = teacherarr[c]
                    status = list(teachersdate.status)
                    status[b] = '1'
                    teachersdate.status = ''.join(status)
                    teachersdate.save()
                    halfday['teacher'] = teacherarr[c].name
                    class_a.now_teacher=teacherarr[c]
                    class_a.save()
                    break
                else:
                    halfday['teacher'] = '没有空闲老师'
                class_sheet['course'].append(halfday)
        class_a.week=week+1
        # class_a.save()
        print(class_sheet)

# 对校外班级进行排课
def orderOutside():
    goon = outclasses  # 筛选符合条件班级
    next_week = getWeek()                    # 获得下周的周数
    class_sheet_list = []                    # 用来存放最终数据
    for a in goon:                       # 按顺序选择班级
        class_sheet = {}                     # 某个班的排课数据
        class_a=a
        data=a.data
        data1=data.split(',')
        print(data1)
        outstage=[]
        for i in data1:
            data2=i.split('-')
            for j in range(int(data2[1])):
                outstage.append(data2[0])
                outstage.append(data2[0])
        data3=outstage
        class_sheet['classname'] = class_a.name         # 班名
        class_sheet['croom'] = class_a.croom            # 教室
        class_sheet['course'] = []                      # 具体每天的课程
        teacher2=class_a.is_teacher2                    # 是否有助教
        week=class_a.week                               # 班级下次上课周数
        if week!=next_week:                             # 是否符合上课周数
            break
        print(data3)
        for b in range(len(data3)):                             # 对14个半天进行排课
            halfday={}
            con=data3[b]
            if con=='0':
                class_sheet['course'].append(halfday)
            else:
                halfday['stage']=con
                major=Major.objects.all().filter(name=con).first()
                teach=teachers.filter(major=major).order_by('-priority')
                for c in teach:
                    status=c.status
                    if status[b]=='0':
                        halfday['teacher'] = c.name
                        class_sheet['course'].append(halfday)
                        status = list(c.status)
                        status[b] = '1'
                        c.status = ''.join(status)
                        c.save()
                    else:
                        continue
        class_a.week = week + 1
        # class_a.save()
        class_sheet_list.append(class_sheet)
    return class_sheet_list





# 对阶段完成班级和新开班级进行排课
def orderNormal():
    goon = classes  # 筛选符合条件班级
    next_week = getWeek()                    # 获得下周的周数
    sortList=orderClass(goon)                # 进行优先级排序获得排序下标
    print(sortList)
    class_sheet_list = []                    # 用来存放最终数据
    for a in sortList:                       # 按顺序选择班级
        print('aaaa',a)
        a=int(a)                             # 把numpy元素转换成int
        # print(goon[a].now_long_time)
        class_sheet = {}                     # 某个班的排课数据
        class_a = goon[a]                    # 选中某一个班级
        class_sheet['classname'] = class_a.name         # 班名
        class_sheet['croom'] = class_a.croom.name       # 教室
        class_sheet['course'] = []                      # 具体每天的课程
        teacher2=class_a.is_teacher2                    # 是否有助教
        now_mode=list(class_a.now_mode.mode)            # 目前上课模式
        # around=now_mode.count('1')
        is_end=class_a.is_end                           # 是否结训
        week=class_a.week                               # 班级下次上课周数
        nowstage = class_a.now_stage  # 当前阶段
        longtime = int(stage.filter(name=nowstage.name).first().hour)  # 当前阶段总共时长
        now_long_time = int(class_a.now_long_time)
        if is_end:                                      # 是否结训
            continue
        print('aaa')
        if week!=next_week:                             # 是否符合上课周数
            break
        for b in range(14):                             # 对14个半天进行排课
            print(b)
            if now_mode[b]=='0':                        # 如果此半天不上课则返回空数据
                halfday = {}
                class_sheet['course'].append(halfday)
                continue
            halfday = {}                                # 半天的阶段和老师
            nowstage = class_a.now_stage  # 当前阶段
            longtime = int(stage.filter(name=nowstage.name).first().hour)  # 当前阶段总共时长
            now_long_time = int(class_a.now_long_time) # 保证每半天的数据更新
            now_teacher=class_a.now_teacher                 # 目前代课老师
            # 如果还没有进入下一个阶段
            if longtime - now_long_time >= 4:           #如果课时差值大于四
                halfday['stage'] = nowstage.name
                halfday['teacher'] = now_teacher.name
                class_sheet['course'].append(halfday)
                status = list(now_teacher.status)
                status[b] = '1'
                now_teacher.status = ''.join(status)
                now_teacher.save()
                class_a.now_long_time = int(class_a.now_long_time) + 4
                class_a.save()
            else:                                       # 如果不够半天课时
                stages,sortarr = bToA(nowstage)         # 获得下一阶段的优先级排序下标
                print(type(len(sortarr)))
                if len(sortarr)==0:                      # 不存在后置阶段说明结训
                    print('break')
                    class_a.is_end = 1
                    class_a.save()
                    break
                # afterstage = stages[int(sortarr[0])].next_course # 获取优先级最高的下一阶段
                afterstage=''
                for after in sortarr:
                    after=int(after)
                    afterstage=stages[after].next_course.name
                    endlist=class_a.endstages.split('-')
                    if afterstage in endlist:
                        continue
                    else:
                        afterstage=afterstage
                print(dir(afterstage))
                halfday['stage'] = afterstage.name
                endstages=class_a.endstages.split('-')                     # 已完成阶段
                print(endstages)
                if endstages[0]=='暂无':
                    class_a.endstages=class_a.now_stage.name
                else:
                    endstages.append(class_a.now_stage.name)
                    new_endstages='-'.join(endstages)
                    class_a.endstages=new_endstages
                class_a.save()
                class_a.now_stage = afterstage
                class_a.save()
                class_a.now_long_time = 4
                class_a.save()
                teacherarr, sortteacher = sort_teacher(afterstage)
                for c in sortteacher:
                    c = int(c)
                    if teacherarr[c].status[b] == '1':
                        continue
                    teachersdate = teacherarr[c]
                    status = list(teachersdate.status)
                    status[b] = '1'
                    teachersdate.status = ''.join(status)
                    teachersdate.save()
                    halfday['teacher'] = teacherarr[c].name
                    class_a.now_teacher=teacherarr[c]
                    class_a.save()
                    break
                else:
                    halfday['teacher'] = '没有空闲老师'
                class_sheet['course'].append(halfday)
        class_a.week=week+1
        # class_a.save()
        # print(class_sheet)
        class_sheet_list.append(class_sheet)
    return class_sheet_list