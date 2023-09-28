from django.shortcuts import render
from django.template import loader
from django.http import HttpResponseRedirect
from .models import *
from django.http import JsonResponse


# Create your views here.
def home(request):
    context = {}
    return render(request, 'BiasNewsDetector/index.html', context)


def get_article(request):
    context = {}
    return render(request, 'BiasNewsDetector/get_article.html', context)


def process_article(request):
    if request.method == "POST":
        website_url = request.POST.get('websiteURL')

        # Do any other processing with the URL if needed

        # Render another template and pass the URL as context
        context = {'website_url': website_url}
        return render(request, 'BiasNewsDetector/process_article.html', context)

    return HttpResponseRedirect('BiasNewsDetector/index.html')
