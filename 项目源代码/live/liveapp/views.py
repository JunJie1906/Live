# coding=utf-8
from django.shortcuts import render,redirect,get_object_or_404
from . import forms
import os
import psutil


import login.models,liveapp.models

def get_rtmp_name():
    f = open('prop.txt', 'r',encoding='utf-8')
    a = f.read().split('\n')
    return a[0]

def get_video_name():
    f = open('prop.txt', 'r',encoding='utf-8')
    a = f.read().split('\n')
    return a[1]
def get_audio_name():
    f = open('prop.txt', 'r',encoding='utf-8')
    a = f.read().split('\n')
    return a[2]
def gen_9_numbers(s):
    return str(abs(hash(s)))[:9]

def ffmpeg(id):

    os.system(
              'ffmpeg.exe '
              '-f dshow -i video="'
              +get_video_name()+
              '"  '
              '-f dshow -i audio="'
              +get_audio_name()+
              '" '
              '-vcodec libx264 '
              '-preset:v ultrafast '
              '-tune:v zerolatency '
              '-f flv '
              +get_rtmp_name()+
              '/live/'+id)

def shareScreen(id):
    os.system('ffmpeg.exe -f gdigrab -video_size 1920x1080 '
              '-framerate 15 -i desktop -pix_fmt yuv420p '
              '-codec:v libx264 -bf 0 -g 300 -f flv '
              'rtmp://localhost:1935/live/'+id)


def live(request,pk):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    username = request.session.get('user_name')

    Live = get_object_or_404(liveapp.models.Live, pk=pk)
    is_main = False
    if username == Live.creater.name:
        is_main = True
    roomID = Live.roomId
    request.session["cur_roomId"] = roomID

    return render(request,'liveapp/live.html',locals())

def openShareScreen(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    username = request.session.get('user_name')
    creater = login.models.User.objects.get(name=username)
    live = liveapp.models.Live.objects.get(creater=creater)
    id = live.roomId
    # t = threading.Thread(target=ffmpeg, args=(id,))
    shareScreen(id)
    return redirect(live.get_absolute_url())

def openCamera(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    username = request.session.get('user_name')
    creater = login.models.User.objects.get(name=username)
    live = liveapp.models.Live.objects.get(creater=creater)
    id = live.roomId
    # t = threading.Thread(target=ffmpeg, args=(id,))
    ffmpeg(id)
    return redirect(live.get_absolute_url())



def closeCamera(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    username = request.session.get('user_name')
    creater = login.models.User.objects.get(name=username)
    live = liveapp.models.Live.objects.get(creater=creater)
    lst = psutil.pids()
    for i in lst:
        # print("=============1==================")
        process = psutil.Process(i)
        # print(process.name())
        # print("=============2==================")
        if process.name() == 'ffmpeg.exe':
            print(process.name())
            print("=============3==================")
            process.kill()
            break
    return redirect(live.get_absolute_url())

def launch(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')

    if request.method=="POST":
        launchForm = forms.launchForm(request.POST)

        if launchForm.is_valid():
            username = request.session.get('user_name')
            creater = login.models.User.objects.get(name=username)
            LiveName = launchForm.cleaned_data.get('LiveName')
            roomID = gen_9_numbers(username+LiveName)
            same_roomID = liveapp.models.Live.objects.filter(roomId=roomID)
            if same_roomID:
                roomID = gen_9_numbers(username)
                same_roomID = liveapp.models.Live.objects.filter(roomId=roomID)
            try:
                newLive = liveapp.models.Live()
                newLive.creater = creater
                newLive.roomId = roomID
                newLive.roomName = LiveName
                newLive.save()
                # t = threading.Thread(target=ffmpeg(roomID))
                # t.start()

            except:
                erro_msg = "您已经有一个正在直播的直播间了！！"
                return render(request,'liveapp/launch.html',locals())

            return redirect(newLive.get_absolute_url())

    launchForm = forms.launchForm()
    return render(request,'liveapp/launch.html',locals())


def FindLive(request):
    if not request.session.get('is_login',None):
        return redirect('/login/')

    if request.method=="POST":
        RoomForm = forms.getRoomForm(request.POST)
        if RoomForm.is_valid():

            roomID = RoomForm.cleaned_data.get('roomID')

            try:
                room = liveapp.models.Live.objects.get(roomId=roomID)
            except:
                erro_message = '不存在此房间！请重新输入'
                return render(request, 'liveapp/FindLive.html',locals())
            request.session["cur_roomId"] = roomID
            return redirect(room.get_absolute_url())

    RoomForm = forms.getRoomForm()
    return render(request,'liveapp/FindLive.html',locals())

def MyLive(request):
    if not request.session.get('is_login',None):
        return redirect('/login/')
    username = request.session.get('user_name')
    user = login.models.User.objects.get(name=username)
    try:
        live = liveapp.models.Live.objects.get(creater=user)
    except:
        return redirect('/launch/')
    return redirect(live.get_absolute_url())

def closelive(request):
    if not request.session.get('is_login',None):
        return redirect('/login/')
    closeCamera(request)
    roomId=request.session.get('cur_roomId')
    try:
        room = liveapp.models.Live.objects.get(roomId=roomId)
    except:
        return redirect('/mylive/')
    room.delete()
    return redirect('/launch/')
