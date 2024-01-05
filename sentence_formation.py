
import re
import spacy
from spellchecker import SpellChecker

spell = SpellChecker()
nlp = spacy.load("en_core_web_sm")
stop_words = ["a", "an", "the", "to", "be", "being", "have", "having", "has", "been", "was", "were", "will", "could", "would", "may", "might", "ought", "by", "at", "as", "on", "for", "is", "are", "of", "in", "did", "does", "didn't", "doesn't", "about", "into", "around", "couldn't", "wasn't", "weren't", "won't", "not", "can", "can't"]


def single_word_formater(word, sentence):
    input_word = word

    word = word.split()
    word = [i for i in word if i.lower() not in stop_words]
    word = "".join(word)

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
                gap_sentence = " ".join(gap_sentence[1:])

                status = True
                return (gap_sentence, sentence, input_word, status)
            
        error = f'К сожалению, нейронным сетям тоже свойственно ошибаться, сгенерировать предложение со словом "{input_word}" не вышло 😓'
        status = False
        return (error, error, input_word, status)
    except:
        status = False
        error = f'К сожалению, нейронным сетям тоже свойственно ошибаться, сгенерировать предложение со словом "{input_word}" не вышло 😓'
        return [error, error, input_word, status]


def word_formater(word, sentence):

  input_word = word

  word = word.split()
  word = [i for i in word if i.lower() not in stop_words]
  word = "".join(word)

  formated_sentence = re.sub(r'[^\-\'\w\s]', '', sentence.lower())
  formated_sentence = formated_sentence.split()
  
  try:
    for i in range(len(formated_sentence)):
      if formated_sentence[i] == word.lower():
          index = i
          break
      elif word.lower() in formated_sentence[i]:
          index = i
          break
      
    gap_sentence = sentence.split()
    gap_sentence[index] = gap_sentence[index].lower().replace(formated_sentence[index], "[G_A_P]")
    gap_sentence = " ".join(gap_sentence[1:])

    return (gap_sentence, sentence, formated_sentence[index], True)
  except:
     res = single_word_formater(input_word, sentence)
     return res
  
  