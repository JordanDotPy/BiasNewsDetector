from django.apps import AppConfig
from BiasNewsDetector.webscrape_tools import newspaper_scrape, newspaper_scrape2
from BiasNewsDetector.ai_tools import full_article_sentiment_analysis
import time

class BiasnewsdetectorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'BiasNewsDetector'
"""
    def ready(self):
        from BiasNewsDetector.models import ArticleParseTime
        test_urls = ["https://www.cnn.com/2020/03/31/politics/mcconnell-impeachment-coronavirus/index.html",
                     "https://www.cnn.com/2020/03/31/politics/wisconsin-primary-coronavirus/index.html",
                     "https://www.cnn.com/2020/03/30/politics/trump-health-experts-extend-coronavirus-guidelines/index.html"]
        avg_time_per_word = 0
        for website_url in test_urls:
            start = time.time()
            newspaper_title, newspaper_text, newspaper_words = newspaper_scrape(website_url)

            # Find all named entities within the article and provide sentiment analysis
            p_sentence, neg_sentence, neu_sentence, ent_sentence, quoted_sentences, all_sentences = full_article_sentiment_analysis(newspaper_text, newspaper_title)
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
            end = time.time()
            time_per_word = (end - start)/newspaper_words
            time_per_sent = (end - start)/len(all_sentences)
            print(f"{newspaper_words} words took {end - start} seconds\n({time_per_word} seconds per word and\n{time_per_sent} seconds per sentence)")
            avg_time_per_word += time_per_word
        avg_time_per_word /= len(test_urls)
        a = ArticleParseTime(seconds_per_word = avg_time_per_word)
        a.save()
        """