from django.contrib import admin
from django.shortcuts import render,redirect
from app01.models import Admin
from app01.forms import AdminModel

# Register your models here.
def admin_list(request):
    queryset = Admin.objects.all()
    return render(request,"admin_list.html",{"queryset":queryset})


def admin_add(request):
    if request.method == "GET":
        form = AdminModel()
        return render(request,"admin_add.html",{"form":form})
    else:
        form = AdminModel(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("/admin/list/")
        else:
            return render(request, "admin_add.html", {"form": form})


def admin_edit(request,nid):
    model = Admin.objects.filter(id=nid).first()
    if request.method == "GET":
        form = AdminModel(instance=model)
        return render(request, "admin_edit.html", {"form": form})
    else:
        form = AdminModel(data=request.POST, instance=model)
        if form.is_valid():
            form.save()
            return redirect("/admin/list/")
        else:
            return render(request, "admin_edit.html", {"form": form})


def admin_delete(request,nid):
    Admin.objects.filter(id=nid).delete()
    return redirect("/admin/list/")