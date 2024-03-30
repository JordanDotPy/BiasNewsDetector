from django.apps import AppConfig
from BiasNewsDetector.webscrape_tools import newspaper_scrape, newspaper_scrape2
from BiasNewsDetector.ai_tools import full_article_sentiment_analysis
import time

class BiasnewsdetectorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'BiasNewsDetector'
