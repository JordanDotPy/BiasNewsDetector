from transformers import BertTokenizer, TFBertForSequenceClassification
from sklearn.feature_extraction.text import CountVectorizer
import tensorflow as tf
import spacy
import numpy as np
import re
from spacy.matcher import Matcher
from spacytextblob.spacytextblob import SpacyTextBlob
from keyword_spacy import KeywordExtractor
from gensim.models import Word2Vec

def fix_quotes(text):
    transl_table = dict([(ord(x), ord(y)) for x,y in zip( u"‘’´“”",  u"'''\"\"")]) 
    return text.translate(transl_table)

def lexicon_reader(file):
    with open(file, 'r') as f:
        for line in f:
            yield line


def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def find_quoted_text(text):
    # Regex pattern for finding text within double or single quotes
    pattern = r'"(.*?)"'
    # Find all matches of the pattern in the sentence
    matches = re.findall(pattern, text, re.IGNORECASE)
    if matches:
        return matches
    else:
        return None


def load_lexicon(filename):
    lexicon = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            # Strip whitespace and newline characters, then add the word to the list
            word = line.strip()
            if word:  # Make sure the line is not empty
                lexicon.append(word)
    return lexicon


def compare_word_to_lexicons(word, positive_model, negative_model, sc):
    positive_similarity = 0
    negative_similarity = 0
    positive_count = 0
    negative_count = 0

    if word in positive_model.wv.key_to_index:
        for vocab_word in positive_model.wv.index_to_key:
            positive_similarity += positive_model.wv.similarity(word, vocab_word)
            positive_count += 1
    if word in negative_model.wv.key_to_index:
        for vocab_word in negative_model.wv.index_to_key:
            negative_similarity += negative_model.wv.similarity(word, vocab_word)
            negative_count += 1

    # Avoid division by zero
    positive_avg = positive_similarity / positive_count if positive_count else 0
    negative_avg = negative_similarity / negative_count if negative_count else 0

    if positive_avg > negative_avg:
        sc += 0.12
        return "positive", positive_avg, sc
    elif negative_avg > positive_avg:
        sc -= 0.12
        return "negative", negative_avg, sc
    else:
        return "neutral", 0, sc


def full_article_sentiment_analysis(text, title):
    # Load spaCy model and add SpacyTextBlob pipe if it's not already added
    text = text.replace("\n", "")
    text = fix_quotes(text)
    nlp = spacy.load("en_core_web_md")
    if not nlp.has_pipe("spacytextblob"):
        nlp.add_pipe('spacytextblob')

    conservative_model = Word2Vec.load("BiasNewsDetector/ai_model/conservative.model")
    liberal_model = Word2Vec.load("BiasNewsDetector/ai_model/liberal.model")
    general_model = Word2Vec.load("BiasNewsDetector/ai_model/generic_lexicon.model")
    positive_model = Word2Vec.load("BiasNewsDetector/ai_model/positive_lexicon.model")
    negative_model = Word2Vec.load("BiasNewsDetector/ai_model/negative_lexicon.model")

    doc = nlp(text)
    # Initialize lists to store sentences based on sentiment
    positive_sentences = []
    negative_sentences = []
    neutral_sentences = []
    entities_sentences = []
    all_sentences = []
    quoted_sentences = find_quoted_text(text)
    analyzed_sentences = set()

    for d in doc:
        sentence = d.sent
        if sentence in analyzed_sentences or sentence == "":
            continue  # Skip this sentence if it has already been analyzed

        analyzed_sentences.add(sentence)  # Add sentence text to the set
        sentiment_score = sentence._.blob.polarity
        sentiment_subjectivity = sentence._.blob.subjectivity

        # check if sentence has a named entity
        has_named_entity = any(ent for ent in doc.ents if ent.sent == sentence)
        # list out all named entities within the sentence
        relevant_entities = ['PERSON', 'ORG', 'GPE', 'EVENT', 'LAW', 'PRODUCT']
        entity_classifier = [ent.text for ent in doc.ents if ent.sent == sentence and ent.label_ in relevant_entities]

        # Dependency Parsing
        print("=====DEPENDENCY PARSING=====")
        for token in sentence:
            # Check for negation
            if token.dep_ == "neg":
                print(f"--- Negation found: {token.text} | modifying: {token.head.text}")
                print(f"Child Token: {token.text} -> {token.dep_} | Parent Token {token.head.text} -> {token.head.dep_}")
                sentiment, avg_similarity, sentiment_score = compare_word_to_lexicons(token.text, positive_model, negative_model, sentiment_score)
                print(f"***** Word: {token.text}, Sentiment: {sentiment}, Avg. Similarity: {avg_similarity}\n")

            # Check for intensifiers
            elif token.dep_ in ['amod', 'advmod'] and token.head.pos_ in ['NOUN', 'VERB', 'ADJ']:
                print(f"--- Intensifier found: {token.text} | modifying: {token.head.text}")
                print(f"Child Token: {token.text} -> {token.dep_} | Parent Token {token.head.text} -> {token.head.dep_}")
                sentiment, avg_similarity, sentiment_score = compare_word_to_lexicons(token.text, positive_model, negative_model, sentiment_score)
                print(f"***** Word: {token.text}, Sentiment: {sentiment}, Avg. Similarity: {avg_similarity}\n")

            elif token.dep_ == "nsubj":
                # Analyze if the subject is associated with biased or charged descriptions
                print(f"Subject found in Token: {token.text} -> {token.dep_} | Parent Token {token.head.text} -> {token.head.dep_}")
                sentiment, avg_similarity, sentiment_score = compare_word_to_lexicons(token.text, positive_model, negative_model, sentiment_score)
                print(f"***** Word: {token.text}, Sentiment: {sentiment}, Avg. Similarity: {avg_similarity}\n")

            elif token.dep_ == "dobj":
                # Analyze if the object is associated with biased or charged descriptions
                print(f"Object found in Token: {token.text} -> {token.dep_} | Parent Token {token.head.text} -> {token.head.dep_}")
                sentiment, avg_similarity, sentiment_score = compare_word_to_lexicons(token.text, positive_model, negative_model, sentiment_score)
                print(f"***** Word: {token.text}, Sentiment: {sentiment}, Avg. Similarity: {avg_similarity}\n")

        # Ignore sentences below thresholds
        if sentiment_subjectivity < 0.15 or (-0.5 < sentiment_score <= 0) or (0.5 > sentiment_score >= 0):
            sentiment = 'Neutral'
            # Neutral Sentiment Sentence with Named Entity
            if has_named_entity and entity_classifier != []:
                entities_sentences.append({
                    "sentence": sentence.text,
                    "sentiment": sentiment,
                    "entity": entity_classifier,
                    'score': sentiment_score
                })
            # Neutral Sentiment Sentence
            else:
                neutral_sentences.append({
                    "sentence": sentence.text,
                    "sentiment": sentiment,
                    'score': sentiment_score
                })
        else:
            if sentiment_score > 0:
                sentiment = "Positive"
                # Positive Sentiment Sentence with Named Entity
                if has_named_entity and entity_classifier != []:
                    entities_sentences.append({
                        "sentence": sentence.text,
                        "sentiment": sentiment,
                        "entity": entity_classifier,
                        'score': sentiment_score
                    })
                # Positive Sentiment Sentence
                else:
                    positive_sentences.append({
                        "sentence": sentence.text,
                        "sentiment": sentiment,
                        'score': sentiment_score
                    })
            else:
                sentiment = "Negative"
                # Negative Sentiment Sentence with Named Entity
                if has_named_entity and entity_classifier != []:
                    entities_sentences.append({
                        "sentence": sentence.text,
                        "sentiment": sentiment,
                        "entity": entity_classifier,
                        'score': sentiment_score
                    })
                # Negative Sentiment Sentence
                else:
                    negative_sentences.append({
                        "sentence": sentence.text,
                        "sentiment": sentiment,
                        'score': sentiment_score
                    })

        all_sentences.append({
            "sentence": sentence.text,
            "sentiment": sentiment,
            "has_entity": has_named_entity,
            'score': sentiment_score
        })

    return positive_sentences, negative_sentences, neutral_sentences, entities_sentences, quoted_sentences, all_sentences
