
from django.urls import path,include
import app1
urlpatterns = [
    path('jokes/', include('juheapp.urls')),
    path('apps/', include('juheapp.urls')),
]