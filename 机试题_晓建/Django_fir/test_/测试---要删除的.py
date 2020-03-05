from django.shortcuts import render
from django.http import HttpResponse, FileResponse, JsonResponse
from HelloDjango import settings
from Utils.resputils import ResponseMixin, SaveImage
from jhapp.models import User

# 两种一样的
from django.views.generic import View
from django.views import View
import requests
import yaml
import os
import json

import static


# Create your views here.

def helloworld(request):
    url = 'http://api.juheapi.com/japi/toh?v=1.0&month=10&day=1&key=5632d75c2c0ea881b88f47e7fb66e6c8'
    res = requests.get(url)
    if res.status_code == 200:
        return HttpResponse(res.text)
    return HttpResponse('获取数据失败!请重新尝试!')


def testrequest(request):
    method = request.method
    mata = request.META
    get = request.GET
    headers = request.headers
    cookie = request.COOKIES
    response_date = {}
    response_date['request_method'] = method
    response_date['get_request_parameter'] = get
    response_date['cookie'] = cookie
    print('请求方法:', method)
    print('客户端信息:', mata)
    print('get请求参数:', get)
    print('请求头:', headers)
    print('cookie:', cookie)
    print(response_date)
    return JsonResponse(data=response_date, safe=False)


def image(request):
    if request.method == 'GET':
        # f = open(r'D:\PycharmProjects\HelloDjango\static\1001068.jpg', 'rb')
        # imagename = '1001068.jpg'
        imagename = request.GET.get('imagename')
        if imagename:
            filename = os.path.join(settings.STATICFILES_DIRS_SELF, imagename + '.jpg')
            # with open 写法需返回 HttpResponse
            with open(filename, 'rb')as f:
                return HttpResponse(f.read(), content_type='image/jpeg')
        filename = r'D:\PycharmProjects\HelloDjango\static\1001068.jpg'
        # 直接 open 的写法 HttpResponse FileResponse 两者都可以
        # f = open(filename, 'rb')
        return FileResponse(open(filename, 'rb'), content_type='image/jpg')
    elif request.method == 'POST':
        # 需要在setting中注释一下 才能返回
        # 'django.middleware.csrf.CsrfViewMiddleware',
        return HttpResponse(f'请求方式为:{request.method}', )
    else:
        return HttpResponse(request.method, '的请求方式还没有实现')


# def showapps(request):
#     return JsonResponse(['微信', '支付宝', 'QQ'], safe=False)
# def showapps(request):
#     return JsonResponse({'appnames': ['微信', '支付宝', 'QQ']}, safe=True)


def showapps(request):
    filename = r'D:/PycharmProjects/HelloDjango/HelloDjango/appcomfig.yaml'
    with open(filename, 'r', encoding='utf-8')as f:
        res = yaml.load(f, Loader=yaml.FullLoader)
        # print(res)
    return JsonResponse(res)


class ImageViews(View, ResponseMixin, SaveImage):
    def get(self, request):
        # imagename = '1001068'
        imagename = request.GET.get('imagename')
        print('-------------', imagename)
        imagetype = '.jpg'
        filename = os.path.join(settings.STATICFILES_DIRS_SELF, imagename + imagetype)
        if not os.path.exists(filename):
            return JsonResponse(data=self.wrap_response({'url': 'URL error', 'code': 2222}))
        # return JsonResponse({'data': {'name': f'{imagename}', 'url': f'/api/v1.0/apps/showimage?imagename={imagename}'},
        #                      'result_code': 200,
        #                      'message': 'success'})
        return JsonResponse(data=self.wrap_response({
            'data': {'name': f'{imagename}', 'url': f'/api/v1.0/apps/showimage?imagename={imagename}'}, 'code': 2000}))

    def post(self, request):
        # return HttpResponse(f'请求方式为:{request.method}', )
        files = request.FILES
        md5key = ''
        if files:
            for key, value in files.items():
                SaveImage.saveimage(key, value)
            return JsonResponse(data=self.wrap_response({
                'name': md5key,
                'code': 2000

            }))
        else:
            return JsonResponse(data=self.wrap_response({
                'code': 2222
            }))

    def delete(self, request):
        imagename = request.GET.get('imagename')
        imagepath = os.path.join(settings.STATICFILES_DIRS_SELF, imagename + '.jpg')
        if os.path.exists(imagepath):
            os.remove(imagepath)
            message = 'remove success'
            code = 2000
        else:
            message = f'file {imagename}.jpg not found'
            code = 2222
        return JsonResponse(data=self.wrap_response({
            'message': message,
            'code': code
        }))


class CookieTest(View):
    def get(self, request):
        request.session['mykey'] = '我的值'
        return JsonResponse({'key': 'value'})


class CookieTest2(View):
    def get(self, request):
        print(request.session['mykey'])
        print(request.session.items())
        return JsonResponse({'key2': 'value2'})


class Authorization(View):
    def get(self, request):
        return HttpResponse('success')

    def post(self, request):
        # print('-------------', request.body)  # b'{"code":"071sEMTO053L062C6ZTO0KmVTO0sEMTA"}'
        # 从body中获取 code nikeName
        bodystr = request.body.decode('utf-8')
        bodydict = json.loads(bodystr)
        code = bodydict.get('code')
        abc = bodydict.get('abc')
        nickName = bodydict.get('nickName')
        # print('abc: ', abc)
        # print('code: ', code)
        # print('nickName: ', nickName)

        # 获取 session_key与openid
        appid = settings.APPID
        secret = settings.AUTHORIZATION_SECRET_KEY
        js_code = code
        url = f'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={js_code}&grant_type=authorization_code'
        res = requests.get(url)
        # print(res.text)

        # 获取 openID
        res_dict = json.loads(res.text)
        openid = res_dict.get('openid')
        if not openid:
            return HttpResponse('认证失败')

        # 给用户添加状态 返回至小程序
        request.session['openid'] = openid
        request.session['id_authorized'] = True
        # 如果数据库中没有 openid 说明第一次登陆 注册一下
        if not User.objects.filter(openid=openid):
            newuser = User(openid=openid, nikename=nickName)
            newuser.save()

        return JsonResponse({'openid': openid, 'message': '认证成功'})


#
# 判断是否已经授权
def already_authorized(request):
    id_authorized = False

    if request.session.get('id_authorized'):
        id_authorized = True
    return id_authorized


# def get_user(request):
#     if not already_authorized(request):
#         raise Exception('not authorized request')
#     open_id = request.session.get('open_id')
#     user = User.objects.get(open_id=open_id)
#     return user


# def c2s(appid, code):
#     return code2session(appid, code)


#
class UserView(View):
    # 关注的城市、股票和星座
    def get(self, request):
        # 判断是否授权
        if not already_authorized(request):
            # response = self.wrap_json_response(code=ReturnCode.SUCCESS)
            response = {'code': '没有授权404'}
            return JsonResponse(data=response, safe=False)
        print('get.request.session:', request.session)
        # 授权成功 获取 session 中的openid
        open_id = request.session.get('openid')
        # 获取当前用户对象数据库数据
        user = User.objects.get(openid=open_id)
        data = {}
        data['focus'] = {}
        data['focus']['city'] = json.loads(user.focus_cities)
        data['focus']['stock'] = json.loads(user.focus_stocks)
        data['focus']['constellation'] = json.loads(user.focus_constellations)
        # response = self.wrap_json_response(data=data, code=ReturnCode.SUCCESS)
        # 将数据库中的数据返回给 小程序 用于渲染界面
        response = {'data': data, 'code': 200}
        return JsonResponse(data=response, safe=False)

    def post(self, request):
        # 判断是否授权
        if not already_authorized(request):
            # response = self.wrap_json_response(code=ReturnCode.SUCCESS)
            response = {'code': '没有授权404'}
            return JsonResponse(data=response, safe=False)
        print('post.request.session:', request.session)
        # 授权成功 获取 session 中的openid
        open_id = request.session.get('openid')
        # 获取当前用户对象数据库数据
        user = User.objects.get(openid=open_id)

        # 将body解码
        received_body = request.body.decode('utf-8')
        received_body = eval(received_body)

        # 获取小程序传过来的值
        cities = received_body.get('city')
        stocks = received_body.get('stock')
        constellations = received_body.get('constellation')

        user.focus_cities = json.dumps(cities)
        user.focus_stocks = json.dumps(stocks)
        user.focus_constellations = json.dumps(constellations)
        user.save()

        # response = self.wrap_json_response(code=ReturnCode.SUCCESS, message='modify user info success.')
        response = {'code': 200, 'message': 'modify user info success.'}

        return JsonResponse(data=response, safe=False)
        pass


class Logout(View):
    def get(self, request):
        request.session.clear()
        return JsonResponse(data={'key': 'logout success.'}, safe=False)


class Status(View):
    def get(self, request):
        data = {'is_authorized': 0}
        if already_authorized(request):
            data = {'is_authorized': 1}
        return JsonResponse(data, safe=False)
