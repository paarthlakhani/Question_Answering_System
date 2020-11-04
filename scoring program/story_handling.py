from nltk.tokenize import sent_tokenize

def read_story_file(story_file):
    """
    """
    with open(story_file) as fp:
        file_content = fp.readlines()
    fp.close()
    return file_content
    

def process_story(story_lines):
    """
    Summary Line:
    Returns a list of sentences in the story

    Parameters:
    story_lines(list): A list containing each line in the story file

    Returns:
    list: A list containnig story sentences.
    """

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

