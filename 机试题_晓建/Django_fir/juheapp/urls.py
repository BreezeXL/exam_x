from django.urls import path
from juheapp import views
urlpatterns = [
    path('juhe', views.hellojuhe),
    path('', views.apps),
    path('test/', views.testrequest),
    # 图片
    path('image/', views.image),
    # 图片,升级版
    path('image1/', views.ImageView.as_view()),
    # 图文
    path('imagetext/', views.ImageText.as_view()),

    path('testcookie/', views.CookieTest.as_view()),
    path('testcookie2/', views.CookieTest2.as_view()),
    # 认证的url
    path('authorization/', views.Authorization.as_view()),
    path('user/', views.UserView.as_view()),
    path('logout/', views.Logout.as_view()),
    # path('weather/', views.Weather.as_view()),

]


