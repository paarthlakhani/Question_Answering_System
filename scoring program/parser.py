import nltk, spacy
from nltk.corpus import stopwords
nlp = spacy.load("en_core_web_sm")

stopWords = set(stopwords.words('english'))

def removeStopWords(sentence):
    """
    Summary line:
    This function simply checks if the current word in belongs to stop words set. If not it adds it to te output list.

    Parameters:
    sentence(string): a string whose stop words need to be removed

    Returns:
    string: a string without stop words
    
    """

    wordsInSentence = nltk.word_tokenize(sentence)
    sentenceWithoutStopWords = " ".join([word for word in wordsInSentence if word not in stopWords])
    return sentenceWithoutStopWords

def word_tokenizer(sentence):
    """
    Summary Line:
    Converts the given sentence into list of words, punctuations

    Parameters:
    sentence(string): Sentence needs to be tokenized

    Returns:
    list: A list of words, punctuations in the sentence
    """

    return nltk.word_tokenize(sentence)

def pos_tagger(sentence):
    """
    Summary Line:
    Finds the POS for each word in the sentence

    Parametrs:
    sentence(string): A sentence

    Returns:
    dict: key being the word and value being the POS tag for the word
    """

    doc = nlp(sentence)
    pos_dict = {}
    for token in doc:
        pos_dict[token.text] = token.pos_
    return pos_dict

def entity_recognizer(sentence):
    """
    Summary Line:
    Finds the named entities in the sentence

    Parameters:
    sentence(string): A sentence

    Returns:
    dict: key being the entity and value being the label for that entity
    """

    doc = nlp(sentence)
    entity_dict = {}
    for ent in doc.ents:
        entity_dict[ent.text] = ent.label_
    return entity_dict

