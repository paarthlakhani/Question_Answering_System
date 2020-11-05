import string
import sys, nltk
from nltk.stem.porter import PorterStemmer

from extract_answers import question_iterator
from processQuestions import findQuestionType
from parser import removeStopWords
from nltk.tokenize import sent_tokenize
from story_handling import process_story, morph_story_sentences
from question_handling import process_questions_file
from rules_parser import find_who_rules_scores


def processInputFile(inputFile):
    """
    Summary Line:
    Process the input file
    First line of the inputfile: contains a path to the directory that has all the stories and questions
    subsequent lines: story Ids

    Parametrs:
    inputFile: inputfile from 'qa <inputfile>' command passed from command line
    
    Return: directory path as a string and story ids as a list
    """
    with open(inputFile) as fp:
        lines = fp.readlines()
        dirPath = lines[0].strip("\n").strip(" ")
        storyIds = [storyId.strip("\n").strip(" ") for storyId in lines[1:]]
        return dirPath, storyIds





def find_questions_and_story(questionsFile, storyFilePath):
    """
    Summary Line:
    We might have to refactor this function. Ideally I prefer doing only one type of work inside a function. Currently not sure what this should do!

    Parameters:
    questionsFile: File that has a list of questions need to be answered
    storyFile: File name that has the story for the questions listed in questionsFile

    Return: None
    """
    morph_story_sentences_dict = morph_story_sentences(storyFilePath)
    question_pair_lst = process_questions_file(questionsFile)
    question_iterator(question_pair_lst, morph_story_sentences_dict)


def find_stories(dirPath, storyIdLst):
    """
    Summary Line:
    For each story Id, find the story file and the question File, then process that story to answer all the questions.

    Parameters:
    dirPath(string): has directory path to all the stories
    storyIdLst(list): a list of storyIds

    Returns:
    None
    """

    for storyId in storyIdLst:
        storyFilePath = dirPath + storyId + ".story"
        storyQuestionFilePath = dirPath + storyId + ".questions"
        find_questions_and_story(storyQuestionFilePath, storyFilePath)
        

if __name__ == "__main__":
    inputFile = sys.argv[1]
    dirPath, storyIdLst = processInputFile(inputFile)
    find_stories(dirPath, storyIdLst)
