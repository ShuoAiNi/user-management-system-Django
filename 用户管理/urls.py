"""用户管理 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01 import views,admin

urlpatterns = [
    # path('admin/', admin.site.urls),
    #首页
    path('',views.home),

    #部门管理
    path('depart/list/',views.depart_list),
    path('depart/add/',views.depart_add),
    path('depart/delete/',views.depart_delete),
    path('depart/edit/<int:nid>/',views.depart_edit),

    #用户管理
    path('user/list/',views.user_list),
    path('user/add/',views.user_add),
    path('user/modelform/add/',views.user_modelform_add),
    path('user/edit/<int:nid>/',views.user_edit),
    path('user/delete/<int:nid>/',views.user_delete),

    #靓号管理
    path('pretty/list/',views.pretty_list),
    path('pretty/add/',views.pretty_add),
    path('pretty/edit/<int:nid>/',views.pretty_edit),
    path('pretty/delete/<int:nid>/',views.pretty_delete),

    #管理员管理
    path('admin/list/',admin.admin_list),
    path('admin/add/',admin.admin_add),
    path('admin/edit/<int:nid>/',admin.admin_edit),
    path('admin/delete/<int:nid>/',admin.admin_delete),

    #用户认证
    path('login/',views.login),
    path('loginout/',views.loginout),
    path('image/code/',views.img),

    #订单管理
    path('order/list/',views.order_list),
    path('order/add/',views.order_add),
    path('order/delete/',views.order_delete),
    path('order/detail/',views.order_detail),
    path('order/edit/',views.order_edit),

    path('chart/list/',views.chart_list),
    path('chart/bar/',views.chart_bar),



]
