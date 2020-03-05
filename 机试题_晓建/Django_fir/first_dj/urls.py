from django.contrib import admin
from django.urls import path, include
# from . import 要被删掉的views
import app1

urlpatterns = [
    path('admin/', admin.site.urls),

    # 下面的是app1里面的
    path('app1/', include('app1.urls')),
    path('api/v1.0/', include('first_dj.v1_0')),

]

# 在生产环境下才起作用,在开发环境下没用
handler404 = app1.views.not_find_page
