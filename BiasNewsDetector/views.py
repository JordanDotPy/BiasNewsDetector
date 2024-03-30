from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponseRedirect
from .models import *
from django.http import JsonResponse
from BiasNewsDetector.webscrape_tools import newspaper_scrape, newspaper_scrape2
from BiasNewsDetector.ai_tools import full_article_sentiment_analysis
from BiasNewsDetector.feedback_tools import check_user_input
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


def feedback(request):
    if request.method == "POST":
        # Extract lists of feedback from the request
        sentences = request.POST.getlist('sentence[]')
        output_analyses = request.POST.getlist('output_analysis[]')
        correct_analyses = request.POST.getlist('correct_analysis[]')
        website_url = request.POST.get('website_url', '')
        news_text = request.POST.get('news_text', '')
        all_sentences = request.session.get('all_sentences', [])

        # Initialize an empty list to hold all feedback entries
        feedback_entries = []

        # Iterate over the sentences and their corresponding analyses
        for i, sentence in enumerate(sentences):
            # Ensure there's an output and correct analysis for each sentence
            output_analysis = output_analyses[i] if len(output_analyses) > i else None
            correct_analysis = correct_analyses[i] if len(correct_analyses) > i else None

            # Here you can process each piece of feedback, e.g., check user input, save to database
            valid_feedback = check_user_input(sentence, all_sentences,output_analysis, correct_analysis, website_url)
            if valid_feedback:
                # Append a dictionary for each feedback entry to the feedback_entries list
                feedback_entries.append({
                    'feedback_sentence': sentence,
                    'output_analysis': output_analysis,
                    'correct_analysis': correct_analysis,
                    # 'feedback_analysis': feedback_analysis,  # Assuming this returns some result
                })

        # Pass the list of feedback entries to your context
        context = {
            'feedback_entries': feedback_entries,
            'news_text': news_text
        }

        return render(request, 'BiasNewsDetector/feedback.html', context)

    # Redirect to a different page if not a POST request
    return redirect('BiasNewsDetector/index.html')


def process_article(request):
    if request.method == "POST":
        website_url = request.POST.get('websiteURL')
        newspaper_title, newspaper_text, newspaper_words, authors = newspaper_scrape(website_url)

        if newspaper_words < 0:
            return error_handler(request, newspaper_title)

        # Find all named entities within the article and provide sentiment analysis
        p_sentence, neg_sentence, neu_sentence, ent_sentence, quoted_sentences, all_sentences = full_article_sentiment_analysis(newspaper_text, newspaper_title)
        request.session['all_sentences'] = all_sentences
        print("=====POSITIVE SENTENCES=====")
        print(p_sentence)
        print("=====NEGATIVE SENTENCES=====")
        print(neg_sentence)
        print("=====NEUTRAL SENTENCES=====")
        print(neu_sentence)
        print("=====ENTITY SENTENCES=====")
        print(ent_sentence)
        # Render another template and pass the URL as context
        context = {'website_url': website_url,
                   'news_words': newspaper_words,
                   'news_title': newspaper_title,
                   'news_text': newspaper_text,
                   'bias_probabilities': None,
                   'analysis_results': all_sentences,
                   'positive_sentences': p_sentence,
                   'negative_sentence': neg_sentence,
                   'neutral_sentence': neu_sentence,
                   'all_sentences': all_sentences,
                   'entity_sentences': ent_sentence
                   }
        return render(request, 'BiasNewsDetector/process_article.html', context)

    return HttpResponseRedirect('BiasNewsDetector/index.html')
