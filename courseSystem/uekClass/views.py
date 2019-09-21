from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
import time,numpy as np,json
import datetime,calendar,pandas as pd
from .models import Classes,OutClasses,ClassRecord
from direction.models import Stage,StagePriority,Major,Classroom
from orderCla.order_classes import model
from teachers.models import Teacher,TeacherStage
from coursetable.models import CourseTimetable

classes=Classes.objects.all()
stage=Stage.objects.all()
classrecord=ClassRecord.objects.all()
outclasses=OutClasses.objects.all()
stagePriority=StagePriority.objects.all()
teachers=Teacher.objects.all()
teacherstage=TeacherStage.objects.all()
classroom=Classroom.objects.all()
coursetimetable=CourseTimetable.objects.all()



def getWeek():
    week=time.strftime("%W")
    week=int(week)+1
    return week



def index(request):
    # week=getWeek()
    # goon=classes.exclude(now_long_time=0) #当前阶段未结束班级
    # gonext=classes.filter(now_long_time=0) #当前阶段已结束班级
    # aa=outclasses.filter(week=week)
    # a=orderOutside()
    # b=orderNormal()
    # a=getdata(a)
    # b=getdata(b)
    # b["data"]+=a["data"]
    # data=b
    # teacherlist = getteacher("前端开发", "UAIF1907")
    # print("teacherlist", teacherlist)
    lt=teachers.filter(name="刘涛").first()
    ydh=teachers.filter(name="杨登辉").first()
    hnz=teachers.filter(name="候宁州").first()
    zp=teachers.filter(name="支鹏").first()
    syx=teachers.filter(name="石永鑫").first()
    lz=teachers.filter(name="刘钊").first()
    sxy=teachers.filter(name="索晓勇").first()
    ydh.status="00000000000000"
    lt.status="00000000000000"
    hnz.status="00000000000000"
    zp.status="00000000000000"
    syx.status="00000000000000"
    lz.status="00000000000000"
    sxy.status="00000000000000"
    lt.save()
    ydh.save()
    hnz.save()
    zp.save()
    syx.save()
    lz.save()
    sxy.save()
    return render(request,"uekClass/index.html")

# 获得整合后的课表数据
def getcourse(request):
    table=coursetimetable.filter(week=getWeek())
    if table:
        data=json.loads(table.first().data)
        return JsonResponse(data)
    a = orderOutside()
    b = orderNormal()
    a = getdata(a,getWeek())
    b = getdata(b,getWeek())
    b["data"] += a["data"]
    data = b
    ctt=CourseTimetable(week=getWeek())
    ctt.data=json.dumps(data)
    ctt.save()
    # print("data",data)
    return JsonResponse(data)



# 获取下下周数据
def getnext2course(request,week):
    teachers.update(status='00000000000000')
    week=int(week)
    next2data=coursetimetable.filter(week=week)
    if next2data:
        # next2data=json.loads(next2data.first().data)
        next2data.delete()
    else:
        a = orderOutside()
        truestage=classes.filter(name='MUIDF1906').first().now_stage
        truetime=classes.filter(name='MUIDF1906').first().now_long_time
        # classes.filter(name='MUIDF1906').update(now_stage=truestage)
        print('1',classes.filter(name='MUIDF1906').first().now_long_time)
        b = nosaveorder()
        a = getdata(a,week)
        b = getdata(b,week)
        b["data"] += a["data"]
        nextdata = b
        # print("b",nextdata)
        # ctt = CourseTimetable(week=week)
        # ctt.data = json.dumps(nextdata)
        # ctt.save()
        return JsonResponse(nextdata)

# 保存数据
def savedata(request):
    after_data=request.POST.get('data')
    after_data=json.loads(after_data)
    # after_data=json.loads(request.body)
    data=json.dumps(after_data)
    after_week_data=after_data["data"]
    befor_data=coursetimetable.filter(week=getWeek())
    befor_week=after_data["num"]
    record=classrecord.filter(week=befor_week)
    if after_data==befor_data and record:
        return HttpResponse("ok")
    coursetimetable.filter(week=befor_week).update(data=data)
    classrecord.filter(week=befor_week).delete()

    for j in after_week_data:
        for e in range(7):
            class_record = ClassRecord(week=befor_week)
            class_record.classes = j["class"]
            roomid=classroom.filter(name=j["room"]).first()
            class_record.room = roomid
            class_record.long_time = 8
            stageid=stage.filter(name=j["con"][e]).first()
            if not stageid:
                continue
            class_record.stage = stageid
            stageobj=stage.filter(name=stageid).first()
            classes.filter(name=j["class"]).update(now_stage=stageobj)
            teacherid=teachers.filter(name=j["teacher"][e]).first()
            class_record.teacher = teacherid
            class_record.save()
            classes.filter(name=j["class"]).update(now_teacher=teacherid)
        now_stage=classes.filter(name=j["class"]).first().now_stage
        nowlongtime=classrecord.filter(classes=j["class"]).filter(stage=now_stage).count()*8
        classes.filter(name=j["class"]).update(now_long_time=nowlongtime)
    return HttpResponse("ok")

# 获取空闲教室
def getroom(request,classname):
    nowroom=[classes.filter(name=classname).first().croom.name]

    room=[i.name for i in classroom.filter(status=0)]+nowroom
    room_list={"room_list":room}
    return JsonResponse(room_list)


# 获取可上阶段
def getstage(request,classname):
    classname=classname
    oneclass=classes.filter(name=classname).first()
    major=oneclass.m_id
    stages=[i.name for i in stage.filter(major=major)]
    endlist=oneclass.endstages.split("-")
    uselist = list(set(stages + endlist))
    if endlist[0]=='暂无':
        uselist = list(stages)
    stage_list={"stage_list":uselist}
    return JsonResponse(stage_list)

# 获取课程表信息
def getdata(data1,week):
    data={}
    data["date"]=get_N_day()
    data["num"]=week
    data["data"]=[]
    for i in data1:
        course={}
        course["class"]=i["classname"]
        course["room"]=i["croom"]
        course["con"]=[]
        course["teacher"]=[]
        flage=False
        for j in i["course"]:
            if flage:
                flage=False
                continue
            if j=={}:
                course["con"].append("")
                course["teacher"].append("")
                flage=True
                continue
            course["con"].append(j["stage"])
            course["teacher"].append(j["teacher"])
            flage=True
        data["data"].append(course)
    return data

# 获取可代课老师
def getteacher(request,classname,newstage):
    class_name=classes.filter(name=classname).first()
    if not class_name:
        class_name=outclasses.filter(name=classname)
        stagename = class_name.now_stage.name
    stagename=class_name.now_stage.name
    onestage=stage.filter(name=newstage).first()
    someteacher=teacherstage.filter(stage=onestage)
    oneclasses=classes.filter(name=classname).first()
    teacherlist=[oneclasses.now_teacher.name]
    for i in someteacher:
        oneteacher=teachers.filter(name=i.teacher.name).first()
        if oneteacher.status == "00000000000000":
            teacherlist.append(oneteacher.name)
    teacherlist={"teacherlist":teacherlist}
    return JsonResponse(teacherlist)

# 获取下周日期
def get_N_day():
    today1 = datetime.date.today()
    today2 = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    m1 = calendar.MONDAY
    m2 = calendar.SUNDAY
    while today1.weekday() != m1:
        today1 += oneday
    # today1 += oneday
    # while today1.weekday() != m1:
    #     today1 += oneday
    while today2.weekday() != m2:
        today2 += oneday
    today2 += oneday
    while today2.weekday() != m2:
        today2 += oneday

    nextMonday = today1.strftime("%Y%m%d")
    nextSunday = today2.strftime("%Y%m%d")
    date_list = [d.strftime("%Y-%m-%d") for d in pd.date_range(nextMonday, nextSunday, freq="D")]
    list_date=[]
    for i in date_list:
        one=i.split("-")
        time=["月","日"]
        time.insert(0,one[1])
        time.insert(2,one[2])
        time1="".join(time)
        list_date.append(time1)
    return list_date


# 班级分类
def orderClass(classes):
    order = []
    for i in classes:
        now_long_time=0
        if i.now_long_time:
            now_long_time=1
        order.append(model.predict([[i.education, i.stu_num,i.benke_num,i.dazhuan_num,i.zhongzhuan_num,i.gaozhong_num,i.is_outside,now_long_time]])[0][0])
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
    sortteacher=list(np.argsort(-np.array([i.priority for i in tss])))
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
        class_sheet["classname"] = class_a.name         # 班名
        class_sheet["croom"] = class_a.croom.name       # 教室
        class_sheet["course"] = []                      # 具体每天的课程
        teacher2=class_a.is_teacher2                    # 是否有助教
        now_mode=list(class_a.now_mode.mode)            # 目前上课模式
        # around=now_mode.count("1")
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
            if now_mode[b]=="0":                        # 如果此半天不上课则返回空数据
                halfday = {}
                class_sheet["course"].append(halfday)
                continue
            halfday = {}                                # 半天的阶段和老师
            nowstage = class_a.now_stage  # 当前阶段
            longtime = int(stage.filter(name=nowstage.name).first().hour)  # 当前阶段总共时长
            now_long_time = int(class_a.now_long_time) # 保证每半天的数据更新
            now_teacher=class_a.now_teacher                 # 目前代课老师
            # 如果还没有进入下一个阶段
            if longtime - now_long_time >= 4:           #如果课时差值大于四
                halfday["stage"] = nowstage.name
                halfday["teacher"] = now_teacher.name
                class_sheet["course"].append(halfday)
                state = list(now_teacher.status)
                state[b] = "1"
                str=now_teacher.state = "".join(state)
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
                halfday["stage"] = afterstage.name
                endstages=class_a.endstages.split("-")                     # 已完成阶段
                if endstages[0]=="暂无":
                    class_a.endstages=class_a.now_stage.name
                else:
                    endstages.append(class_a.now_stage.name)
                    new_endstages="-".join(endstages)
                    class_a.endstages=new_endstages
                class_a.save()
                class_a.now_stage = afterstage
                class_a.save()
                class_a.now_long_time = 4
                class_a.save()
                teacherarr, sortteacher = sort_teacher(afterstage)
                for c in sortteacher:
                    c = int(c)
                    if teacherarr[c].status[b] == "1":
                        continue
                    teachersdate = teacherarr[c]
                    status = list(teachersdate.status)
                    status[b] = "1"
                    teachersdate.status = "".join(status)
                    teachersdate.save()
                    halfday["teacher"] = teacherarr[c].name
                    class_a.now_teacher=teacherarr[c]
                    class_a.save()
                    break
                else:
                    halfday["teacher"] = "没有空闲老师"
                class_sheet["course"].append(halfday)
        class_a.week=week+1
        class_a.save()
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
        data1=data.split(",")
        outstage=[]
        for i in data1:
            data2=i.split("-")
            for j in range(int(data2[1])):
                outstage.append(data2[0])
                outstage.append(data2[0])
        data3=outstage
        class_sheet["classname"] = class_a.name         # 班名
        class_sheet["croom"] = class_a.croom            # 教室
        class_sheet["course"] = []                      # 具体每天的课程
        teacher2=class_a.is_teacher2                    # 是否有助教
        week=class_a.week                               # 班级下次上课周数
        if week!=next_week:                             # 是否符合上课周数
            break
        for b in range(len(data3)):                             # 对14个半天进行排课
            halfday={}
            con=data3[b]
            if con=="0":
                class_sheet["course"].append(halfday)
            else:
                halfday["stage"]=con
                major=Major.objects.all().filter(name=con).first()
                teach=teachers.filter(major=major).order_by("-priority")
                for c in teach:
                    status=c.status
                    if status[b]=="0":
                        halfday["teacher"] = c.name
                        class_sheet["course"].append(halfday)
                        status = list(c.status)
                        status[b] = "1"
                        c.status = "".join(status)
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
    class_sheet_list = []                    # 用来存放最终数据
    data = {}                                # 用来存放最终数据
    data["date"]=getWeek()
    data["num"]=getWeek()
    for a in sortList:                       # 按顺序选择班级
        a=int(a)                             # 把numpy元素转换成int
        # print(goon[a].now_long_time)
        class_sheet = {}                     # 某个班的排课数据
        class_a = goon[a]                    # 选中某一个班级
        class_sheet["classname"] = class_a.name         # 班名
        class_sheet["croom"] = class_a.croom.name       # 教室
        class_sheet["course"] = []                      # 具体每天的课程
        teacher2=class_a.is_teacher2                    # 是否有助教
        now_mode=list(class_a.now_mode.mode)            # 目前上课模式
        # around=now_mode.count("1")
        is_end=class_a.is_end                           # 是否结训
        week=class_a.week                               # 班级下次上课周数
        nowstage = class_a.now_stage                    # 当前阶段
        longtime = int(stage.filter(name=nowstage.name).first().hour)  # 当前阶段总共时长
        now_long_time = int(class_a.now_long_time)
        if is_end:                                      # 是否结训
            continue
        if week!=next_week:                             # 是否符合上课周数
            break
        oneroom=classroom.filter(name=class_a.croom.name).first()
        # print(oneroom)
        oneroom.status=1
        oneroom.save()
        for b in range(14):                             # 对14个半天进行排课
            if now_mode[b]=="0":                        # 如果此半天不上课则返回空数据
                halfday = {}
                class_sheet["course"].append(halfday)
                continue
            halfday = {}                                # 半天的阶段和老师
            nowstage = class_a.now_stage  # 当前阶段
            longtime = int(stage.filter(name=nowstage.name).first().hour)  # 当前阶段总共时长
            now_long_time = int(class_a.now_long_time) # 保证每半天的数据更新
            now_teacher=class_a.now_teacher                 # 目前代课老师
            # 如果还没有进入下一个阶段
            if longtime - now_long_time >= 4:           #如果课时差值大于四
                halfday["stage"] = nowstage.name
                halfday["teacher"] = now_teacher.name
                class_sheet["course"].append(halfday)
                status = list(now_teacher.status)
                status[b] = "1"
                now_teacher.status = "".join(status)
                now_teacher.save()
                class_a.now_long_time = int(class_a.now_long_time) + 4
                class_a.save()
            else:                                       # 如果不够半天课时
                stages,sortarr = bToA(nowstage)         # 获得下一阶段的优先级排序下标
                if len(sortarr)==0:                      # 不存在后置阶段说明结训
                    class_a.is_end = 1
                    class_a.save()
                    oneroom = classroom.filter(name=class_a.croom.name).first()
                    oneroom.status = 0
                    oneroom.save()
                    endlist=class_a.endstages.split("-")
                    endlist.append(class_a.now_stage.name)
                    new_endstages = "-".join(endlist)
                    class_a.endstages = new_endstages
                    class_a.save()
                    break
                # afterstage = stages[int(sortarr[0])].next_course # 获取优先级最高的下一阶段
                afterstage=""
                for after in sortarr:
                    after=int(after)
                    afterstage=stages[after].next_course
                    endlist=class_a.endstages.split("-")
                    if afterstage in endlist:
                        continue
                    else:
                        afterstage=afterstage
                halfday["stage"] = afterstage.name
                endstages=class_a.endstages.split("-")                     # 已完成阶段
                if endstages[0]=="暂无":
                    class_a.endstages=class_a.now_stage.name
                else:
                    endstages.append(class_a.now_stage.name)
                    new_endstages="-".join(endstages)
                    class_a.endstages=new_endstages
                class_a.save()
                class_a.now_stage = afterstage
                class_a.save()
                class_a.now_long_time = 4
                class_a.save()
                teacherarr, sortteacher = sort_teacher(afterstage)
                for c in sortteacher:
                    c = int(c)
                    if teacherarr[c].status[b] == "1":
                        continue
                    teachersdate = teacherarr[c]
                    status = list(teachersdate.status)
                    status[b] = "1"
                    teachersdate.status = "".join(status)
                    teachersdate.save()
                    halfday["teacher"] = teacherarr[c].name
                    class_a.now_teacher=teacherarr[c]
                    class_a.save()
                    break
                else:
                    halfday["teacher"] = "没有空闲老师"
                class_sheet["course"].append(halfday)
        # class_a.week=week+1
        # class_a.save()
        print(class_sheet)
        class_sheet_list.append(class_sheet)
    return class_sheet_list


# 不保存课表
def nosaveorder():
    goon = classes  # 筛选符合条件班级
    next_week = getWeek()                    # 获得下周的周数
    sortList=orderClass(goon)                # 进行优先级排序获得排序下标
    class_sheet_list = []                    # 用来存放最终数据
    data = {}                         # 用来存放最终数据
    data["date"]=getWeek()
    data["num"]=getWeek()
    for a in sortList:                       # 按顺序选择班级
        a=int(a)                             # 把numpy元素转换成int
        class_sheet = {}                     # 某个班的排课数据
        class_a = goon[a]                    # 选中某一个班级
        class_sheet["classname"] = class_a.name         # 班名
        # classes.filter(name=class_sheet["classname"]).first().now_stage.name
        # print(classes.filter(name='MUIDF1906').first().now_long_time)
        class_sheet["croom"] = class_a.croom.name       # 教室
        class_sheet["course"] = []                      # 具体每天的课程
        now_mode=list(class_a.now_mode.mode)            # 目前上课模式
        is_end=class_a.is_end                           # 是否结训
        week=class_a.week                               # 班级下次上课周数
        if is_end:                                      # 是否结训
            continue
        if week!=next_week:                             # 是否符合上课周数
            break
        oneroom=classroom.filter(name=class_a.croom.name).first()
        oneroom.status=1
        oneroom.save()
        for b in range(14):                             # 对14个半天进行排课
            if now_mode[b]=="0":                        # 如果此半天不上课则返回空数据
                halfday = {}
                class_sheet["course"].append(halfday)
                continue
            halfday = {}                                # 半天的阶段和老师
            # nowstage = class_a.now_stage  # 当前阶段
            # now_long_time = int(class_a.now_long_time) # 保证每半天的数据更新
            nowstage=classes.filter(name='MUIDF1906').first().now_stage
            longtime = int(stage.filter(name=nowstage.name).first().hour)  # 当前阶段总共时长
            now_long_time=classes.filter(name='MUIDF1906').first().now_long_time
            print('2',now_long_time)
            now_teacher=classes.filter(name='MUIDF1906').first().now_teacher
            # now_teacher=class_a.now_teacher                 # 目前代课老师
            # 如果还没有进入下一个阶段
            if longtime - now_long_time >= 4:           #如果课时差值大于四
                halfday["stage"] = nowstage.name
                halfday["teacher"] = now_teacher.name
                class_sheet["course"].append(halfday)
                status = list(now_teacher.status)
                status[b] = "1"
                now_teacher.status = "".join(status)
                now_teacher.save()
                class_a.now_long_time = int(now_long_time) + 4
                class_a.save()
            else:                                       # 如果不够半天课时
                stages,sortarr = bToA(nowstage)         # 获得下一阶段的优先级排序下标
                if len(sortarr)==0:                      # 不存在后置阶段说明结训
                    # class_a.is_end = 1
                    # class_a.save()
                    oneroom = classroom.filter(name=class_a.croom.name).first()
                    oneroom.status = 0
                    oneroom.save()
                    # endlist=class_a.endstages.split("-")
                    # endlist.append(class_a.now_stage.name)
                    # new_endstages = "-".join(endlist)
                    # class_a.endstages = new_endstages
                    # class_a.save()
                    break
                afterstage=""
                for after in sortarr:
                    after=int(after)
                    afterstage=stages[after].next_course
                    endlist=class_a.endstages.split("-")
                    if afterstage in endlist:
                        continue
                    else:
                        afterstage=afterstage
                halfday["stage"] = afterstage.name
                # endstages=class_a.endstages.split("-")                     # 已完成阶段
                # if endstages[0]=="暂无":
                #     pass
                    # class_a.endstages=class_a.now_stage.name
                # else:
                #     pass
                    # endstages.append(class_a.now_stage.name)
                    # new_endstages="-".join(endstages)
                    # class_a.endstages=new_endstages
                class_a.save()
                class_a.now_stage = afterstage
                class_a.save()
                class_a.now_long_time = 4
                class_a.save()
                teacherarr, sortteacher = sort_teacher(afterstage)
                for c in sortteacher:
                    c = int(c)
                    if teacherarr[c].status[b] == "1":
                        continue
                    teachersdate = teacherarr[c]
                    status = list(teachersdate.status)
                    status[b] = "1"
                    teachersdate.status = "".join(status)
                    teachersdate.save()
                    halfday["teacher"] = teacherarr[c].name
                    class_a.now_teacher=teacherarr[c]
                    class_a.save()
                    break
                else:
                    halfday["teacher"] = "没有空闲老师"
                class_sheet["course"].append(halfday)
        # class_a.week=week+1
        # class_a.save()
        print(class_sheet)
        class_sheet_list.append(class_sheet)
    return class_sheet_list


# 优先级数据录入
# def orderinput():
#     data='{"a":"b"}'