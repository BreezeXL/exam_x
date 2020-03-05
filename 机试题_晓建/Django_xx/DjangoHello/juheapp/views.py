from django.shortcuts import render
from django.http import HttpResponse, FileResponse, JsonResponse
# Create your views here.
import requests
import yaml
from django.conf import settings
from django.views import View
# import myfirstproj.settings 和上边一致
# from myfirstproj import settings
import os
from django.shortcuts import render
from utils import responseutil
from utils.responseutil import UtilMixin

def hellojuhe(request):
    url = 'http://v.juhe.cn/joke/content/list.php?sort=asc&page=2&pagesize=3&time=1418816972&key=a3d4e42ae7d867b78774ca35f741f124'
    res = requests.get(url)
    if res.status_code == 200:
        return HttpResponse(res.text)
    else:
        return HttpResponse('没有获取到数据')


def testrequest(request):
    print('请求方法:', request.method)
    print('客户端信息:', request.META)
    print('get请求参数:', request.GET)
    print('请求头:', request.headers)
    print('cookie:', request.COOKIES)
    return JsonResponse({'请求方法': request.method,
                         '客户端信息': 'ssss',
                         '请求头': 'ssss',
                         'cookie': request.COOKIES.__str__()
                         })


def image(request):
    if request.method == 'GET':
        filepath = os.path.join(settings.STATIC_ROOT_SELF, 'abc.png')
        f = open(filepath, 'rb')
        # with open(filepath, 'rb') as f:
        # return HttpResponse(content=f.read(),content_type='image/png')
        return FileResponse(f, content_type='image/jpg')
    elif request.method == "POST":
        return HttpResponse('这是post请求')
    else:
        return HttpResponse(request.method + '方法没有实现')


class ImageView(View,UtilMixin):

    def get(self, request):

        filepath = os.path.join(settings.STATIC_ROOT_SELF, 'abc.png')
        f = open(filepath, 'rb')
        # with open(filepath, 'rb') as f:
        # return HttpResponse(content=f.read(),content_type='image/png')
        return FileResponse(f, content_type='image/jpg')
        # return render(request,'upfile.html')

    def post(self, request):
        files1 = request.FILES
        # class 'django.utils.datastructures.MultiValueDict'
        # print(type(files))
        picdir = settings.UPLOAD_PIC_DIR

        for key,value in files1.items():
            filename = os.path.join(picdir,key[-8:])
            UtilMixin.savepic(filename,value.read())

        # return HttpResponse(filename)
        return JsonResponse(UtilMixin.wrapdic({'filename':key[-8:]}))

    def delete(self,request):
        picname = request.GET.get('name')
        print('picname',picname)
        picdir = settings.UPLOAD_PIC_DIR
        pic_full_path = os.path.join(picdir,picname)
        if not os.path.exists(pic_full_path):
            return HttpResponse('图片不存在')
        else:
            # 删除它
            os.remove(pic_full_path)
            return HttpResponse('图片删除成功')



from utils.responseutil import ResponseMixin


class ImageText(View, ResponseMixin):
    # def get(self,request):
    #     filepath = os.path.join(settings.STATIC_ROOT_SELF, 'ac.png')
    #     if os.path.exists(filepath):
    #         f = open(filepath, 'rb')
    #         return FileResponse(f, content_type='image/jpg')
    #     else:
    #         return JsonResponse(data={'code':4040,'des':'没有找到图片'})

    # def get(self,request):
    #     return render(request,'imagetext.html',{'des':'图片描述','url':'/api/v1.0/apps/image/'})

    # 提取公共的状态码信息
    # def wrapjson(self,response):
    #     response['code']=1000
    #     response['codedes']='没发现问题'
    #     return response

    def get(self, request):
        # return JsonResponse(data={'url': 'xxxxx', 'des': '我很好',
        #                           'code': 1000, 'codedes': '没发现问题'})

        # return JsonResponse(data=self.wrapjson({'url': 'xxxxx', 'des': '我很好',
        #                           }))
        # return JsonResponse(data=responseutil.wrap_response({'url': 'xxxxx', 'des': '我很好'
        #                           }))
        # ? 为何wrap_response 不能独立出来,变成一个类, 让所有 xxxView 都继承呢?
        return JsonResponse(data=self.wrap_response({'url': 'xxxxx', 'des': '我很好','code':2002}))


# def apps(request):
#     return JsonResponse(['微信','支付宝','钉钉'],safe=False)
# def apps(request):
#     return JsonResponse({'names':['微信','支付宝','钉钉']},safe=T

# def apps(request):
#     return JsonResponse([{'name': '微信'},
#                          {'name': '支付宝'}, {'name': '钉钉'}], safe=False)

def apps(request):
    if request.method == "POST":
        return HttpResponse('逗你玩..')
    filepath = r'E:\pycharm_projects\myfirstproj\myfirstproj\myappconfig.yaml'
    with open(filepath, 'r', encoding='utf8') as f:
        res = yaml.load(f, Loader=yaml.FullLoader)
    return JsonResponse(res, safe=False)
