import sys

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

def processStory():
    pass

def processQuestions(questionsFile, storyFile):
    try:
        with open(questionsFile) as fp:
            print(fp.readlines())   
    except:
        pass
        # print("File "+questionsFile+" doesn't exist!")

'''
    dirPath: a string containing directory path to all the stories
    storyIdLst: a list of storyIds
    Return: None
    For each story Id, find the story file and the question File, then process that story to answer all the questions.
'''
def findStories(dirPath, storyIdLst):
    for story in storyIdLst:
        storyFilePath = dirPath+story+".story"
        storyQuestionFilePath = dirPath+story+".questions"
        processQuestions(storyQuestionFilePath, storyFilePath)
        

if __name__ == "__main__":
    inputFile = sys.argv[1]
    dirPath, storyIdLst = processInputFile(inputFile)
    findStories(dirPath, storyIdLst)
