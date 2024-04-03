from django.db import models


class UserFeedback(models.Model):
    website_url = models.URLField(max_length=200)
    sentence = models.CharField(max_length=200)
    output_sentiment = models.CharField(max_length=50)
    correct_sentiment = models.CharField(max_length=50)