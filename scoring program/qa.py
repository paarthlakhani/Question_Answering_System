import string
import sys

import nltk
from nltk.stem.porter import PorterStemmer
from processQuestions import findQuestionType
from stopWordsHandling import removeStopWords
from nltk.tokenize import sent_tokenize

'''
    Process the input file
    inputFile: inputfile from 'qa <inputfile>' command passed from command line
    First line of the inputfile: contains a path to the directory that has all the stories and questions
    subsequent lines: story Ids
    Return: directory path as a string and story ids as a list
'''


def processInputFile(inputFile):
    with open(inputFile) as fp:
        lines = fp.readlines()
        dirPath = lines[0].strip("\n").strip(" ")
        storyIds = [storyId.strip("\n").strip(" ") for storyId in lines[1:]]
        return dirPath, storyIds


def processStory(story_lines):
    story_sentences = []
    story_headline = story_lines[0].strip()
    story_date = story_lines[1].strip()
    story_id = story_lines[2].strip()

    story_line_no = 3
    while story_lines[story_line_no].strip() != "TEXT:":
        story_line_no = story_line_no + 1
    story_line_no = story_line_no + 1
    story = ''.join(story_lines[story_line_no:])
    story_sentences = sent_tokenize(story)
    return story_sentences


def morphological_roots(list_of_words):
    porter_stemmer = PorterStemmer()
    for word_index in range(0, len(list_of_words)):
        list_of_words[word_index] = porter_stemmer.stem(list_of_words[word_index])
    return list_of_words


def word_match(morphological_root_of_question, morph_story_sentence_words):
    score = 0
    for morph_story_word in morph_story_sentence_words:
        if morph_story_word in morphological_root_of_question:
            score = score + 1
    return score


def processQuestions(questionsFile, story_sentences):
    answer = ""
    question_id = ""
    morph_story_sentences_dict = {}
    for story_sentence_index in range(0, len(story_sentences)):
        story_sentences[story_sentence_index] = story_sentences[story_sentence_index].translate(
                        str.maketrans('', '', string.punctuation))
        story_sentence_without_stop_words = removeStopWords(story_sentences[story_sentence_index])
        tokenized_story_words = nltk.word_tokenize(story_sentence_without_stop_words)
        morph_story_words = morphological_roots(tokenized_story_words)
        morph_story_sentences_dict[story_sentence_index] = morph_story_words
    with open(questionsFile) as fp:
        questions = fp.readlines()
        for question_component in questions:
            if question_component != "\n":
                question_component = question_component.strip("\n")
                question_type_data = question_component.split(":")
                if question_type_data[0] == "QuestionID":
                    question_id = question_type_data[1]
                if question_type_data[0] == "Question":
                    sentence_score = {}
                    question = question_type_data[1]
                    question_type = findQuestionType(question.lower())
                    question_without_stop_words = removeStopWords(question)
                    print(question_without_stop_words)
                    question_without_stop_words = question_without_stop_words.translate(
                        str.maketrans('', '', string.punctuation))
                    question_words = nltk.word_tokenize(question_without_stop_words)
                    morphological_root_of_question = morphological_roots(question_words)
                    for sentence_number, morph_sentence_words in morph_story_sentences_dict.items():
                        word_match_score = word_match(morphological_root_of_question, morph_sentence_words)
                        sentence_score[sentence_number] = word_match_score
                    print(sentence_score)
            else:
                question_id = "QuestionID:" + str(question_id) + "\n"
                answer = "Answer:" + answer + "\n"
                question_id_answer = question_id + answer
                print(question_id_answer)
                answer = ""
                question_id = ""


'''
    questionsFile: File that has a list of questions need to be answered
    storyFile: File name that has the story for the questions listed in questionsFile
    Return: None
'''


def find_questions_and_story(questionsFile, storyFile):
    with open(storyFile) as story:
        story_sentences = processStory(story.readlines())
        # print(story_sentences)
    # with open(questionsFile) as fp:
    #    print(fp.readlines())
    processQuestions(questionsFile, story_sentences)


'''
    dirPath: a string containing directory path to all the stories
    storyIdLst: a list of storyIds
    Return: None
    For each story Id, find the story file and the question File, then process that story to answer all the questions.
'''


def findStories(dirPath, storyIdLst):
    for storyId in storyIdLst:
        storyFilePath = dirPath + storyId + ".story"
        storyQuestionFilePath = dirPath + storyId + ".questions"
        find_questions_and_story(storyQuestionFilePath, storyFilePath)


if __name__ == "__main__":
    inputFile = sys.argv[1]
    dirPath, storyIdLst = processInputFile(inputFile)
    findStories(dirPath, storyIdLst)
