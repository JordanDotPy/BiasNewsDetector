from django.shortcuts import render
from django.template import loader
from .models import *
from django.http import JsonResponse


# Create your views here.
def home(request):
    context = {}
    return render(request, 'BiasNewsDetector/index.html', context)

