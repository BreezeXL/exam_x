from django.urls import path
from app1 import views

urlpatterns = [
    path('', views.index),
    # path('hello/',views.hello_world),
    path('content', views.acticle_content),
    path('index', views.get_index_page),
    # path('detail',views.get_detail_page),
    path('detail/<int:article_id>', views.get_detail_page)

]
