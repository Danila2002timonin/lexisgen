import re
import spacy
from spellchecker import SpellChecker

spell = SpellChecker() #зачем?
nlp = spacy.load("en_core_web_sm")

def single_word_formater(word, sentence, data_type):
    input_word = word

    try:
        gap_sentence = sentence.split()

        omitted_punct = re.sub(r'[^\-\'\w\s]', '', sentence.lower())
        
        tokenized_sentence = nlp(omitted_punct)
        tokenized_sentence_list = omitted_punct.split()
        word = word.lower()
        word = nlp(word)

        for token in tokenized_sentence:
            if word[0].lemma_ == token.lemma_:

                ind = tokenized_sentence_list.index(str(token.text))
                tagged_word = tokenized_sentence_list[ind]
                gap_sentence[ind] = "[G_A_P]"
                gap_sentence = " ".join(gap_sentence)

                status = True
                return (gap_sentence, sentence, input_word, status, ind)
            
        error = f'К сожалению, нейронным сетям тоже свойственно ошибаться, сгенерировать предложение со словом "{input_word}" не вышло 😓'
        status = False
        return (error, error, input_word, status)
    except:
        status = False
        error = f'К сожалению, нейронным сетям тоже свойственно ошибаться, сгенерировать предложение со словом "{input_word}" не вышло 😓'
        return [error, error, input_word, status]


def word_formater(word, sentence, data_type):

  input_word = word

  formated_sentence = re.sub(r'[^\-\'\w\s]', '', sentence.lower())
  formated_sentence = formated_sentence.split()
  
  try:
    for i in range(len(formated_sentence)):
      if formated_sentence[i] == word.lower():
          index = i
          break
    # else:
    #   for i in range(len(formated_sentence)):
    #     if word.lower() in formated_sentence[i]:
    #         index = i
    #         break
      
    gap_sentence = sentence.split()
    gap_sentence[index] = gap_sentence[index].lower().replace(formated_sentence[index], "[G_A_P]")
    gap_sentence = " ".join(gap_sentence)

    return (gap_sentence, sentence, formated_sentence[index], True, index)
  except:
     res = single_word_formater(input_word, sentence, data_type)
     return res
  
  
def multiple_word_formater(phrase, sentence, data_type):

  if data_type:
    stop_words = ["a", "an", "not", "someone", "something", "somewhere", "to", "am", "are", "is"]

    phrase = phrase.split()
    phrase = [i for i in phrase if i.lower() not in stop_words]
    phrase = " ".join(phrase)

  sentence = sentence.split()
  if sentence[0][0] in "1234567890":
     sentence = sentence[1:]
  
  sentence = " ".join(sentence)

  gap_sentence, answer, indexes, final_status, final_answer = sentence, [], [], [], []

  ind_dict = {}
  ind_difference = {}

  for word in phrase.lower().split():
    ind_dict[word] = []

  for word in phrase.lower().split():
    temp_sentence = sentence.lower()

    for i in range(len(sentence.split())):
      data = word_formater(word, temp_sentence, data_type)
      if data[3]:
         ind = data[4]
         ind_dict[word].append(ind)
         temp_sentence = data[0]
         final_status.append(True)
      else:
        final_status.append(False)
        try:
          if len(ind_dict[word]) == 0:
            del ind_dict[word]
        except:
          pass

  if True in final_status:
  # if False not in final_status:

    if len(list(ind_dict.keys())) > 1:
      for i in ind_dict[list(ind_dict.keys())[0]]:
        for j in ind_dict[list(ind_dict.keys())[1]]:
          ind_difference[abs(i - j)] = (i, j)

      first_ind = ind_difference[min(list(ind_difference.keys()))][0]
      indexes.append(first_ind)

      temp_k = -10000000000000000000000000
      for key in list(ind_dict.keys())[1:]:
        for k in sorted(ind_dict[key]):
          if k > first_ind and k > temp_k:
            temp_k = k
            indexes.append(k)
            break
    else:
      indexes.append(ind_dict[list(ind_dict.keys())[0]][0])

    gap_sentence = gap_sentence.split()

    for ind in indexes:
      final_answer.append(gap_sentence[ind])
      gap_sentence[ind] = "[G_A_P]"

    final_gap_sentence = gap_sentence.copy()
    sentence_with_all_gaps = gap_sentence.copy()

    for i in range(len(gap_sentence)-1):
       if gap_sentence[i] == '[G_A_P]' and gap_sentence[i+1] == '[G_A_P]':
          final_gap_sentence[i] = '[DELETE]'

    final_gap_sentence_v2 = []
    for w in final_gap_sentence:
      if w != '[DELETE]':
        final_gap_sentence_v2.append(w)

    gap_sentence = " ".join(final_gap_sentence_v2)
    final_answer = " ".join(final_answer)
    sentence_with_all_gaps = " ".join(sentence_with_all_gaps)

    return (gap_sentence, sentence, final_answer, True, sentence_with_all_gaps)

  else:
      status = False
      error = f'К сожалению, нейронным сетям тоже свойственно ошибаться, сгенерировать предложение с "{phrase}" не вышло 😓'
      return [error, error, phrase, status, error]
  