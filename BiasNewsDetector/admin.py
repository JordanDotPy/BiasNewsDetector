from django.contrib import admin
from .models import UserFeedback
from sentence_transformers import SentenceTransformer
from datetime import datetime
import numpy as np
import uuid
import os


class UserFeedbackAdmin(admin.ModelAdmin):
    search_fields = ['website_url', 'output_sentiment']
    list_display = ('website_url', 'sentence', 'output_sentiment', 'correct_sentiment')
    list_editable = ['correct_sentiment', 'output_sentiment']
    actions = ['create_feedback_embeddings']

    def create_feedback_embeddings(self, request, queryset):
        model = SentenceTransformer('all-MiniLM-L6-v2')
        sentences = queryset.values_list('sentence', flat=True)

        # Generate embeddings
        embeddings = model.encode(list(sentences))

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4()
        file_path = os.path.join('BiasNewsDetector/ai_model/feedback_embeddings',
                                 f"embeddings_{timestamp}_{unique_id}.npy")
        np.save(file_path, embeddings)


# Register your models here.
admin.site.register(UserFeedback, UserFeedbackAdmin)

