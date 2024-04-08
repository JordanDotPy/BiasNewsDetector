from transformers import BertTokenizer, TFBertForSequenceClassification
from sklearn.feature_extraction.text import CountVectorizer
import tensorflow as tf
import spacy
import numpy as np
import re
import json
from urllib.parse import urlparse
from spacy.matcher import Matcher
from spacytextblob.spacytextblob import SpacyTextBlob
from keyword_spacy import KeywordExtractor
from gensim.models import Word2Vec
import torch
from transformers import BertTokenizer,BertModel
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity


def find_media_bias_by_url(url):
    # Load the JSON data
    with open('BiasNewsDetector/ai_model/text_data/all_sides.json', 'r') as file:
        data = json.load(file)

    # Parse the article URL to extract the domain
    parsed_article_url = urlparse(url)
    article_domain = parsed_article_url.netloc

    # Sometimes, 'www.' is included in URLs and sometimes it's not. Removing it can help in matching.
    if article_domain.startswith('www.'):
        article_domain = article_domain[4:]

    # Iterate through the list of publications
    for item in data['allsides_media_bias_ratings']:
        publication = item['publication']
        source_url = publication.get('source_url', '')

        # Skip if source URL is empty
        if not source_url:
            continue

        # Parse the source URL to extract the domain
        parsed_source_url = urlparse(source_url)
        source_domain = parsed_source_url.netloc

        # Similarly, remove 'www.' if present
        if source_domain.startswith('www.'):
            source_domain = source_domain[4:]

        # Check if the article's domain matches the source's domain
        if article_domain == source_domain:
            return publication.get('media_bias_rating', 'Bias rating not found'), \
                   publication.get('source_name', 'Source name not found'), \
                   publication.get('allsides_url', 'ALLSides url not found')

    return None, None, None


def fix_quotes(text):
    transl_table = dict([(ord(x), ord(y)) for x,y in zip( u"‘’´“”",  u"'''\"\"")]) 
    return text.translate(transl_table)


def lexicon_reader(file):
    with open(file, 'r') as f:
        for line in f:
            yield line


def has_more_than_five_words_in_quotes(sentence):
    # Use regular expression to find all words within quotes
    words_in_quotes = re.findall(r'"([^"]+)"', sentence)
    
    # Count the number of words in quotes
    total_words_in_quotes = sum(len(re.findall(r'\w+', word)) for word in words_in_quotes)
    
    # Return True if the total number of words in quotes is more than five, False otherwise
    return total_words_in_quotes > 5


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


def compare_modifier_to_lexicons(modifier_token, head_token, positive_model, negative_model, sentiment_score):
    # Determine sentiment based on average similarity scores
    if modifier_token.dep_ == 'neg':
        if head_token.text in positive_model.wv.key_to_index:
            sentiment = "Negative"
            sentiment_score -= 0.15
        elif head_token.text in negative_model.wv.key_to_index:
            sentiment = "Positive"
            sentiment_score += 0.12
        else:
            sentiment = "Neutral"
    else:
        if head_token.text in positive_model.wv.key_to_index:
            sentiment = "Positive"
            if modifier_token.text in positive_model.wv.key_to_index:
                sentiment_score += 0.12
            sentiment_score += 0.06
        elif head_token.text in negative_model.wv.key_to_index:
            sentiment = "Negative"
            if modifier_token.text in negative_model.wv.key_to_index:
                sentiment_score -= 0.15
            sentiment_score -= 0.06
        else:
            sentiment = "Neutral"

    return sentiment, sentiment_score


def full_article_sentiment_analysis(text):
    # Load spaCy model and add SpacyTextBlob pipe if it's not already added
    text = text.replace("\n", "")
    text = fix_quotes(text)
    nlp = spacy.load("en_core_web_md")
    if not nlp.has_pipe("spacytextblob"):
        nlp.add_pipe('spacytextblob')

    positive_model = Word2Vec.load("BiasNewsDetector/ai_model/polarity/positive_lexicon.model")
    negative_model = Word2Vec.load("BiasNewsDetector/ai_model/polarity/negative_lexicon.model")

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
                sentiment, sentiment_score = compare_modifier_to_lexicons(token, token.head, positive_model, negative_model, sentiment_score)
                # sentiment, avg, sentiment_score = compare_modifier_to_lexicons(token, token.head, positive_model, negative_model, sentiment_score)

            # Check for intensifiers
            elif token.dep_ in ['amod', 'advmod'] and token.head.pos_ in ['NOUN', 'VERB', 'ADJ']:
                print(f"--- Intensifier found: {token.text} | modifying: {token.head.text}")
                print(f"Child Token: {token.text} -> {token.dep_} | Parent Token {token.head.text} -> {token.head.dep_}")
                sentiment, sentiment_score = compare_modifier_to_lexicons(token, token.head, positive_model, negative_model, sentiment_score)
                # sentiment, avg, sentiment_score = compare_modifier_to_lexicons(token, token.head, positive_model, negative_model, sentiment_score)

        # Ignore sentences below thresholds
        if sentiment_subjectivity < 0.12 or (-0.35 < sentiment_score <= 0) or (0.35 > sentiment_score >= 0) or has_more_than_five_words_in_quotes(sentence.text):
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
            "entity": entity_classifier,
            'score': sentiment_score
        })

    sentence_embedding(all_sentences)

    return positive_sentences, negative_sentences, neutral_sentences, entities_sentences, quoted_sentences, all_sentences


def generate_embeddings(sentence_list, model):
    sentences = [sentence_dict['sentence'] for sentence_dict in sentence_list]
    embeddings = model.encode(sentences)
    return embeddings


def sentence_embedding(all_sentences):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    all_embeddings = generate_embeddings(all_sentences, model)

    for idx, all_embedding in enumerate(all_embeddings):
        # Exclude the current sentence for self-comparison by creating a new array without the current sentence
        other_all_embeddings = np.concatenate([all_embeddings[:idx], all_embeddings[idx + 1:]], axis=0)
        other_all_sentences = np.concatenate([all_sentences[:idx], all_sentences[idx + 1:]], axis=0)

        # Extract the embedding for the target sentence
        target_embedding = all_embeddings[idx].reshape(1, -1)  # Reshape for cosine_similarity

        # Calculate cosine similarity between target and all other sentences
        similarities = cosine_similarity(target_embedding, other_all_embeddings)[0]

        # Find the index of the most similar sentence (excluding the target sentence itself)
        most_similar_index = np.argmax(similarities)

        # Retrieve the most similar sentence and its sentiment
        most_similar_sentence = other_all_sentences[most_similar_index]['sentence']
        most_similar_sentiment = other_all_sentences[most_similar_index]['sentiment']
        similarity_score = similarities[most_similar_index]

        # print(f"Sentence: {all_sentences[idx]['sentence']}")
        # print(f"most similar to sentence: {most_similar_sentence}")
        # print(f"Sentiment of similar sentence: {most_similar_sentiment}")
        # print(f"Similarity Score: {similarity_score}\n")

        if similarity_score >= 0.75:
            all_sentences[idx]['sentiment'] = most_similar_sentiment
