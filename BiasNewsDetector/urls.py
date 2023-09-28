from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('article/', views.get_article, name='article'),
    path('process/', views.process_article, name='process_url'),
]