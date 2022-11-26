from django.http import JsonResponse
from django.contrib.auth import authenticate,login,logout

# 登录接口
def signin(request):
    # 从 HTTP POST 请求中获取用户名、密码参数
    userName = request.POST.get('username')
    passWord = request.POST.get('password')
    # 使用 Django auth 库里面的 方法校验用户名、密码
    user = authenticate(username=userName,password=passWord)
    # 如果能找到用户，并且密码正确
    if user is not None :
        # 用户是否被禁用
        if user.is_active:
            # 用户是否为管理员用户
            if user.is_superuser:
                # 如果以上都正确，用户登录成功
                login(request,user)
                # 在session存入用户类型
                request.session['usertype'] = 'mgr'

                return JsonResponse({'ret': 0})
            else:
                return JsonResponse({'ret':1,'msg':'请使用管理员账户登录'})
        else:
            return JsonResponse({'ret':0,'mesg':'用户已经被禁用'})
    # 否则就是用户名、密码有误
    else:
        return JsonResponse({'ret':1,'msg':'用户名或密码错误'})

# 登出接口
def signout(request):
    # 使用登出方法
    logout(request)
    return JsonResponse({'ret':0})

