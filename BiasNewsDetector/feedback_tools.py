from .models import *


def check_user_input(user_input, news_text, all_sentences, out_sentiment, correct_sentiment, website_url):
    for input in user_input:
        if input in all_sentences['sentence'].values or input in news_text:
            UserFeedback.objects.create(sentence=user_input,
                                        website_url=website_url, output_sentiment=out_sentiment,
                                        correct_sentiment=correct_sentiment)
    return 0
