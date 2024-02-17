from transformers import BertTokenizer, TFBertForSequenceClassification
import tensorflow as tf


def analyze_bias(text):
    # Load tokenizer and model
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = TFBertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)

    # Tokenize text and manage long texts
    inputs = tokenizer(text, return_tensors="tf", padding=True, truncation=True, max_length=512)

    # Make predictions
    outputs = model(inputs)
    logits = outputs.logits

    # Apply softmax to convert logits to probabilities
    probabilities = tf.nn.softmax(logits, axis=-1)

    # Convert probabilities to JSON serializable format
    probabilities_json = probabilities.numpy().tolist()

    # Return the analysis result
    return {'probabilities': probabilities_json}
