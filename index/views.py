import json

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import User,Goods,GoodsType

# Create your views here.
#首页
def index(request):
    return render(request,'index.html')

def check_login(request):
    #检查登录状态
    #1 检查session
    if 'uphone' in request.session and 'uid' in \
            request.session and 'uname' in request.session:
        uname = request.session.get('uname')
        # 登录状态返回
        res = {'loginState':1,'username':uname}
        return JsonResponse(res)
    #2 如果session没有数据,则检查Cookie
    #3-1 如果Cookie有,需要把Cookie数据回写给session
    #3-2 如果Cookie没有,用户肯定没有
    if 'uphone' in request.COOKIES and 'uid' in \
            request.COOKIES and 'uname' in request.COOKIES:
        request.session['uphone'] = request.COOKIES['uphone']
        request.session['uname'] = request.COOKIES['uname']
        request.session['uid'] = request.COOKIES['uid']
        res = {'loginState': 1, 'username': request.session['uname']}
        return JsonResponse(res)
    # 未登录返回结构
    # res = {'loginState':0}
    res = {'loginState':0}
    return JsonResponse(res)

def load_goods(request):
    #加载商品
    #商品品类,商品类 [{'type':{'title':'热带水果'},'goods':[{商品字典},{}...]}]
    all_list = []
    all_types = GoodsType.objects.all()
    for _type in all_types:#避开关键字
        data = {}
        data['type'] = {'title':_type.title}
        data['goods'] = []
        all_goods = _type.goods_set.filter(isActive=True).order_by('-create_time')[:10]
        for good in all_goods:
            d = {}
            d['title'] = good.title
            d['price'] = str(good.price)
            d['spec'] = good.spec
            #good.picture 是个Django的 image 对象
            d['picture'] = str(good.picture)
            data['goods'].append(d)
        all_list.append(data)
    return HttpResponse(json.dumps(all_list),content_type='application/json')

#注册
def register(request):
    if request.method == 'GET':
        # 渲染页面
        return render(request,'register.html')
    elif request.method == 'POST':
        # 处理 注册逻辑 【处理提交的数据】
        uphone = request.POST.get('uphone')
        if not uphone:
            #号码为空
            return HttpResponse('号码不能为空')
        uphones = User.objects.filter(uphone=uphone)
        if uphones:
            #号码已注册
            return HttpResponse('号码已注册')
        uname = request.POST.get('uname')
        if not uname:
            return HttpResponse('用户名不能为空')
        uemail = request.POST.get('uemail')
        userpass1 = request.POST.get('userpass1')
        userpass2 = request.POST.get('userpass1')
        if not userpass1 or not userpass2:
            # 密码未提交
            return HttpResponse('请输入密码')
        if userpass1 != userpass2:
            # 两次密码不相等
            return HttpResponse('两次输入密码不一致')
        # 创建用户
        try:
            user = User.objects.create(uphone=uphone,uname=uname,uemail=uemail,
                                       upwd=userpass1)
        except Exception as e:
            return HttpResponse('当前用户名已注册')

        # 存cookies
        resp = HttpResponseRedirect('/index')
        #免登陆一天
        resp.set_cookie('uphone',uname,60*60*24)
        resp.set_cookie('uname',uname, 60*60*24)
        resp.set_cookie('uid',user.id,60*60*24)
        return resp

#登录
def login(request):
    #登录
    if request.method == 'GET':
        # 1,检查session
        if 'uphone' in request.session and 'uid' in \
                request.session and 'uname' in request.session:
            #已经登录
            return HttpResponseRedirect('/index')
        # 2, 检查cookies
        if 'uphone' in request.COOKIES and 'uid' in \
                request.COOKIES and 'uname' in request.COOKIES:
            # 已登录 & session没数据
            # 回写session并让用户跳转至首页
            request.session['uphone'] = request.COOKIES['uphone']
            request.session['uid'] = request.COOKIES['uid']
            return HttpResponseRedirect('/index')
        return render(request,'login.html')
    elif request.method == 'POST':
        # 处理登录提交的数据
        # 检查用户是否点击 下次免登陆
        save_cookies = False
        if 'save_cookies' in request.POST.keys():
            save_cookies = True

        uphone = request.POST.get('uphone')
        if not uphone:
            return HttpResponse('号码不能为空')
        upwd = request.POST.get('userpass')
        if not upwd:
            return HttpResponse('密码不能为空')
        # 查找用户
        user = User.objects.filter(uphone=uphone)
        if not user:
            return HttpResponse('号码未注册')
        if user[0].upwd != upwd:
            return HttpResponse('密码错误')
        # 用户和密码均匹配
        # 记录登录状态
        request.session['uphone'] = uphone
        request.session['uname'] = user[0].uname
        request.session['uid'] = user[0].id

        # 检查是否存储cookies
        resp = HttpResponseRedirect('/index')
        if save_cookies:
            # cookies中存储用户登录状态 时长30天
            resp.set_cookie('uphone',uphone, 60*60*24*30)
            resp.set_cookie('uname',user[0].uname, 60*60*24*30)
            resp.set_cookie('uid',user[0].id, 60*60*24*30)
        return resp

#退出
def logout(request):
    return render(request,'login.html')


