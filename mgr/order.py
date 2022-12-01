from django.http import JsonResponse
from django.db import connection
from django.core.paginator import Paginator
import json

def dispatcher(request):
    # 根据session判断用户是否是登录的管理员用户
    if 'usertype' not in request.session:
        return JsonResponse({
                                'ret':302,
                                'msg':'未登录',
                                'redirect':'/mgr/sign.html'},
                                status=302
                            )
    if request.session['usertype'] != 'mgr':
        return JsonResponse({
                               'ret':'302',
                               'msg': '用户非mgr类型',
                               'redirect': '/mgr/sign.html'},
                               status=302
                            )

    # 将请求参数统一放入request 的 params 属性中，方便后续处理

    # GET请求 参数在url中，同过request 对象的 GET属性获取
    if request.method == 'GET':
        # 根据不同的action分派给不同的函数进行处理
        request.params = request.GET
    # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
    elif request.method in ['POST','PUT','DELETE']:
        # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
        request.params = json.loads(request.body)

    # 根据不同的action分派给不同的函数进行处理
    action = request.params['action']
    if action == 'list_order':
        return listorders(request)
    elif action == 'add_order':
        return addorder(request)
    elif action == 'delete_order':
        return deleteorder(request)

# 获取所有订单接口
def listorders(request):
    cursur =connection.cursor()
    # 使用 execute()  方法执行 SQL 查询
    cursur.execute("SELECT * FROM `common_order`")
    # 使用 fetchone() 方法获取单条数据.
    data = cursur.fetchall()
    # 关闭数据库连接
    cursur.close()
    retlist = list(data)
    # 默认跳转到第一页
    pagenum = request.GET.get('pagenum','1')
    # 默认一页展示10条数据
    pagesize = request.GET.get('pagesize','10')

    page_obj = Paginator(retlist, pagesize)
    page_data = page_obj.get_page(pagenum)
    res = page_data.object_list
    # 获取列表长度
    count = len(res)
    # 获取最大页码数
    maxpagenum = Paginator(retlist, pagesize).num_pages

    if int(pagesize) <= 10:
        if int(pagenum) <= int(maxpagenum):
            return JsonResponse({'ret': 0, 'retlist': res, 'total': count})
        else:
            return JsonResponse({'ret': 4, 'msg': f'参数错误,当前页面最大为{maxpagenum}'})
    else:
        return JsonResponse({'ret': 4, 'msg': f'参数错误,当前页最多展示10条数据'})