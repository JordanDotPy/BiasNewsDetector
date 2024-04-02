from .models import *


def check_user_input(user_input, all_sentences, out_sentiment, correct_sentiment, website_url):
    valid_feedback = False
    # Iterate through each dictionary in the all_sentences list
    user_input = user_input.strip()
    for sentence_dict in all_sentences:
        # Check if user_input matches the 'sentence' value in the current dictionary
        if user_input == sentence_dict['sentence'] and user_input != '' and out_sentiment != correct_sentiment:
            if sentence_dict['sentiment'] == out_sentiment:
                duplicate_sentence = UserFeedback.objects.filter(sentence=user_input,
                                                                 website_url=website_url, output_sentiment=out_sentiment,
                                                                 correct_sentiment=correct_sentiment)
                if not duplicate_sentence.exists():
                    UserFeedback.objects.create(sentence=user_input,
                                                website_url=website_url, output_sentiment=out_sentiment,
                                                correct_sentiment=correct_sentiment)
                    valid_feedback = True
                    break
    return valid_feedback

