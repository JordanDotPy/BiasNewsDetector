from gensim.models import Word2Vec
from gensim.models.word2vec import PathLineSentences


def preprocess_and_tokenize(input_file, output_file=None):
    cleaned_sentences = []
    with open(input_file, 'r', encoding='utf-8') as f_in:
        for line in f_in:
            # Remove leading '0' and any spaces after it
            cleaned_line = line.lstrip('0 ').rstrip('\n')
            # Tokenize the cleaned line into words
            tokens = cleaned_line.split()
            cleaned_sentences.append(tokens)
            # Optionally write to a new file
            if output_file:
                with open(output_file, 'a', encoding='utf-8') as f_out:
                    f_out.write(" ".join(tokens) + '\n')
    return cleaned_sentences

# Assuming you have your corpus in a directory where each file is a document
# general_bias_lexicon = 'BiasNewsDetector/ai_model/text_data/bias-lexicon.txt'
positive_lexicon = 'BiasNewsDetector/ai_model/text_data/lexicons/positive_lexicon.txt'
negative_lexicon = 'BiasNewsDetector/ai_model/text_data/lexicons/negative_lexicon.txt'

# Training a Word2Vec model
sentences = PathLineSentences(positive_lexicon)
model = Word2Vec(sentences=sentences, vector_size=100, window=5, min_count=1, workers=4)
model.save("positive_lexicon.model")
print("General Lexicon Model Done!")

sentences = PathLineSentences(negative_lexicon)
model = Word2Vec(sentences=sentences, vector_size=100, window=5, min_count=1, workers=4)
model.save("negative_lexicon.model")
print("General Lexicon Model Done!")

