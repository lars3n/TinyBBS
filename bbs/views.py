#coding: utf-8
import datetime
import json, os
from itertools import chain

from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms.utils import ErrorList
from django.utils.html import escape, strip_tags, remove_tags
from django.db.models import Q

from captcha.models import CaptchaStore  
from captcha.helpers import captcha_image_url 

from bbs.form import *
from bbs.models import *
from bbs.biz import *
from django.conf import settings


def index(request):
    try:
        user_bbs = BBS.objects.filter(bbs_author__user=request.user)
    except:
        user_bbs = None
    allBbsCount = BBS.objects.all().count()
    allCommentCount = Comments.objects.all().count()
    bbsTodayCount = BBS.objects.filter(created_at__contains=datetime.datetime.now().strftime("%Y-%m-%d")).count()
    userRegisterCount = User.objects.all().count()

    bbs_list = BBS.objects.all()[:20]
    categories = Category.objects.all()
    program_cate = Category.objects.filter(category_class=1)

    newMsg = 0
    try:
        for m in request.user.bbs_user.msg_to.all():
            if m.status == 1:
                newMsg += 1
    except:
        newMsg = 0

    return render_to_response("index.html",
        {'bbs_list': bbs_list,
         #"user_bbs": user_bbs,
         "user": request.user,
         "categories": categories,
         "program_cate": program_cate,
         'allBbsCount': allBbsCount,
         "allCommentCount": allCommentCount,
         "bbsTodayCount": bbsTodayCount,
         "userRegisterCount": userRegisterCount,
         "newMsg": newMsg,},
         context_instance = RequestContext(request)
        )

def category(request, category_id):
    bbs_list = BBS.objects.filter(bbs_category__id=category_id)[:20]
    categories = Category.objects.all()
    cur_cate = Category.objects.get(id=category_id)

    return render_to_response("index.html",
        {'bbs_list': bbs_list,
         "user": request.user,
         "categories": categories,
         "cur_cate": cur_cate,},
        )

def recent(request, pageNo=None):
    try:
        pgNo = int(pageNo)
    except:
        pgNo = 1

    if pgNo == 0:
        pgNo = 1

    categories = Category.objects.all()
    bbs_list = BBS.objects.all()
    p = Paginator(bbs_list, 10)

    if pgNo > p.num_pages:
        pgNo = p.num_pages
    curPage = p.page(pgNo)
    allBbsCount = BBS.objects.all().count()

    return render_to_response("recent.html",
        {"user": request.user,
         "categories": categories,
         'curPage': curPage,
        'pcount': p.num_pages,
        'allBbsCount': allBbsCount,
        },
        context_instance = RequestContext(request))

def bbs_detail(request, bbs_id=None, pageNo=None):
    try:
        pgNo = int(pageNo)
    except:
        pgNo = 1

    if pgNo == 0:
        pgNo = 1

    bbs = get_object_or_404(BBS, id=bbs_id)
    bbs.view_count += 1
    bbs.save()
    categories = Category.objects.all()
    form = ReplayForm()
    try:
        bbs_comments = Comments.objects.filter(bbs_id=bbs_id)
        p = Paginator(bbs_comments, 20)
        if pgNo > p.num_pages:
            pgNo = p.num_pages
        curPage = p.page(pgNo)
    except:
        curPage = None

    #time_delta = bbs.created_at.replace(tzinfo=None)-datetime.datetime.now()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 
    # 判斷當前文章是否已被收藏  
    favorited = False
    try:
        for b in request.user.bbs_user.favorites.all():
            if unicode(b.id) == bbs_id:
                favorited = True
    except:
        favorited = False

    return render_to_response("bbs_detail.html",
        {"bbs": bbs,
        "curPage": curPage,
        "categories": categories,
        "form": form,
        "now": now,
        'pcount': p.num_pages,
        'bbs_comments': bbs_comments,
        'favorited': favorited,
        },
        context_instance = RequestContext(request),
        )

@csrf_exempt
@login_required
def replays(request, bbs_id):      
    if request.is_ajax():
        form = ReplayForm(request.POST)
        content = request.POST.get('content', None)
        # 過濾掉不安全標籤
        content = remove_tags(content, "script html body")
        if form.is_valid() and content and bbs_id:
            Comments.objects.create(
                user_id = BBS_user.objects.get(user__username=request.user),
                bbs_id = BBS.objects.get(id=bbs_id),
                pub_date = datetime.datetime.now(),
                cmt_content = content
                )
            cur_user = BBS_user.objects.get(user__username=request.user)
            # 傳入用戶頭像地址，用於ajax
            avatar = unicode(cur_user.avatar)
            return  HttpResponse(json.dumps(
                {"content": content,
                 "avatar": avatar,
                 "signature": cur_user.signature
                }))
        return None

    return HttpResponseRedirect(reverse("home"))


def login(request):
    hashkey = CaptchaStore.generate_key()  
    image_url = captcha_image_url(hashkey)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse("home"))
            form.errors['password'] = "用户不存在或密码错误"
            return render_to_response("login.html",
                {'form': form, "hashkey": hashkey, "image_url": image_url},
                context_instance = RequestContext(request))
        return render_to_response("login.html",
                {'form': form, "hashkey": hashkey, "image_url": image_url},
                context_instance = RequestContext(request))
    form = LoginForm()
    return render_to_response("login.html",
        {'form': form, "hashkey": hashkey, "image_url": image_url,},
        context_instance = RequestContext(request))

@login_required
def logout(request):
    user = request.user
    auth.logout(request)
    return HttpResponseRedirect(reverse("home"))

def register(request):
    hashkey = CaptchaStore.generate_key()  
    image_url = captcha_image_url(hashkey)
    if request.method == 'POST':
        form = RegisterForm(request.POST)       
        if form.is_valid():
            userBiz = UserBiz()
            error_dict = userBiz.userValidate(form)

            if error_dict:
                for errorName in error_dict.keys():
                    form.errors[errorName] = error_dict[errorName]
                hashkey = CaptchaStore.generate_key()  
                image_url = captcha_image_url(hashkey)
                return render_to_response("register.html",
                    {"form": form, "hashkey": hashkey, "image_url": image_url,},
                    context_instance = RequestContext(request)
                    )

            cd = form.cleaned_data
            username = cd['username']
            password = cd['password1']
            new_user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=cd['email']
                    )

            userBiz.save(new_user)
            BBS_user.objects.create(user=new_user, )

            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
            return HttpResponseRedirect(reverse('home'))
        return render_to_response("register.html",
            {"form": form, "hashkey": hashkey, "image_url": image_url,},
            context_instance = RequestContext(request)
            )

    form = RegisterForm()
    return render_to_response("register.html",
        {"form": form, "hashkey": hashkey, "image_url": image_url,},
        context_instance = RequestContext(request)
        )

@login_required
def bbs_pub(request):
    categories = Category.objects.all()
    hashkey = CaptchaStore.generate_key()  
    image_url = captcha_image_url(hashkey)  
    if request.method == 'POST':
        form = BbsPubForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            bbsBiz = BbsBiz()         
            bbs_category = bbsBiz.getCategory(cd['bbs_category'])
            bbs_author = bbsBiz.getBbsAuthorByReq(request.user)

            if bbs_category and bbs_author:
                bbs_content = remove_tags(cd['bbs_content'], "html body script")
                BBS.objects.create(
                    bbs_title = cd['bbs_title'],
                    bbs_content = bbs_content,
                    view_count = 0,
                    bbs_category = bbs_category,
                    bbs_author = bbs_author,
                )
                return HttpResponseRedirect(reverse('home'))      
        return render_to_response("bbs_pub.html", {"form": form,
            "categories": categories,
            "hashkey": hashkey, "image_url": image_url},
            context_instance = RequestContext(request))

    form = BbsPubForm()
    return render_to_response("bbs_pub.html",
        {"form": form, "categories": categories,
        "hashkey": hashkey, "image_url": image_url},
        context_instance = RequestContext(request))

@login_required
def delete(request, bbs_id=None):
    try:
        BBS.objects.get(id=bbs_id).delete()
        return HttpResponse('''<meta http-equiv="refresh" content="3;url=/">\
            <h2>Delete Succesfully</h2>''')
    except:
        return HttpResponse('''<meta http-equiv="refresh" content="3;url=/">\
            <h2>Delete Failed</h2>''')

# 返回用于發送郵件的頁面
def forgot(request):
    # 用于刷新验证码
    hashkey = CaptchaStore.generate_key()  
    image_url = captcha_image_url(hashkey)
    if request.method == 'POST':
        form = ForgotForm(request.POST)       
        if form.is_valid():
            email = request.POST.get("email")
            try:
                user = User.objects.get(email=email)
            except:
                user = None
                form.errors['email'] = '此邮箱未注册'
            if user:
                resetBiz = ResetPwdBiz()
                resetBiz.send_email(email)

                return render_to_response("forget.html",
                    {"success": form},
                    context_instance = RequestContext(request)
                    )
            return render_to_response("forget.html",
                {"hashkey": hashkey, "image_url": image_url, "form": form},
                context_instance = RequestContext(request)
                )
        return render_to_response("forget.html",
            {"hashkey": hashkey, "image_url": image_url, "form": form},
            context_instance = RequestContext(request)
            )
    return render_to_response("forget.html",
        {"hashkey": hashkey, "image_url": image_url},
        context_instance = RequestContext(request)
        )

# 返回重置密碼的頁面，及處理重置密碼事項
def reset(request, reset_code):
    try:
        user = BBS_user.objects.get(reset_password=reset_code)
    except:
        user = None

    if user and request.method == 'POST':
        form = ResetPwdForm(request.POST)
        if form.is_valid():
            password1 = form['password1'].value()
            password2 = form['password2'].value()
            if password1 != password2:
                form.errors['password2'] = '两次密码不一致'
                return render_to_response('reset_pwd.html',
                    {'form': form},
                    context_instance = RequestContext(request))
            user.reset_password = ''        #将重置密码的code 清空
            user.save()
            cd = form.cleaned_data
            user2 = User.objects.get(username=user)
            user2.set_password(cd['password1'])
            user2.save()
            return render_to_response('reset_pwd.html', {'success': form},
                            context_instance = RequestContext(request))
        return render_to_response('reset_pwd.html', {'form': form},
                            context_instance = RequestContext(request))
    if user:
        form = ResetPwdForm()
        return render_to_response('reset_pwd.html',
            {'form': form},
            context_instance = RequestContext(request))
    return HttpResponseRedirect(reverse('home'))

@login_required  
def change_info(request):
    pwdForm = ChangePwdForm()
    infoForm = ChangeInfoForm()
    avatarForm = ChangeAvatarForm()
    cur_user = BBS_user.objects.get(user__username=request.user)
    if request.method == "POST":
        form = ChangeInfoForm(request.POST)
        if form.is_valid():
            new_sig = form.cleaned_data['signature']
            new_intro = form.cleaned_data['user_intro']

            try:
                user = BBS_user.objects.get(user__username=request.user)
                user.signature = new_sig
                user.user_intro = new_intro
                user.save()
                return HttpResponseRedirect(reverse("change_info"))
            except:
                return HttpResponse("<h1>更改失败</h1>")

        return render_to_response("change_info.html",
                    {"cur_user": cur_user, 
                     "pwdForm": pwdForm,
                     "infoForm": form,
                     "avatarForm": avatarForm},
                    context_instance = RequestContext(request))

    infoForm = ChangeInfoForm()
    cur_user = BBS_user.objects.get(user__username=request.user)
    return render_to_response("change_info.html",
        {"cur_user": cur_user, 
         "infoForm": infoForm,
        },
        context_instance = RequestContext(request))


@login_required  
def change_avatar(request):
    if request.method == 'POST':  
        content = request.FILES['avatar']        
        user = BBS_user.objects.get(user__username=request.user)
        oldAvatar = user.avatar
        oldAvatarPath = "%s/%s" % (settings.MEDIA_ROOT.replace('\\','/'), oldAvatar)
        if os.path.exists(oldAvatarPath) and oldAvatar != "avatar/default_avatar.jpg":
            os.remove(oldAvatarPath)
        user.avatar = content
        user.save()
        return HttpResponseRedirect(reverse('change_avatar'))

    avatarForm = ChangeAvatarForm()
    cur_user = BBS_user.objects.get(user__username=request.user)
    return render_to_response("change_avatar.html",
        {"cur_user": cur_user},
        context_instance = RequestContext(request))

@login_required
def change_password(request):
    info = None
    if request.method == "POST":
        form = ChangePwdForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data     
            orgi_pwd = cd['ori_password']
            pwd1 = cd['new_password_1']
            pwd2 = cd['new_password_2']

        user = auth.authenticate(username=request.user, password=orgi_pwd)
        if user is None:
            form.errors['ori_password'] = "原密码错误"
        if pwd1 != pwd2:
            form.errors['new_password_2'] = "两次密码不一致"  

        if pwd1 == pwd2 and user:
            user = User.objects.get(username=request.user)
            user.set_password(pwd1)
            user.save()

            #user = auth.authenticate(username=request.user, password=pwd1)
            #auth.login(request, user)
            # 修改完密码，让用户重新登录
            auth.logout(request)
            return HttpResponseRedirect(reverse("info"))
               
        return render_to_response("change_pwd.html", {"form": form},
            context_instance = RequestContext(request))
    
    return render_to_response("change_pwd.html",
        context_instance = RequestContext(request))

def info(request):
    return render_to_response("info.html")

def user_profile(request, userId=None):
    user_prof = BBS_user.objects.get(user__id=userId)
    isFollowed = Follow.objects.filter(fans=request.user.bbs_user).filter(follow=user_prof)

    return render_to_response("user_profile.html",
        {"user_prof": user_prof,
         "isFollowed": isFollowed },
        context_instance = RequestContext(request))

def new_captcha(request):
    if request.method == 'GET':
        csn = CaptchaStore.generate_key()
        cimageurl = captcha_image_url(csn)
        return HttpResponse(cimageurl)

@login_required
def favor_add(request, bbsId):
    bbs = BBS.objects.get(id=bbsId)
    cur_user = BBS_user.objects.get(user__username=request.user)
    if cur_user.favorites.filter(id=bbsId):
        return HttpResponse("已经收藏过了")
    cur_user.favorites.add(bbs)
    return HttpResponseRedirect(reverse('bbs_detail', args=[bbsId]))

@login_required
def favor_del(request, bbsId):
    bbs = BBS.objects.get(id=bbsId)
    cur_user = BBS_user.objects.get(user__username=request.user)

    cur_user.favorites.remove(bbs)
    return HttpResponseRedirect(reverse('bbs_detail', args=[bbsId]))

@login_required
def favorites(request):
    return render_to_response("favorites.html",
        {'user': request.user})

@login_required
def message(request):
    msgFrom = Message.objects.filter(msg_from__user=request.user)
    msgTo = Message.objects.filter(msg_to__user=request.user)
    msg = msgFrom | msgTo

    # 獲取跟用戶相關的私信
    List = [i.dialog.id for i in msg]
    # 獲取會話列表
    dialogList = [MsgDialog.objects.get(id=i) for i in set(List)]
    # 獲取列表中每個會話的最新一條私信
    dialogList2 = [i.message_set.all().order_by('created_at').reverse()[0] for i in dialogList]

    return render_to_response("message.html",
        {'dialogList': dialogList2,
         'user': request.user})

@login_required
def message_send(request, toId):

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            msgContent = cd['content']
            msgTo = BBS_user.objects.get(user__id=toId)

            msgContent = MsgContent.objects.create(
                message_text=msgContent)            

            # 獲取同時跟當前用戶及發送用戶相關的會話
            m1 = Message.objects.filter(msg_from__user__id=toId).filter(msg_to__user__id=request.user.id)
            m2 = Message.objects.filter(msg_from__user__id=request.user.id).filter(msg_to__user__id=toId)

            # 若兩個用戶之前曾有過會話，則使用舊的會話，否則創建新的會話
            if m1:              
                msgDialog = MsgDialog.objects.get(id=m1[0].dialog.id)
            elif m2:
                msgDialog = MsgDialog.objects.get(id=m2[0].dialog.id)
            else:
                msgDialog = MsgDialog.objects.create()

            Message.objects.create(
                msg_content=msgContent,
                msg_from=request.user.bbs_user,
                msg_to=msgTo,
                dialog=msgDialog,
                status=1)

            return HttpResponseRedirect(reverse('user_profile', args=[toId]))

    return HttpResponse("发送失败")

@login_required
def message_show(request, dialogId):
    msg = Message.objects.filter(dialog__id=dialogId)
    msg1 = msg[0]
    for m in msg:
        m.status=0          # 將私信狀態標記為已讀
        m.save()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            msgContent = cd['content']
            msgDialog = MsgDialog.objects.get(id=dialogId)

            # 獲取當前會話對象
            if msg1.msg_from.user.username == request.user.username:
                msgTo = msg1.msg_to
            else:
                msgTo = msg1.msg_from

            msgContent = MsgContent.objects.create(
                message_text=msgContent)            

            msg_from = BBS_user.objects.get(user__username=request.user)
            
            Message.objects.create(
                msg_content=msgContent,
                msg_from=msg_from,
                msg_to=msgTo,
                dialog=msgDialog,
                status=1)
            return HttpResponseRedirect(reverse('message_show', args=[dialogId]))

    return render_to_response('message_show.html',
        {'msg': msg,
         'user': request.user,
         'msg1': msg1},
         context_instance = RequestContext(request))

@login_required
def follow(request):
    myFollow = Follow.objects.filter(fans=request.user.bbs_user)
    followList = []
    followBbsList = []
    followBbsList2 = []
    for i in myFollow:
        for f in i.follow.all():
            followList.append(f)
            followBbsList = chain(followBbsList, f.bbs_set.all())

    # django 模板不支持chain()函數返回的迭代對象，所以用list重新保存
    for i in followBbsList:
        followBbsList2.append(i)

    return render_to_response('follow.html',
        {'user': request.user,
         'followList': followList,
         'followBbsList': followBbsList2})

@login_required
def follow_add(request, userId):
    fans = BBS_user.objects.get(user__username=request.user)
    follow = BBS_user.objects.get(user__id=userId)
    f = Follow.objects.create()
    f.fans.add(fans)
    f.follow.add(follow)
    f.save()

    return HttpResponseRedirect(reverse('user_profile', args=[userId]))

@login_required
def follow_del(request, userId):
    fans = BBS_user.objects.get(user__username=request.user)
    follow = BBS_user.objects.get(user__id=userId)
    f = Follow.objects.filter(fans=fans).filter(follow=follow)
    f.delete()

    return HttpResponseRedirect(reverse('user_profile', args=[userId]))

@login_required
def fans(request):
    myFans = Follow.objects.filter(follow=request.user.bbs_user)
    fansList = []
    for i in myFans:
        for f in i.fans.all():
            fansList.append(f)

    return render_to_response("fans.html",
        {"user": request.user,
         "fansList": fansList,
         })

def search(request):
    if request.method == 'POST':
        kw = request.POST.get('keyword', None)
        Bbs = None
        if kw:
            Bbs = BBS.objects.all().filter(Q(bbs_title__contains=kw)|
                Q(bbs_summary__contains=kw)).exclude(bbs_title='welcome')

        return render_to_response('search.html',
            {'bbses': Bbs,
            'keyword': kw,
            'user': request.user})
    else:
        return HttpResponse('<h1>查询失败</h1>')

