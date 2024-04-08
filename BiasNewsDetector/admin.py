from django.contrib import admin
from .models import UserFeedback
from sentence_transformers import SentenceTransformer
from BiasNewsDetector.ai_tools import find_media_bias_by_url
import numpy as np
import uuid
import os


class UserFeedbackAdmin(admin.ModelAdmin):
    search_fields = ['website_url', 'output_sentiment']
    list_display = ('website_url', 'sentence', 'output_sentiment', 'correct_sentiment')
    list_editable = ['correct_sentiment', 'output_sentiment']
    list_filter = ('website_url', 'correct_sentiment')
    actions = ['create_feedback_embeddings']

    def create_feedback_embeddings(self, request, queryset):
        website_name = None
        model = SentenceTransformer('all-MiniLM-L6-v2')
        sentences = queryset.values_list('sentence', flat=True)
        # Check if the queryset is not empty and get the 'website_url' of the first object
        if queryset.exists():
            first_object_url = queryset.first().website_url
            website_name = find_media_bias_by_url(first_object_url)[1]
            website_name = website_name.replace(" ", "_")

        # Generate embeddings
        embeddings = model.encode(list(sentences))
        if website_name:
            unique_id = uuid.uuid4()
            file_path = os.path.join('BiasNewsDetector/ai_model/feedback_embeddings',
                                     f"{website_name}_{unique_id}.npy")
            np.save(file_path, embeddings)


# Register your models here.
admin.site.register(UserFeedback, UserFeedbackAdmin)

