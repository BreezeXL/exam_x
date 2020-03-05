import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "first_dj.settings")
django.setup()

from django.conf import settings
from django.test import TestCase
import yaml,random
from django.conf import settings
from django.db.models import Value
from django.db.models.functions import Concat
from juheapp.models import User


# 读取yaml配置文件
filepath = r'D:\study\project__\django_333\first_dj\first_dj\myappconfig.yaml'
with open(filepath, 'r', encoding='utf8') as f:
    res = yaml.load(f, Loader=yaml.FullLoader)
    print(res)
    print(type(res))


os.environ['DJANGO_SETTINGS_MODULE'] = 'myfirstproj.settings'
# static_file_path = os.path.join(settings.BASE_DIR,'static')
#
# print('static_file_path:', static_file_path)
# filename = r'/abc.png'
# filepath = os.path.join(static_file_path, filename)
# print(filepath)
print('basedir:', settings.BASE_DIR)

static_filedir = settings.STATIC_URL
# print('static_filedir',static_filedir)
print('static_filedir', os.path.join(settings.BASE_DIR, 'static'))
print(settings.STATIC_ROOT)
def ranstr(length):
    CHS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    salt = ''
    for i in range(length):
        salt += random.choice(CHS)
    return salt

# 添加一个用户
def add_one():
    # 1
    user = User(open_id = 'test_open_id', nickname='test_nickname')
    user.save()

    # 2
    User.objects.create(open_id = 'test_open_id2', nickname='test_nickname2')


def add_batch():
    new_user_list = []
    for i in range(10):
        open_id = ranstr(32)
        nickname = ranstr(10)
        user = User(open_id=open_id, nickname=nickname)
        new_user_list.append(user)
    User.objects.bulk_create(new_user_list)