from transformers import BertTokenizer, TFBertForSequenceClassification
import tensorflow as tf
import spacy
from spacy.matcher import Matcher


def find_bias(text):
    nlp = spacy.load("en_core_web_sm")

    # Define rule-based patterns for bias or factual statements
    bias_patterns = [[{"LOWER": "clearly"}], [{"LOWER": "obviously"}], [{"LOWER": "worst"}], [{"LOWER": "best"}], [{"LOWER": "unfair"}], [{"LOWER": "crazy"}], [{"LOWER": "fair"}], [{"LOWER": "significant"}]]
    fact_patterns = [[{"POS": "PROPN"}, {"POS": "VERB"}, {"POS": "DET"}, {"POS": "NOUN"}]]  # Simplified example

    matcher = Matcher(nlp.vocab)
    matcher.add("BIAS", bias_patterns)
    matcher.add("FACT", fact_patterns)

    doc = nlp(text)

    ''''# Tokenization
    for token in doc:
        print(token.text)

    # Linguistic Annotations
    print("Linguistic Annotations\n")
    for token in doc:
        print(token.text, token.pos_, token.dep_)

    # Parts of Speech Tags and Dependencies
    print("Parts of Speech Tags and Dependencies\n")
    for token in doc:
        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
              token.shape_, token.is_alpha, token.is_stop)

    # Named Entities
    print("Named Entities\n")
    for ent in doc.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_)'''

    # Find matches
    matches = matcher(doc)
    # Extract sentences containing the matches
    bias_sentences = set()
    for match_id, start, end in matches:
        span = doc[start:end]  # The matched span
        sentence = span.sent  # The sentence containing the matched span
        bias_sentences.add(sentence.text)

    bias_sentences = list(bias_sentences)  # Convert to list if you need ordered sentences
    print(bias_sentences)
    return bias_sentences


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
