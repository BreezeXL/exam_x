from django.urls import path, include
from app1 import views

urlpatterns = [
    path('hello/', views.hello),
    path('show/', views.show_detail),
    path('show_aticle/', views.show_aticle),
    path('show_aticle2/', views.show_aticle2),
    path('show_aticles/', views.show_aticles),
    path('index/', views.index),
    path('detail/<int:article_id>', views.detail2),
    path('image/', views.show_image),
    # path('detail2/<int:article_id>', views.detail2),

]

