from django.shortcuts import render
from django.template import loader
from django.http import HttpResponseRedirect
from .models import *
from django.http import JsonResponse
from BiasNewsDetector.webscrape_tools import beautifulsoup_scrape, newspaper_scrape
from BiasNewsDetector.ai_tools import analyze_bias


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
        bs4_text, bs4_words = beautifulsoup_scrape(website_url)
        newspaper_text, newspaper_words = newspaper_scrape(website_url)

        # bias_analysis = analyze_bias(website_txt)
        # Render another template and pass the URL as context
        context = {'website_url': website_url,
                   'bs4_text': bs4_text,
                   'news_words': newspaper_words,
                   'news_text':newspaper_text,
                   'bias_probabilities': None,
                   'bs4_words': bs4_words}
        return render(request, 'BiasNewsDetector/process_article.html', context)

    return HttpResponseRedirect('BiasNewsDetector/index.html')
