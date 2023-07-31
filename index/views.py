from django.shortcuts import render, redirect
from .models import Videos, Favorites, Views, get_short_id
from login.models import Users
from django.contrib.auth import logout
from django.http import HttpResponse, JsonResponse, FileResponse
from django.contrib import messages

# Create your views here.

def index(request):
    '''网站主页的视图函数'''
    if request.method == "GET":
        var = {}
        videos = list(Videos.objects.filter(state='n').order_by('-view_counts').values())
        var.update({'videos':videos})
        user = request.user # 获取当前用户
        if user.username != '':
            is_user = '1'
        else:
            is_user = '0'
        var.update({'is_user':is_user})
        var.update({'user':user})
        return render(request, 'index.html', context=var)
    
    elif request.method == 'POST':
        var = {}
        user = request.user # 获取当前用户
        if user.username != '':
            is_user = '1'
        else:
            is_user = '0'
        var.update({'is_user':is_user})
        var.update({'user':user})

        form_id = request.POST.get("formid",'')
        if form_id == '1':
            # logout()，会清理 session
            logout(request)
            # messages.error(request, '成功登出')
            return redirect('/index/')
        elif form_id == '0':
            search = request.POST.get("search",'')
            videos_ser = list(Videos.objects.filter(title__icontains=search, state='n').values())
            var.update({'videos':videos_ser})
            return render(request, 'index.html', context=var)

def upload_video(request):
    '''用户上传视频'''
    var = {}
    if request.method == "GET":
        return render(request, 'upload_video.html', context=var)
    elif request.method == 'POST':
        # 变量获取
        video_title = request.POST.get("video_title", "")
        video_sum = request.POST.get("video_sum", "")
        video_file = request.FILES.get("video_file",'')
        video_cover = request.FILES.get("video_cover",'')
        user = request.user

        if not user:  # 用户未登录
            return render(request, 'upload_video.html', context=var)
        
        video_exist = '0'
        if Videos.objects.filter(title=video_title):
            video_temp = Videos.objects.filter(title=video_title).get()  # 提取有相同标题的视频
        else:
            video_exist = '1'
                
        if video_exist == '1' or user.id != video_temp.author.id:  # 不是本人上传的视频
            video_id = get_short_id()  # 获取一个随机的视频ID
            while Videos.objects.filter(id=video_id):
                video_id = get_short_id()
            # 将视频保存
            video_obj = Videos.objects.create(id=video_id, author=user, title=video_title, sum=video_sum, address=video_file, cover=video_cover, state='n')
            if video_obj:
                messages.error(request, '上传成功')
                return render(request, 'upload_video.html', context=var)
        else:  # 是本人上传的视频，对原有视频做修改
            video_obj =Videos.objects.create(author=user, title=video_title, sum=video_sum, address=video_file, cover=video_cover, state='n')
            if video_obj:
                messages.error(request, '上传成功')
                return render(request, 'upload_video.html', context=var)
        
    messages.error(request, '上传失败')
    return render(request, 'upload_video.html', context=var)

def video_play(request,v_id):
    '''视频播放'''
    if request.method == "GET":
        var = {}
        video = Videos.objects.filter(id=v_id).get()
        var.update({'video':video})
        user = request.user # 获取当前用户
        if user.username != '':
            is_user = '1'
        else:
            is_user = '0'
        var.update({'is_user':is_user})
        var.update({'user':user})

        if is_user == '0':
            pass
        elif not Views.objects.filter(user_src=user, video=video):  # 用户未观看过
            Views.objects.create(video=video, user_src=user)  # 创建观看记录
            vc = Views.objects.filter(video=video).count()
            video.view_counts = vc
            video.save()
        else:  # 用户观看过该视频
            view = Views.objects.filter(user_src=user, video=video).get()
            view.save()  # 更新观看时间

        response = render(request, 'video_play.html', context=var)
        try:
            video_file = open("/media/"+str(video.address), 'rb')
            response = FileResponse(video_file, content_type='video/mp4')
        except FileNotFoundError:
            return render(request, 'video_play.html', context=var)
        
        return response
    
    elif request.method == 'POST':
        var = {}
        video = Videos.objects.filter(id=v_id).get()
        var.update({'video':video})
        user = request.user # 获取当前用户
        if user.username != '':
            is_user = '1'
        else:
            is_user = '0'
        var.update({'is_user':is_user})
        var.update({'user':user})
        form_id = request.POST.get("formid",'')
        if form_id == '1':  # 处理收藏的表单
            # 获取表单变量
            user = request.user
            video = Videos.objects.filter(id=v_id).get()
            if not Favorites.objects.filter(user_src=user, video=video):  # 未建立过收藏
                Favorites.objects.create(video=video, user_src=user)  # 创建收藏
                fc = Favorites.objects.filter(video=video).count()
                video.favorites_counts = fc
                video.save()
                messages.error(request, '收藏成功')
                return render(request, 'video_play.html', context=var)
            else:
                messages.error(request, '收藏失败')
                return render(request, 'video_play.html', context=var)
        elif form_id == '0':
            search = request.POST.get("search",'')
            videos_ser = list(Videos.objects.filter(title__icontains=search, state='n').values())
            var.update({'videos':videos_ser})
            return render(request, 'index.html', context=var)