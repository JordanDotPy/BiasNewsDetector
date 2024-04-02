from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('about/', views.about, name='about'),
    path('team/', views.team, name='team'),
    path('article/', views.get_article, name='article'),
    path('process/', views.process_article, name='process_url'),
    path('feedback_submission/', views.feedback, name='feedback_submission')
]