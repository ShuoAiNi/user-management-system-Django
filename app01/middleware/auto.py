from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class LoginMiddleware(MiddlewareMixin):

    def process_request(self,request):
        #request.path_info 获取用户请求的url
        if request.path_info in ['/login/','/image/code/']:
            return

        session = request.session.get("info")
        if session:
            return
        else:
            return redirect("/login/")


