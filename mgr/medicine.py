from django.http import JsonResponse
from common.models import CommonMedicine
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
        # 获取药品name来判断药品是否存在
        Cname = request.params['data']['name']
        Cnames = []
        for name in CommonMedicine.objects.values('name'):
            for key, value in name.items():
                Cnames.append(value)
        if Cname not in Cnames:
            return addmedicine(request)
        else:
            return JsonResponse({"ret": 3, "msg": "药品名已经存在"})

    elif action == 'modify_medicine':
        # 获取药品id来判断药品是否存在
        Mid = request.params['id']
        Mname = request.params['newdata']['name']
        Medicines = []
        for newdata in CommonMedicine.objects.values():
            for key, value in newdata.items():
                Medicines.append(value)
        if Mid in Medicines:
            if Mname not in  Medicines:
                return modifymedicine(request)
            else:
                return JsonResponse({'ret': 3, 'msg':'药品名已经存在'})
        else:
            return JsonResponse({'ret': 2, 'msg': f'id为{Mid}的药品名不存在'})

    elif action == 'del_medicine':
        # 获取药品id来判断客户是否存在
        Mid = request.params['id']
        Mids = []
        for id in CommonMedicine.objects.values('id'):
            for key, value in id.items():
                Mids.append(value)
        if Mid in Mids:
            return deletemedicine(request)
        else:
            return JsonResponse({'ret': 2, 'msg': f'id为{Mid}的药品名不存在'})
    else:
        return JsonResponse({'ret': 1, 'msg': '参数错误'})

# 获取所有药品信息接口
def listmedicines(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    qs = CommonMedicine.objects.values()
    # 将 QuerySet 对象 转化为 list 类型
    # 否则不能 被 转化为 JSON 字符串
    retlist = list(qs)
    # 默认跳转到第一页
    page = request.GET.get('pagenum', '1')
    # 默认展示10条数据
    size = request.GET.get('pagesize', '10')

    page_obj = Paginator(retlist, size)
    page_data = page_obj.get_page(page)
    res = page_data.object_list
    # 获取列表长度
    count = len(res)
    # 统计数据库有多少条数据
    maxsize = CommonMedicine.objects.count()
    pagesize = request.params['pagesize']
    if int(pagesize) <= int(maxsize):
        return JsonResponse({'ret': 0, 'retlist': res, 'total': count})
    else:
        return JsonResponse({'ret': 4, 'msg': f'参数错误,当前最大数量为{count}'})


# 新增药品信息接口
def addmedicine(request):

    info = request.params['data']
    # 从请求消息中 获取要添加药品的信息
    # 并且插入到数据库中
    # 返回值 就是对应插入记录的对象
    record = CommonMedicine.objects.create(name=info['name'],
                                           desc=info['desc'],
                                           sn=info['sn'])
    return JsonResponse({'ret': 0, 'id': record.id})

# 修改药品信息接口
def modifymedicine(request):
    # 从请求消息中 获取修改客户的信息
    # 找到该药品，并且进行修改操作
    medicineid = request.params['id']
    newdata = request.params['newdata']
    # 根据 id 从数据库中找到相应的药品记录
    medicine = CommonMedicine.objects.get(id=medicineid)
    if 'name' in newdata:
        medicine.name = newdata['name']
    if 'desc' in newdata:
        medicine.desc = newdata['desc']
    if 'sn' in newdata:
        medicine.sn = newdata['sn']
    # 注意，一定要执行save才能将修改信息保存到数据库
    medicine.save()
    return JsonResponse({'ret': 0})

# 删除药品信息接口
def deletemedicine(request):
    # 找到药品id并进行删除
    medicineid = request.params['id']
    # 根据 id 从数据库中找到相应的药品记录
    medicine = CommonMedicine.objects.get(id=medicineid)
    # delete 方法就将该记录从数据库中删除了
    medicine.delete()
    return JsonResponse({'ret': 0})