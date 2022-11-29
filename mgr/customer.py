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
    elif request.method in ['POST', 'PUT', 'DELETE']:
        # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
        request.params = json.loads(request.body)

    # 根据不同的action分派给不同的函数进行处理
    action = request.params['action']
    if action == 'list_customer':
        return listcustomers(request)

    elif action == 'add_customer':
        # 获取客户name来判断客户是否存在
        Cname = request.params['data']['name']
        Cnames = []
        for name in CommonCustomer.objects.values('name'):
            for key,value in name.items():
                Cnames.append(value)
        if Cname not in Cnames:
            return addcustomer(request)
        else:
            return JsonResponse({"ret": 3,"msg": "客户名名已经存在"})

    elif action == 'modify_customer':
        # 获取客户id来判断客户是否存在
        Cid = request.params['id']
        Cname = request.params['newdata']['name']
        Customers = []
        for newdata in CommonCustomer.objects.values():
            for key, value in newdata.items():
                Customers.append(value)
        if Cid in Customers:
            if Cname not in Customers:
                return modifycustomer(request)
            else:
                return JsonResponse({'ret': 3, 'msg': '客户名已经存在'})
        else:
            return JsonResponse({'ret': 2, 'msg': f'id为{Cid}的客户名不存在'})

    elif action == 'del_customer':
        # 获取客户id来判断客户是否存在
        Cid = request.params['id']
        Cids = []
        for id in CommonCustomer.objects.values('id'):
            for key, value in id.items():
                Cids.append(value)
        if Cid in Cids:
            return deletecustomer(request)
        else:
            return JsonResponse({'ret': 2, 'msg': f'id为{Cid}的客户名不存在'})
    else:
        return JsonResponse({'ret': 1, 'msg': '参数错误'})

# 获取所有客户信息接口
def listcustomers(request):
    cursur = connection.cursor()
    # 使用 execute()  方法执行 SQL 查询
    cursur.execute("SELECT * FROM `common_customer`")
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

# 新增客户信息接口
def addcustomer(request):

    info = request.params['data']
    # 从请求消息中 获取要添加客户的信息
    # 并且插入到数据库中
    # 返回值 就是对应插入记录的对象
    record = CommonCustomer.objects.create(name=info['name'],
                            phonenumber=info['phonenumber'],
                            address=info['address'])
    return JsonResponse({'ret':0,'id':record.id})

# 修改客户信息接口
def modifycustomer(request):
    # 从请求消息中 获取修改客户的信息
    # 找到该客户，并且进行修改操作
    customerid = request.params['id']
    newdata = request.params['newdata']
    # 根据 id 从数据库中找到相应的客户记录
    customer = CommonCustomer.objects.get(id=customerid)
    if 'name' in newdata:
        customer.name = newdata['name']
    if 'phonenumber' in newdata:
        customer.phonenumber = newdata['phonenumber']
    if 'address' in newdata:
        customer.address = newdata['address']
    # 注意，一定要执行save才能将修改信息保存到数据库
    customer.save()
    return JsonResponse({'ret':0})

# 删除客户信息接口
def deletecustomer(request):
    # 找到客户id并进行删除
    customerid = request.params['id']
    # 根据 id 从数据库中找到相应的客户记录
    customer = CommonCustomer.objects.get(id=customerid)
    # delete 方法就将该记录从数据库中删除了
    customer.delete()
    return JsonResponse({'ret':0})

