from django.urls import path, include
from juheapp import views
#
urlpatterns = [
    path('juhe/', views.hellojuhe),
    path('test/', views.testrequest),
    path('image/', views.image),
    path('image1/', views.ImageView.as_view()),
    path('imagetext/', views.ImageText.as_view()),
    path('', views.apps),

]

