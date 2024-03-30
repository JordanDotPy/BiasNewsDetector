from django.db import models


class NewsArticle(models.Model):
  url = models.URLField(max_length=200)
  title = models.CharField(max_length=200)
  content = models.CharField(max_length=10000)

"""
class ArticleParseTime(models.Model):
  seconds_per_word = models.DecimalField(max_digits = 5, decimal_places = 4)
"""