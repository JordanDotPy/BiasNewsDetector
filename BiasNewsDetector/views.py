from django.shortcuts import render
from django.template import loader
from django.http import HttpResponseRedirect
from .models import *
from django.http import JsonResponse
from BiasNewsDetector.webscrape_tools import beautifulsoup_scrape, newspaper_scrape
from BiasNewsDetector.ai_tools import analyze_bias, find_bias, read_large_files, ner_sentiment_analysis, kw_sentiment_analysis


# Create your views here.
def home(request):
    context = {}
    return render(request, 'BiasNewsDetector/index.html', context)


def get_article(request):
    context = {}
    return render(request, 'BiasNewsDetector/get_article.html', context)


def about(request):
    context = {}
    return render(request, 'BiasNewsDetector/about.html', context)


def team(request):
    '''
    liberal = 'BiasNewsDetector/ai_model/text_data/liberal.txt'
    conservative = 'BiasNewsDetector/ai_model/text_data/conservative.txt'
    con = read_large_files(conservative)
    x = 0
    while next(con) is not None:
        try:
            print(next(con))
        except StopIteration:
            break
        x += 1

    lib = read_large_files(liberal)

    x = 0
    while next(lib) is not None:
        try:
            print(next(lib))
        except StopIteration:
            break
        x += 1
    '''
    context = {}
    return render(request, 'BiasNewsDetector/team.html', context)


def process_article(request):
    if request.method == "POST":
        website_url = request.POST.get('websiteURL')
        bs4_text, bs4_words = beautifulsoup_scrape(website_url)
        newspaper_text, newspaper_words = newspaper_scrape(website_url)

        # bias_analysis = analyze_bias(website_txt)
        bias_sentence_list = find_bias(newspaper_text)
        # Find all named entities within the article and provide sentiment analysis
        ner_bias_sentences = ner_sentiment_analysis(newspaper_text)
        # Render another template and pass the URL as context
        context = {'website_url': website_url,
                   'bs4_text': bs4_text,
                   'news_words': newspaper_words,
                   'news_text':newspaper_text,
                   'bias_probabilities': None,
                   'bias_sentence': bias_sentence_list,
                   'analysis_results': ner_bias_sentences,
                   'bs4_words': bs4_words}
        return render(request, 'BiasNewsDetector/process_article.html', context)

    return HttpResponseRedirect('BiasNewsDetector/index.html')
