from constants import *
from parser import word_tokenizer, entity_recognizer


def word_match(morphological_root_of_question, morph_story_sentence_words):
    """ 
    Refer page number 2(bottom left para)
    Verb matches are weighed more heavily than non verb matches. Can you chage it accordingly?
    """
    score = 0
    for morph_story_word in morph_story_sentence_words:
        if morph_story_word in morphological_root_of_question:
            score = score + 1
    return score


def find_where_rules_score(question, story_sentence):
    """
    Summary Line:
    Where questions almost always look for a specific location.
    Finds the over all score for this sentnce by applying various rules defined below

    Parameters:
    question(string): A question with stop words (original question)
    story_sentence(string): A sentence inside the story

    Return:
    int: Overall integer scrore for this sentence
    """
    score = 0
    # Rule 1: general word matching function
    score += word_match(question, story_sentence)

    tokenized_words = word_tokenizer(story_sentence)
    
    # Rule 2: identifies location preposition
    for word in tokenized_words:
        if word in location_preposition:
            score += good_clue

    # Rule 3: looks for sentences with words belonging to LOCATION semantic class
    named_entities = entity_recognizer(story_sentence)
    for entity, label in named_entities.items():
        if label in spacy_location_labels:
            # Need to add one more check here to identify LOCATION
            score += confident

    return score

