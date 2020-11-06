clue = 3
good_clue = 4
confident = 6
slam_dunk = 20

all_question_type = {"why", "whose", "what", "where", "when", "how", "who", "whom"}

# common prepositions: above, along, at, below, beside, between, during, for, from, in, near, on, outside, over, past, through, towards, under, up, with
location_preposition = {"in", "on", "at", "near", "next to", "between", "far from", "opposite", "behind", "under",
                        "below", "above", "on top of", "at the top", "at the bottom", "across", "beside", "around",
                        "front"}

spacy_location_labels = {"GPE", "LOC"}


usa_names_1910_2013 = []
with open('./usa_names_1910_2013', 'r') as names_file:
    usa_names_1910_2013 = names_file.readlines()
    usa_names_1910_2013 = list(map(lambda name: name.strip(), usa_names_1910_2013))

common_titles = []
with open('./common_titles.txt', 'r') as common_titles_file:
    common_titles = common_titles_file.readlines()
    common_titles = list(map(lambda name: name.strip(), common_titles))
#print(common_titles)

human_class = usa_names_1910_2013 + common_titles

countries = []
with open("./country_names.txt") as fp:
    country_names = fp.readlines()
    countries = list(map(lambda name: name.strip(), country_names))

us_states = []
with open("./states_US.txt") as fp:
    states = fp.readlines()
    us_states = list(map(lambda name:name.strip(), states))

canadian_provinces =[]
with open("./provinces_CANADA.txt") as fp:
    provinces = fp.readlines()
    canadian_provinces = list(map(lambda name:name.strip(), provinces))

LOCATION = countries + us_states + canadian_provinces
# print(LOCATION)

MONTH = set(["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"])