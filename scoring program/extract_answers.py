import rules_parser
import parser as p
import constants

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
            score = rules_parser.find_why_rules_score(original_sentence, sent_number, best_sentence_index, best_sentence_score, cur_score)
        elif question_type == "what":
            score = rules_parser.find_what_rules_score(question, original_sentence, morphed_sentence_list)
        elif question_type == "when":
            score = rules_parser.find_when_rules_score(question, sentence_list[0], sentence_list[1])
        elif question_type == "how":
            score = rules_parser.find_how_rules_score(question, original_sentence, morphed_sentence_list)
        elif question_type == "whom":
            score = rules_parser.find_who_rules_scores(question, sentence_list[0], sentence_list[1])
        elif question_type == "whose":
            score = rules_parser.find_who_rules_scores(question, sentence_list[0], sentence_list[1])
        elif question_type == "which":
            pass
        morph_story_sentences_dict[sent_number] = [original_sentence, morphed_sentence_list
                                                   , score]
    answer = find_matching_story_sentence(morph_story_sentences_dict, question_type, question)
    return answer

def extract_where_answer(sentence, question):
    # Where is something located?
    answer_sentence = ''
    named_entities = p.entity_recognizer(sentence)
    if len(named_entities) == 1:
        for key in named_entities:
            answer_sentence += key
        return answer_sentence
        
    if "locate" or "live" in question.lower():
        # print("The sentence is:", sentence, "\nThe question is:",question)
        for entity, label in named_entities.items():
            if label == "GPE" or label == "LOC" or label in constants.LOCATION:
                if answer_sentence:
                    answer_sentence += " " + entity
                else:
                    answer_sentence = entity
        return answer_sentence if answer_sentence else sentence
    #where did find something
    return sentence

def extract_why_answer(sentence, question):
    answer_sentence = ''
    if "because" in sentence.lower():
        words = sentence.lower().split()
        i = -1
        for i, word in enumerate(words):
            if "because" in word:
                i += 1
                answer_sentence += word
                break
        while i < len(words) and words[i].isalpha():
            answer_sentence += " " + words[i]
            i += 1
        return answer_sentence
    if "so" in sentence.lower():
        words = sentence.lower().split()
        i = -1
        for i, word in enumerate(words):
            if "so" in word:
                i += 1
                answer_sentence += word
                break
        while i < len(words) and words[i].isalpha():
            answer_sentence += " " +words[i]
            i += 1
        return answer_sentence

    return sentence


def extract_how_answer(sentence, question):
    tokenized_words = p.word_tokenizer(sentence)
    named_entities = p.entity_recognizer(sentence)
    for entity, label in named_entities.items():
        if label in set(["QUANTITY", "MONEY", "PERCENT", "DATE"]):
            return entity
    for i, word in enumerate(tokenized_words):
        if word.isdigit() or "$" in word or "%" in word:
            return "t".join(tokenized_words[i:i+2])
    return sentence



def find_answer(sentence, question_type, question):
    if question_type == "where":
        return extract_where_answer(sentence, question)
    # if question_type == "how":
    #     return extract_how_answer(sentence, question)
    # if question_type == "why":
    #     return extract_why_answer(sentence, question)
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


def question_iterator(question_pair_lst, morph_story_sentences_dict, output_file):
    for question_pair in question_pair_lst:
        question = question_pair["Question"]
        question_type = question_pair["Type"]
        answer = find_story_sentence_scores(morph_story_sentences_dict, question_type, question)
        answer = answer.strip('\n')
        answer = answer.replace('\n', ' ')
        question_id_write = "QuestionID: " + question_pair["QuestionID"].strip()
        question = "Question: " + question.strip()
        answer_write = "Answer: " + answer + "\n"
        print(question_id_write)
        #print(question)
        print(answer_write)
        output_file.write(question_id_write)
        output_file.write("\n")
        output_file.write(answer_write)
        output_file.write("\n")
