from django.contrib import admin
from .models import UserFeedback


class UserFeedbackAdmin(admin.ModelAdmin):
    search_fields = ['website_url', 'output_sentiment']
    list_display = ('website_url', 'sentence', 'output_sentiment', 'correct_sentiment')
    list_editable = ['correct_sentiment', 'output_sentiment']


# Register your models here.
admin.site.register(UserFeedback, UserFeedbackAdmin)

