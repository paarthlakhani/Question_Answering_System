import rules_parser


def find_story_sentence_scores(morph_story_sentences_dict, question_type, question):
    # call the rule function
    if question_type == "why":
        morph_story_sentences_dict, best_sentence_index, best_sentence, best_sentence_score = rules_parser.find_best_sentence_for_why_rules(question, morph_story_sentences_dict)

    for sent_number, sentence_list in morph_story_sentences_dict.items():
        score = 0
        original_sentence, morphed_sentence_list = sentence_list[0], sentence_list[1]
        if question_type == "who":
            score = rules_parser.find_who_rules_scores(question, sentence_list[0], sentence_list[1]) # 0 - original, 1 - morphed
        elif question_type == "where":
            score = rules_parser.find_where_rules_score(question, sentence_list[0], sentence_list[1])
        elif question_type == "why":
            cur_score = morph_story_sentences_dict[sent_number][2]
            score = rules_parser.find_why_rules_score(original_sentence, sent_number,best_sentence_index,best_sentence_score, cur_score)
        elif question_type == "what":
            pass
        elif question_type == "when":
            pass
        elif question_type == "how":
            pass
        elif question_type == "whom":
            pass
        elif question_type == "whose":
            pass
        morph_story_sentences_dict[sent_number] = [original_sentence, morphed_sentence_list
                                                   , score]
    answer = find_matching_story_sentence(morph_story_sentences_dict, question_type, question)
    return answer


def find_answer(sentence, question_type, question):
    return sentence


def find_matching_story_sentence(morph_story_sentences_dict, question_type, question):
    max_score = 0
    matching_sentence = ''
    for sentence_number, sentence_elements in morph_story_sentences_dict.items():
        sentence, score = sentence_elements[0], sentence_elements[2]
        if score > max_score:
            max_score = score
            matching_sentence = sentence
    return find_answer(matching_sentence, question_type, question)


def question_iterator(question_pair_lst, morph_story_sentences_dict):
    for question_pair in question_pair_lst:
        #print(question_pair)
        question = question_pair["Question"]
        question_type = question_pair["Type"]
        answer = find_story_sentence_scores(morph_story_sentences_dict, question_type, question)
        print("QuestionID: " + question_pair["QuestionID"])
        print("Question: " + question)
        print("Answer: " + answer)
        print("\n")


