from django.shortcuts import render
from .models import Classes,OutClasses
from direction.models import Stage
from orderCla.order_classes import model

classes=Classes.objects.all()
stage=Stage.objects.all()
outclasses=OutClasses.objects.all()




# Create your views here.
def index(request):
    goon=classes.exclude(now_long_time=0) #当前阶段未结束班级
    gonext=classes.filter(now_long_time=0) #当前阶段已结束班级
    print(outclasses)

    return render(request,'uekClass/index.html')



# 班级排序:先进行分类1，当前阶段没有结束的2，校外课3，换阶段班和新开班
#           然后对1，3类进行班级排序最后整合排序的班级
def orderClass():
    classes.filter()