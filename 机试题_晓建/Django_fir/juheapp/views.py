from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
import requests, os, hashlib, yaml, json
from django.conf import settings
from first_dj import settings
from django.views import View
from utils.responseutil import UtilMixin
from utils.responseutil import ResponseMixin
from first_dj.appid import *
from juheapp.models import *


# from utils.wx.code2session import code2session

def hellojuhe(request):
    url = "http://v.juhe.cn/dream/category?fid=%E6%9D%9C%E5%B0%91%E6%AF%85&key=cad5055003636967696a2c0d81fca82c"
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


def apps(request):
    # return JsonResponse(['微信', '支付宝','钉钉','王者荣耀'],safe=False, )
    # # return JsonResponse({'name': ['微信', '支付宝', '钉钉', '王者荣耀']}, safe=True, )
    if request.method == "POST":
        return HttpResponse('逗你玩..')
    filepath = r'D:\study\project__\django_333\first_dj\first_dj\myappconfig.yaml'
    with open(filepath, 'r', encoding='utf8') as f:
        res = yaml.load(f, Loader=yaml.FullLoader)
    return JsonResponse(res, safe=False)


def image(request):
    if request.method == 'GET':
        filepath = os.path.join(settings.STATIC_ROOT_SELF, 'abc.png')
        f = open(filepath, 'rb')
        # with open(filepath,'tb')as f:
        #     return HttpResponse(content=f.read(), content_type='image/png')
        return FileResponse(f, content_type='image/jpg')
    elif request.method == "POST":
        return HttpResponse('这是post请求')
    else:
        return HttpResponse(request.method + "方法没有实现")


class ImageView(View, UtilMixin):
    def get(self, request):
        filepath = os.path.join(settings.STATIC_ROOT_SELF, 'abc.png')
        f = open(filepath, 'rb')
        # with open(filepath,'tb')as f:
        #     return HttpResponse(content=f.read(), content_type='image/png')
        return FileResponse(f, content_type='image/jpg')

    # def post(self, request):
    #     #     # return HttpResponse('这是post请求')
    #     #     # return self.get(request)
    #     #     file_obj=request.FILES.get('file',None)
    #     #     print(file_obj.name)
    #     #     print(file_obj.size)
    #     #
    #     #
    #     #     files = request.FILES
    #     #     print('6666666我在views文件',type(files))
    #     #     for key,value in files.items():
    #     #         print(777,key)
    #     #         print(888,value)
    #     #     return HttpResponse('测试.123..')

    # def post(self, request):    # 张锦涛写的
    #     # 获取文件 返回 key(文件名),value(文件内容)对象
    #     files = request.FILES
    #     response = []
    #     for key, value in files.items():
    #         content = value.read()
    #         md5 = hashlib.md5(content).hexdigest()
    #         path = os.path.join(STATIC_ROOT_SELF, md5 + '.jpg')
    #         with open(path, 'wb') as f:
    #             f.write(content)
    #         response.append({
    #             'name': key,
    #             'md5': md5
    #         })
    #     message = 'post message success'
    #     # response = utils.response.wrap_json_response(message=message)
    #     response = self.wrap_json_response(data=response,
    #                                        code=utils.response.ReturnCode.SUCCESS,
    #                                        message=message)
    #     return JsonResponse(data=response, safe=False)
    def post(self, request):
        # 获取request的文件
        files1 = request.FILES
        # class 'django.utils.datastructures.MultiValueDict'
        # print(type(files))
        picdir = settings.UPLOAD_PIC_DIR

        # 以字典的形式获取filename和内容
        for key, value in files1.items():
            filename = os.path.join(picdir, key[-8:])  # 取名
            UtilMixin.savepic(filename, value.read())  # 保存

            return JsonResponse(UtilMixin.wrapdic({'filename': key[-8:]}))  # return filename倒数8位
        return HttpResponse('代表files里面没有内容')

    def delete(self, request):
        picname = request.GET.get('name')
        picdir = settings.UPLOAD_PIC_DIR
        print(666666, picname, picdir)
        pic_full_path = os.path.join(picdir, picname)
        if not os.path.exists(pic_full_path):
            return HttpResponse('图片不存在')
        else:
            return HttpResponse('删除成功')

    # def delete(self, request):
    #     # 取出文件名字
    #     md5 = request.GET.get('md5')
    #     # 判断这个名字存不存在
    #     img_name = md5 + '.jpg'
    #     # 文件路径
    #     path = os.path.join(IMAGES_DIR, img_name)
    #     if os.path.exists(path):
    #         os.remove(path)
    #         message = 'remove success.'
    #     else:
    #         message = 'file(%s) not found.' % img_name
    #         # response = utils.response.wrap_json_response(message=message)
    #     response = self.wrap_json_response(code=utils.response.ReturnCode.SUCCESS,
    #                                        message=message)
    #     return JsonResponse(data=response, safe=False)

    # def put(self, request):
    #     message = 'put message success'
    #     # response = utils.response.wrap_json_response(message=message)
    #     response = self.wrap_json_response(message=message)
    #     return JsonResponse(data=response, safe=False)


class ImageText(View, ResponseMixin, ):
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
        return JsonResponse(data=self.wrap_response({'url': 'xxxxx', 'des': '我很好', 'code': 2002}))


class CookieTest(View):
    # 此视图函数对应的url是:http://127.0.0.1:8000/api/v1.0/apps/testcookie/
    # 和小程序对应
    def get(self, request):
        # print(dir(request))
        request.session['mykey'] = '我的值value11111111'
        return JsonResponse({'132': '123123'})


class CookieTest2(View):
    """此视图函数对应的url是:http://127.0.0.1:8000/api/v1.0/apps/testcookie/
    负责接收cookie
    """

    def get(self, request):
        # print(dir(request))
        print(33333, request.session['mykey'])
        # request.session['mykey'] = '我的值value'
        return JsonResponse({'222222': '2222222222222222'})


class Authorization(View):
    def get(self, request):
        # return self.post(request)
        return HttpResponse('success我是get接口')

    def post(self, request):
        # print(request.GET)
        # post的参数在body里面
        print(request.body)  # b'{"code":"033xOZOA0uTdkj2IOlOA0FOgPA0xOZOY"}'
        bodystr = request.body.decode('utf-8')
        bodydict = json.loads(bodystr)  # 变成一个字典
        code = bodydict.get('code')
        nickname = bodydict.get('nickname')
        appid = APPID
        secret = SECTER_KEY
        # print('-----code:', code)
        # print('-----secret:', secret)
        # print('-----nickname:', nickname)

        # 发起请求
        url = f'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type=authorization_code'
        res = requests.get(url)
        # print('----res.text', res.text)
        res_dict = json.loads(res.text)
        openid = res_dict.get('openid')
        if not openid:
            return HttpResponse('认证失败')
        # 给这个用户赋予了一些状态
        request.session['openid'] = openid
        request.session['if_authorized'] = True

        # 将用户信息导入数据库
        # 如果数据库中没有将openid说明第一次登录,注册一下
        if not User.objects.filter(openid=openid):
            # 昵称从用户那边传过来
            newuser = User(openid=openid, nickname=nickname)
            # 保存至数据库
            newuser.save()
        return JsonResponse({'openid': openid, })
        # return HttpResponse('authorize post ok')


# 20200227新添加得
# GET https://api.weixin.qq.com/sns/jscode2session?appid=APPID&secret=SECRET&js_code=JSCODE&grant_type=authorization_code
def c2s(appid, code):
    return code2session(appid, code)


def code2session(appid, code):
    API = 'https://api.weixin.qq.com/sns/jscode2session'
    params = 'appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' % \
             (APPID, SECTER_KEY, code)
    url = API + '?' + params
    response = requests.get(url=url, )
    data = json.loads(response.text)
    print(data)
    return data


def __authorize_by_code(request):
    '''
    使用wx.login的到的临时code到微信提供的code2session接口授权

    post_data = {
        'encryptedData': 'xxxx',
        'appId': 'xxx',
        'sessionKey': 'xxx',
        'iv': 'xxx'
    }
    '''
    response = {}
    post_data = request.body.decode('utf-8')
    post_data = json.loads(post_data)
    app_id = post_data.get('appId').strip()
    nickname = post_data.get('nickname').strip()
    code = post_data.get('code').strip()
    print(code)
    print(app_id)
    if not (app_id and code):
        response['result_code'] = 2500
        response['message'] = 'authorized failed. need entire authorization data.'
        return JsonResponse(response, safe=False)
    try:
        data = c2s(app_id, code)
    except Exception as e:
        print(e)
        response['result_code'] = 2500
        response['message'] = 'authorized failed.'
        return JsonResponse(response, safe=False)
    openid = data.get('openid')
    if not openid:
        response['result_code'] = 2500
        response['message'] = 'authorization error.'
        return JsonResponse(response, safe=False)
    request.session['openid'] = openid
    request.session['is_authorized'] = True

    print(openid)
    # User.objects.get(openid=openid) # 不要用get，用get查询如果结果数量 !=1 就会抛异常
    # 如果用户不存在，则新建用户
    if not User.objects.filter(openid=openid):
        new_user = User(openid=openid, nickname=nickname)
        new_user.save()

    # message = 'user authorize successfully.'
    # response = wrap_json_response(data={}, code=ReturnCode.SUCCESS, message=message)
    return JsonResponse(response, safe=False)


def authorize(request):
    return __authorize_by_code(request)


# 判断是否已经授权
def already_authorized(request):
    is_authorized = False

    if request.session.get('is_authorized'):
        is_authorized = True
    return is_authorized


def get_user(request):
    if not already_authorized(request):
        raise Exception('not authorized request')
    open_id = request.session.get('open_id')
    user = User.objects.get(open_id=open_id)
    return user


class UserView(View):
    # 关注的城市、股票和星座
    def get(self, request):
        if not already_authorized(request):
            return JsonResponse({'key': '没登录认证'}, safe=False)
        openid = request.session.get('openid')
        user = User.objects.get(openid=openid)
        data = {}
        data['focus'] = {}
        data['focus']['city'] = json.loads(user.focus_cities)
        data['focus']['stock'] = json.loads(user.focus_stocks)
        data['focus']['constellation'] = json.loads(user.focus_constellations)
        return JsonResponse(data=data, safe=False)

    def post(self, request):
        if not already_authorized(request):
            return JsonResponse({'key': '没登录认证'}, safe=False)
        openid = request.session.get('openid')
        user = User.objects.get(openid=openid)

        received_body = request.body.decode('utf-8')
        received_body = eval(received_body)

        cities = received_body.get('city')
        stocks = received_body.get('stock')
        constellations = received_body.get('constellation')
        #  不是追加的形式,是覆盖原有纪录
        # todo 这个bug 可以自己修复下

        user.focus_cities = json.dumps(cities)
        user.focus_stocks = json.dumps(stocks)
        user.focus_constellations = json.dumps(constellations)
        user.save()

        return JsonResponse(data={'msg': '成功了'}, safe=False)
        pass


class Logout(View):
    def get(self, request):
        return JsonResponse({'000000': '1111111111'})

# 检测状态信息
class Status(View):
    def get(self, request):
        print('调用get_status函数')
        if already_authorized(request):
            data = {'is_authorized': 1}
        else:
            data = {'is_authorized': 0}
        return JsonResponse(data, safe=False)



def weather(cityname):
    '''
    :param cityname: 城市名字
    :return: 返回实况天气
    '''
    key = '写自己的key'
    api = 'http://apis.juhe.cn/simpleWeather/query'
    params = 'cityname=%s&key=%s' % (cityname, key)
    url = api + '?' + params
    print(url)
    response = requests.get(url=url)
    data = json.loads(response.text)
    print(data)
    result = data.get('result')
    realtime = result.get('realtime')
    response = {}
    response['temperature'] = realtime.get('temp')
    response['win'] = realtime.get('win')
    response['humidity'] = realtime.get('humidity')
    # response = {}
    # response['temperature'] = 'temperature'
    # response['win'] = 'win'
    # response['humidity'] = 'humidity'
    return response


class Weather(View):
    def get(self, request):
        if not already_authorized(request):
            response = {'key':2500}
        else:
            data = []
            openid = request.session.get('openid')
            user = User.objects.filter(openid=openid)[0]
            cities = json.loads(user.focus_cities)
            for city in cities:
                result = weather(city.get('city'))
                result['city_info'] = city
                data.append(result)
            response = data
        return JsonResponse(data=response, safe=False)
        pass

    def post(self, request):
        data = []
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        print(received_body)
        cities = received_body.get('cities')
        for city in cities:
            result = weather(city.get('city'))
            result['city_info'] = city
            data.append(result)
        response_data = {'key':'post..'}
        return JsonResponse(data=response_data, safe=False)