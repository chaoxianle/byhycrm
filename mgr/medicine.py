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
    if action == 'list_medicine':
        return listmedicines(request)

    elif action == 'add_medicine':
        # 根据订单名来判断客户是否存在
        mname = request.params['data']['name']
        cursur = connection.cursor()
        cursur.execute("SELECT id,name FROM `common_medicine`")
        data = dict(cursur.fetchall())
        # 关闭数据库连接
        cursur.close()
        names = []
        for id, name in data.items():
            names.append(name)
        if mname not in names:
            return addmedicine(request)
        else:
            return JsonResponse({"ret": 3, "msg": "药品名已经存在"})

    elif action == 'modify_medicine':
        # 获取订单id来判断药品是否存在
        mid = request.params['id']
        mname = request.params['newdata']['name']
        # 获取游标对象
        cursur = connection.cursor()
        cursur.execute("SELECT id,name FROM `common_medicine`")
        data = dict(cursur.fetchall())
        print(data)
        # 关闭数据库连接
        cursur.close()
        names = []
        for id,name in data.items():
            names.append(name)
        if mid in data:
            if mname not in names:
                return modifymedicine(request)
            else:
                return JsonResponse({'ret': 3, 'msg':'订单已经存在'})
        else:
            return JsonResponse({'ret': 2, 'msg': f'id为{mid}的订单不存在'})

    elif action == 'del_medicine':
        # 获取药品id来判断药品是否存在
        mid = request.params['id']
        cursur = connection.cursor()
        cursur.execute("SELECT id,name FROM `common_medicine`")
        data = dict(cursur.fetchall())
        if mid in data:
            return deletemedicine(request)
        else:
            return JsonResponse({'ret': 2, 'msg': f'id为{mid}的药品名不存在'})
    else:
        return JsonResponse({'ret': 1, 'msg': '参数错误'})

# 获取所有药品信息接口
def listmedicines(request):
    # 获取游标对象
    cursur = connection.cursor()
    # 使用 execute()  方法执行 SQL 查询
    cursur.execute("SELECT * FROM common_medicine")
    # 使用 fetchone() 方法获取所有数据.
    data = cursur.fetchall()
    # 关闭数据库连接
    cursur.close()
    infodict = {}
    retlist = []
    for info in data:
        infodict['id'] = info[0]
        infodict['name'] = info[1]
        infodict['phonenumber'] = info[2]
        infodict['address'] = info[3]
        retlist.append(infodict)
    # 默认跳转到第一页
    pagenum = request.GET.get('pagenum', '1')
    # 默认一页展示10条数据
    pagesize = request.GET.get('pagesize', '10')

    page_obj = Paginator(retlist, pagesize)
    page_data = page_obj.get_page(pagenum)
    res = page_data.object_list
    # # 获取列表长度
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

# 新增药品信息接口
def addmedicine(request):
    # 从请求消息中 获取要添加药品的信息
    # 并且插入到数据库中
    # 返回值 就是对应插入记录的对象
    mname = request.params['data']['name']
    msn = request.params['data']['sn']
    mdesc = request.params['data']['desc']
    cursur = connection.cursor()
    isql = "insert into common_medicine(name,sn,description)values(%s,%s,%s)"
    # 使用 execute()  方法执行 SQL 查询
    cursur.execute(isql, (mname, msn, mdesc))
    # 获取游标对象
    cursur = connection.cursor()
    cursur.execute("select id from common_medicine order by id desc limit 1 ")
    data = cursur.fetchall()
    cursur.close()
    return JsonResponse({'ret': 0, 'id': (data[0][0])})

# 修改药品信息接口
def modifymedicine(request):
    # 从请求消息中 获取修改药品的对应信息
    # 找到该客户，并且进行修改操作
    mustomerid = request.params['id']
    mname = request.params['newdata']['name']
    msn = request.params['newdata']['sn']
    mdescription = request.params['newdata']['description']
    # 根据 id 从数据库中找到相应的药品记录
    cursur = connection.cursor()
    msql = "update common_medicine set name = %s,sn = %s,description = %s where id = %s"
    cursur.execute(msql, (mname, msn, mdescription, mustomerid))
    cursur.close()
    return JsonResponse({'ret': 0})

# 删除药品信息接口
def deletemedicine(request):
    # 找到药品id并进行删除
    medicineid = request.params['id']
    # 根据 id 从数据库中找到相应的客户记录
    cursur = connection.cursor()
    # delete 方法就将该记录从数据库中删除了
    dsql = "delete from common_medicine where id = %s"
    cursur.execute(dsql, (medicineid))
    cursur.close()
    return JsonResponse({'ret': 0})