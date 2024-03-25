from django.shortcuts import render
from django.template import loader
from django.http import HttpResponseRedirect
from .models import *
from django.http import JsonResponse
from django.contrib import messages
from BiasNewsDetector.webscrape_tools import newspaper_scrape, newspaper_scrape2
from BiasNewsDetector.ai_tools import full_article_sentiment_analysis
from BiasNewsDetector.error import error_handler


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
    context = {}
    return render(request, 'BiasNewsDetector/team.html', context)


def process_article(request):
    if request.method == "POST":
        website_url = request.POST.get('websiteURL')
        newspaper_title, newspaper_text, newspaper_words = newspaper_scrape(website_url)

        if newspaper_words < 0:
            error_text = error_handler(newspaper_words)
            request.path = "/article/"
            messages.error(request, error_text)
            return HttpResponseRedirect(request.path)

        # Find all named entities within the article and provide sentiment analysis
        p_sentence, neg_sentence, neu_sentence, ent_sentence, quoted_sentences, all_sentences = full_article_sentiment_analysis(newspaper_text, newspaper_title)
        print("=====POSITIVE SENTENCES=====")
        print(p_sentence)
        print("=====NEGATIVE SENTENCES=====")
        print(neg_sentence)
        print("=====NEUTRAL SENTENCES=====")
        print(neu_sentence)
        print("=====ENTITY SENTENCES=====")
        print(ent_sentence)
        print("=====QUOTED SENTENCES=====")
        print(quoted_sentences)
        # Render another template and pass the URL as context
        context = {'website_url': website_url,
                   'news_words': newspaper_words,
                   'news_title': newspaper_title,
                   'news_text':newspaper_text,
                   'bias_probabilities': None,
                   'analysis_results': all_sentences,
                   'positive_sentences': p_sentence,
                   'negative_sentence': neg_sentence,
                   'neutral_sentence': neu_sentence,
                   }
        return render(request, 'BiasNewsDetector/process_article.html', context)

    return HttpResponseRedirect('BiasNewsDetector/index.html')
