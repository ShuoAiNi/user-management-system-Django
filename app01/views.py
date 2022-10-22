from django.shortcuts import render,redirect,HttpResponse
from app01.models import Department,UserInfo,PrettyNum,Admin,Order
from app01.forms import UserModelForm,PrettyModelForm,LoginForm,OrderModelForm
from django.utils.safestring import mark_safe
from code import check_code
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import random
from datetime import datetime
# Create your views here.
def home(request):
    return HttpResponse("首页")


def depart_list(request):
    """"部门列表"""
    queryset = Department.objects.all()
    return render(request,"depart_list.html",{"queryset":queryset})

def depart_add(request):
    """添加部门"""
    if request.method == "GET":
        return render(request,"depart_add.html")
    else:
        name = request.POST.get("name")
        Department.objects.create(title=name)
        return redirect("/depart/list/")

def depart_delete(request):
    """删除部门"""
    nid = request.GET.get("nid")
    Department.objects.filter(id=nid).delete()
    return redirect("/depart/list")

def depart_edit(request,nid):
    if request.method == "GET":
        edit_model = Department.objects.filter(id=nid).first()
        return render(request,"depart_edit.html",{"edit_model":edit_model})
    else:
        title = request.POST.get("name")
        Department.objects.filter(id=nid).update(title=title)
        return redirect("/depart/list")


def user_list(request):
    queryset = UserInfo.objects.all()
    return render(request,"user_list.html",{"queryset":queryset})

def user_add(request):
    if request.method == "GET":
        context = {
            "gender_choice":UserInfo.gender_choice,
            "depart_list":Department.objects.all()
        }
        return render(request,"user_add.html",context)
    else:
        name = request.POST.get("name")
        password = request.POST.get("password")
        age = request.POST.get("age")
        account = request.POST.get("account")
        create_time = request.POST.get("create_time")
        gender = request.POST.get("gender")
        depart = request.POST.get("depart")

        UserInfo.objects.create(name=name,password=password,age=age,account=account,create_time=create_time,gender=gender,depart_id=depart)
        return redirect("/user/list/")

def user_modelform_add(request):
    if request.method == "GET":
        form = UserModelForm()
        return render(request,"user_modelform_add.html",{"form":form})
    else:
        form = UserModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("/user/list/")
        else:
            return render(request,"user_modelform_add.html",{"form":form})

def user_edit(request,nid):
    if request.method == "GET":
        model = UserInfo.objects.filter(id=nid).first()
        form = UserModelForm(instance=model)
        return render(request,"user_edit.html",{"form":form})
    else:
        model = UserInfo.objects.filter(id=nid).first()
        form = UserModelForm(data=request.POST,instance=model)
        if form.is_valid():
            form.save()
            return redirect("/user/list")
        else:
            return render(request,"user_edit.html",{"form":form})

def user_delete(request,nid):
    UserInfo.objects.filter(id=nid).first().delete()
    return redirect("/user/list/")

def pretty_list(request):
    """靓号列表"""
    #搜索功能，根据电话搜索
    data_dict = {}
    search_data = request.GET.get('q','')
    if search_data:
        data_dict['mobile__contains'] = search_data

    #分页
    page = int(request.GET.get('page',1))
    page_size = 10
    start = (page-1) * page_size #起始
    end = page * page_size #结束

    queryset = PrettyNum.objects.filter(**data_dict).order_by('-level')[start:end]
    #获取数据库页数
    total_count = PrettyNum.objects.all().count()
    total_page_count , div =divmod(total_count,page_size)
    if div:
        total_page_count += 1

    #计算出当前页的前五页，后五页
    plus = 5
    # 如果数据库中的页不足11页
    if total_page_count <= plus*2+1:
        start_page = 1
        end_page = total_page_count
    else:
        #数据库中的数据大于11页
        #且当前页小于等于5
        if page <= plus:
            start_page = 1
            end_page = 2*plus +1
        else:
            if page > total_page_count-5:
                start_page = total_page_count - 2*plus
                end_page =  total_page_count
            else:
                start_page = page - plus
                end_page = page + plus


    #页码
    page_str_list = []
    #上一页
    if page>1:
        pre = '<li class="active"><a href="?page={}">上一页</a></li>'.format(page-1)
        page_str_list.append(pre)

    for i in range(start_page,end_page+1):
        if i == page:
            ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
        else:
            ele = '<li><a href="?page={}">{}</a></li>'.format(i,i)
        page_str_list.append(ele)
    #下一页
    if page< total_page_count:
        pre = '<li class="active"><a href="?page={}">下一页</a></li>'.format(page + 1)
        page_str_list.append(pre)

    page_string = mark_safe("".join(page_str_list))
    return render(request,"pretty_list.html",{"queryset":queryset,"search_data":search_data,"page_string":page_string})


def pretty_add(request):
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request,"pretty_add.html",{"form":form})
    else:
        form = PrettyModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("/pretty/list/")
        else:
            return render(request,"pretty_add.html",{"form":form})


def pretty_edit(request,nid):
    model = PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = PrettyModelForm(instance=model)
        return render(request,"pretty_edit.html",{"form":form})
    else:
        form = PrettyModelForm(data=request.POST,instance=model)
        if form.is_valid():
            form.save()
            return redirect("/pretty/list/")
        else:
            return render(request,"pretty_edit.html",{"form":form})


def pretty_delete(request,nid):
    PrettyNum.objects.filter(id=nid).first().delete()
    return redirect("/pretty/list/")


def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request,"login.html",{"form":form})
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            #因为form中有code字段，而数据库中没有，所有做验证时不能将code放进去验证
            input_code = form.cleaned_data.pop("code")
            #获取之前放入session中的img_code
            code = request.session.get("img_code","")
            if code.upper() != input_code.upper():
                #给form.code.error添加错误信息
                form.add_error("code","验证码错误")
                return render(request,"login.html",{"form":form})

            #form.clean_data = {"username":"sss","password":"dadnalkdhnaoldhnao"}

            #当LoginForm中的字段名等于MODEL里的字段名时，可以将**form.cleaned_data传入filter中，作为校验
            obj = Admin.objects.filter(**form.cleaned_data).first()
            if obj:
                #删除掉之前session中的验证码，防止使用此验证码多次登录
                request.session.clear()
                request.session["info"] = {"id":obj.id,"username":obj.username}
                #重新设置session的超时时间为7天
                request.session.set_expiry(60*60*24*7)
                return redirect("/depart/list/")
            else:
                form.add_error("password","用户名或密码错误")
                return render(request, "login.html", {"form": form})
        else:
            return render(request,"login.html",{"form":form})


def loginout(request):
    request.session.clear()
    return redirect('/login/')


def img(request):
    """生成图片验证码"""
    #接收生成的图片和图片的验证码
    img , code_string = check_code()
    #将图片验证码写入到自己的session中，以便校验
    request.session["img_code"] = code_string
    #给sess设置60s超时
    request.session.set_expiry(60)
    #创建1个IO对象
    stream = BytesIO()
    # 把图片img保存到内存
    img.save(stream,'png')
    #getvalue()获取图片信息
    return HttpResponse(stream.getvalue())


def order_list(request):
    queryset = Order.objects.all().order_by("-id")
    form = OrderModelForm()
    return render(request,"order_list.html",{"form":form,"queryset":queryset})

@csrf_exempt
def order_add(request):
    """新建订单ajax"""
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000,9999))
        form.instance.admin_id = request.session["info"]["id"]
        form.save()
        return JsonResponse({"status":True})
    return JsonResponse({"status":False,"error":form.errors})


def order_delete(request):
    uid = request.GET.get("uid")
    exists = Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status":False,"error":"删除失败,数据不存在"})
    Order.objects.filter(id=uid).delete()
    return JsonResponse({"status":True})


def order_detail(request):
    """根据uid获取当前行数据"""
    uid = request.GET.get("uid")
    #加上.values后生成的row_dict是一个字典{"status":"已支付"}
    row_dict = Order.objects.filter(id=uid).values("status","title","price").first()
    if not row_dict:
        return JsonResponse({"status": False, "error": "数据不存在"})
    else:
        data = {
            "status":True,
            "result":row_dict
        }
        return JsonResponse(data)

@csrf_exempt
def order_edit(request):
    """编辑订单"""
    uid = request.GET.get("uid")
    row_object = Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status":False,"tips":"数据不存在。"})
    else:
        #使用instance=object对象可以将对象中的数据传入到界面中，将数据库中的值赋给前端input框中的value，使得编辑时能够显示原来的数据
        form = OrderModelForm(data=request.POST,instance=row_object)
        if form.is_valid():
            form.save()
            return JsonResponse({"status":True})
        return JsonResponse({"status":False,"error":form.errors})


def chart_list(request):
    return render(request,"chart_list.html")


def chart_bar(request):
    """构造柱状图的数据"""
    legend = ["销量"]
    xAxis = ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']
    series = [{
        "name":'销量',
        "type":"bar",
        "data":[5,20,36,10,10,20]
    }]
    result = {
        "status":True,
        "data":{
            "legend":legend,
            "xAxis":xAxis,
            "series":series,
        }
    }
    return JsonResponse(result)