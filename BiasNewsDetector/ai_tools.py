from transformers import BertTokenizer, TFBertForSequenceClassification
from django.http import JsonResponse


def analyze_bias(text):
    # Load tokenizer and model
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = TFBertForSequenceClassification.from_pretrained('ai_model')

    # Tokenize text and make predictions
    inputs = tokenizer(text, return_tensors="tf", padding=True, truncation=True, max_length=512)
    outputs = model(inputs)

    # Process the model's output into a human-readable format
    # This step depends on your specific model and output format

    # Return the analysis result
    return JsonResponse(outputs)

