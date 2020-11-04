clue = 3
good_clue = 4
confident = 6
slam_dunk = 20

all_question_type = {"why", "whose", "what", "where", "when", "how", "who"}

# common prepositions: above, along, at, below, beside, between, during, for, from, in, near, on, outside, over, past, through, towards, under, up, with
location_preposition = set(["in", "on", "at", "near", "next to", "between", "far from", "opposite", "behind",
                        "under", "below", "above", "on top of", "at the top", "at the bottom", "across", "beside", "around","front"])

spacy_location_labels = set(["GPE", "LOC"])
