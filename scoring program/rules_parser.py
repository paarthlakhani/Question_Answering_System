from constants import *
#from parser import word_tokenizer, entity_recognizer, get_noun_chunks_list, is_proper_noun, is_human
import parser as p

def word_match(morphological_root_of_question, morph_story_sentence_words):
    """ 
    Refer page number 2(bottom left para)
    Verb matches are weighed more heavily than non verb matches. Can you change it accordingly?
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

    tokenized_words = p.word_tokenizer(story_sentence)
    
    # Rule 2: identifies location preposition
    for word in tokenized_words:
        if word in location_preposition:
            score += good_clue

    # Rule 3: looks for sentences with words belonging to LOCATION semantic class
    named_entities = p.entity_recognizer(story_sentence)
    
    for entity, label in named_entities.items():
        if label in spacy_location_labels:
            # Need to add one more check here to identify LOCATION
            score += confident

    return score


def is_name_in_sentence_frag(sentence_frag):
    sentence_noun_phrase_chunk = p.get_noun_chunks_list(sentence_frag)

    sentence_contain_name = False
    for noun_phrase in sentence_noun_phrase_chunk:
        if p.is_name(noun_phrase):
            sentence_contain_name = True
            return sentence_contain_name
    return sentence_contain_name


def is_human_in_sentence(sentence_frag):
    tokenized_words = p.word_tokenizer(sentence_frag)
    for word in tokenized_words:
        if p.is_human(word):
            return True
    return False


def find_who_rules_scores(question, story_sentence):
    """
    Rules defined for 'who' type of questions
    :param question: A question with stop words (original question)
    :param story_sentence: A single sentence of a story
    :return: Score of this sentence after applying
    """
    score = 0
    # Rule 1: general word matching function
    score += word_match(question, story_sentence)

    # Rule 2
    if not is_name_in_sentence_frag(question):
        if is_name_in_sentence_frag(story_sentence):
            score += confident

    # Rule #3
    if not is_name_in_sentence_frag(question):
        if "name" in story_sentence:
            score += good_clue

    # Rule #4
    if is_name_in_sentence_frag(story_sentence) or is_human_in_sentence(story_sentence):
        score += good_clue

    return score
def find_why_rules_score(story_sentence, cur_sentence_index, best_sentence_index, best_sentence_score, cur_sentence_score):
    """
    Summary Line:
    WHY questions are handled differently than other questions.
    The WHY rules are based on the observation that the answer to WHY question often appears immediately
    before/after the sentence that most closely matches the question. This is due to the
    causal nature of WHY questions.
    The caller of this function should call WORDMATCH on all the sentences and decide the BEST sentence.
    After finding the BEST sentence, reinitialize the score of the other sentences to 0.
    (ASSUMING THAT THE BEST SENTENCE SCORE SHOULD BE INTIALIZED TO ZERO AS WELL.)
    
    Parameters:
    story_sentence(string): A string containing a sentence in the story
    cur_sentence_index: Index of the 'story_sentence' inside te story
    best_sentence_index: Index of the 'BEST sentence' inside the story
    best_sentence_score: Score of the sentence that best matched wordmatch()
    cur_senetnce_score: Score of the current sentence against wordmatch()

    Returns:
    int: Overall integer score for this sentence
    """

    score = 0

    # Rule 1: Rewards all the sentences that produced the BEST word match score
    if cur_sentence_score == best_sentence_score:
        score += clue
    
    # Rule 2: If S immed. preceeds member of BEST
    if cur_sentence_index == best_sentence_index - 1:
        score += clue

    # Rule 3: If S immed. follows member of BEST
    elif cur_sentence_index == best_sentence_index + 1:
        score += good_clue

    # Rule 4: Reawrds sentences that contain the word 'want'
    if "want" in story_sentence:
        score += good_clue
    
    # Rule 5: Rewards the sentences that contain the word 'so' or 'because'
    tokenized_words = p.word_tokenizer(story_sentence)
    for word in tokenized_words:
        if word.lower() == "so" or word.lower() == "because":
            score += good_clue
            # SHOULD WE BREAK HERE?
            
    return good_clue
        


