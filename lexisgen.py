import streamlit as st
from gpt import bot
from bestcomponentever import input_field
from streamlit_tags import st_tags
from sentence_formation import word_formater
import random
import time
import spacy
import json
import re
from deta import Deta
from streamlit_extras.grid import grid
# import environ


#Необходимый модуль для проверки правописания

from spellchecker import SpellChecker
spell = SpellChecker()

#Конфигурация внешенго вида сраницы, скрытие встроенных эелементов

st.set_page_config(
    page_title="LexisGen",
    page_icon="",
    layout="wide",
    initial_sidebar_state="auto"
)

st.markdown("""
<style>div[data-testid="stToolbar"] { display: none;}</style>
""", unsafe_allow_html=True)

#база данных приложения
# env = environ.Env()
# environ.Env.read_env()

base_key = "c03jv3hc1sq_xXhXWPVcKULDSaBXbwjaWJS3Qx4JacXV"
# base_key = env('DATABASE_KEY')
deta = Deta(base_key)
database = deta.Base("users")


# загрузка файла с контекстами
@st.cache_data(show_spinner=False)
def load_contexts():
    with open('./contexts.json') as json_file:
        data = json.load(json_file)
    return data

contexts = load_contexts()

# инициализация английского словаря
@st.cache_resource
def load_dictionary(dict_type):
    nlp = spacy.load(dict_type)
    return nlp

nlp = load_dictionary("en_core_web_sm")

#Определение констант, флагов и коллекций данных
main_prompt = '''You are provided with a list of words and contexts, and you should generate a list of sentences at elementary English level, where the mentioned words are used in the appropriate context. When making sentences, follow these requirements:
1. Form of these words remain unchanged.
2. You have to provide only one sentence for each word and nothing else.
3. These words are not replaced with synonyms.
4. Each sentence must contain at least 20 words.'''

if "define_initial_values" not in st.session_state:
    st.session_state.define_initial_values = True

if "data" not in st.session_state:
    st.session_state.data = [{"role": "system", "content": main_prompt}]

if "level" not in st.session_state:
    st.session_state.level = "middle"

if "stop_words" not in st.session_state:
    st.session_state.stop_words = ["a", "an", "the", "to", "be", "being", "have", "having", "has", "been", "was", "were", "will", "could", "would", "may", "might", "ought", "by", "at", "as", "on", "for", "is", "are", "of", "in", "did", "does", "didn't", "doesn't", "about", "into", "around", "couldn't", "wasn't", "weren't", "won't", "not"]

if "propriate_length" not in st.session_state:
    st.session_state.propriate_length = True

if "propriate_spell" not in st.session_state:
    st.session_state.propriate_spell = True

if "responses" not in st.session_state:
    st.session_state.responses = []

if "formated_responses" not in st.session_state:
    st.session_state.formated_responses = []

if "number_of_sentenses" not in st.session_state:
    st.session_state.number_of_sentenses = 0

if "answers" not in st.session_state:
    st.session_state.answers = []

if "unique_key" not in st.session_state:
    st.session_state.unique_key = 0

if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}

if "check_answers" not in st.session_state:
    st.session_state.check_answers = False

if "check_language" not in st.session_state:
    st.session_state.check_language = True

if "not_in_sw" not in st.session_state:
    st.session_state.not_in_sw = True

if "key_is_provided" not in st.session_state:
    st.session_state.key_is_provided = False
    
if "tokens" not in st.session_state:
    st.session_state.tokens = 0

if "collections" not in st.session_state:
    st.session_state.collections = []

if "show_answers_form" not in st.session_state:
    st.session_state.show_answers_form = False

if "results" not in st.session_state:
    st.session_state.results = []

if "gens_number" not in st.session_state:
    st.session_state.gens_number = 0

if "show_submit_form" not in st.session_state:
    st.session_state.show_submit_form = False

if "allow_generation" not in st.session_state:
    st.session_state.allow_generation = False

if "error_item" not in st.session_state:
    st.session_state.error_item = ""

if "input_item" not in st.session_state:
    st.session_state.input_item = ""

if "initial_values" not in st.session_state:
    st.session_state.initial_values = []

if "acsses_key" not in st.session_state:
    st.session_state.acsses_key = ""

with st.sidebar:


    if acsses_key := st.text_input("Ключ доступа", type="password", autocomplete=""):
        if acsses_key != "":
            @st.cache_data()
            def check_acsses_key(token):
                if database.get(token) != None:

                    key_is_provided = True
                    # st.toast("Вы успешно авторизированы!", icon="✨")
                    return key_is_provided
                else:
                    key_is_provided = False
                    return key_is_provided
            st.session_state.key_is_provided = check_acsses_key(acsses_key)

            if st.session_state.key_is_provided:
                data = database.get(acsses_key)

                st.session_state.acsses_key = data["access_key"]


                st.session_state.gens_number = data["gens_number"]

            else:
                    st.warning("Ключ доступа недействителен либо введен неверно")
        else:
            st.session_state.key_is_provided = False
    else:
        st.session_state.key_is_provided = False

main_grid_1 = grid([5, 4.5, 2])
main_grid = grid([2, 4.5, 2])

main_grid_1.write("")
# main_grid_1.title("📚 LexisGen", anchor=False)
main_grid_1.title(" LexisGen", anchor=False)
main_grid_1.write("")

main_grid.write("")

with main_grid.container():
    st.write("")
    st.write("")

    with st.form("words input"):
        if "keywords" not in st.session_state:
            st.session_state.keywords = []

        text, maxtags = ('Нажмине Enter, чтобы добавить слово', 8)

        st.subheader("Введите слова:", anchor=False)

        if keywords := st_tags(label="", text=text, value=[], maxtags = 8, key='keyword'): 
            st.session_state.keywords = keywords

            st.session_state.propriate_spell = True
            st.session_state.propriate_length = True

        #основная логика программы
        if st.form_submit_button("Сгенерировать"):
            for item in st.session_state.keywords:

                #проверка, относится ли слово к английскому языку

                reg = re.compile(r'[a-zA-Z]')
                if reg.match(item.lower()):
                    st.session_state.check_language = True
                else:
                    st.session_state.check_language = False
                    st.session_state.error_item = item

                # проверка корректности введеного слова 
                # Если слово написано неверно, то предложить исправленный вариант, если вариантов нет - указать, что такого слова не существует

                try:
                    temp = item.lower().replace('-', " ")
                    temp = temp.split()
                    misspelled = spell.unknown(temp)
                    if len(misspelled) > 0:
                        st.session_state.propriate_spell = False
                        for w in misspelled:
                            i = temp.index(w)
                            temp[i] = spell.correction(w)
                    
                        st.session_state.error_item = " ".join(temp)
                        st.session_state.input_item = item
                except:
                    st.session_state.propriate_spell = "impossible_word"
                    st.session_state.input_item = item

                #проверка, является ли введенный текст словочетанием или отдельным словом

                if len(item.split()) > 1:
                    t = 0
                    for w in item.split():
                        if w.lower() in st.session_state.stop_words:
                            continue
                        else:
                            t += 1
                    if t > 1:
                        st.session_state.propriate_length = False
                        st.session_state.error_item = item

                #проверка на отношение Только к списку стоп-слов

                if item.lower().strip() in st.session_state.stop_words:
                    st.session_state.not_in_sw = False
                    st.session_state.error_item = item
                else:
                    st.session_state.not_in_sw = True

                if st.session_state.propriate_length and st.session_state.propriate_spell == True and st.session_state.check_language and st.session_state.not_in_sw and len(st.session_state.keywords) >= 2 and st.session_state.gens_number > 0:
                    st.session_state.allow_generation = True
                else:
                    if st.session_state.gens_number == 0:
                        st.session_state.allow_generation = False
                    if len(st.session_state.keywords) <= 2:
                        st.session_state.allow_generation = False
                    if st.session_state.propriate_length == False:
                        st.session_state.allow_generation = False
                    if st.session_state.check_language == False:
                        st.session_state.allow_generation = False
                    if st.session_state.propriate_spell == "impossible_word" and st.session_state.check_language:
                        st.session_state.allow_generation = False
                    if st.session_state.propriate_spell == False:
                        st.session_state.allow_generation = False
                    if st.session_state.not_in_sw == False:
                        st.session_state.allow_generation = False

            if st.session_state.key_is_provided:
                if st.session_state.allow_generation:

                    st.session_state.responses.clear()
                    st.session_state.formated_responses.clear()
                    st.session_state.answers.clear()
                    st.session_state.user_answers.clear()
                    st.session_state.url_q = 0
                    st.session_state.check_answers = False
                    st.session_state.data = [{"role": "system", "content": main_prompt}]
                    st.session_state.results = ""
                    st.session_state.error_item = ""
                    st.session_state.input_item = ""

                    prompt = ""
                    for i in range(len(st.session_state.keywords)):

                        # prompts = {"middle": f'''{i  + 1}.Make up a sentence at elementary English level with the word "{st.session_state.keywords[i].lower()}". Add the context of {contexts[str(random.randint(0, 515))].lower()}. The sentence lenght must be up to 26 words. Do not change the initial form of "{st.session_state.keywords[i].lower()}".'''}
                        prompts = {"middle": f'''{i  + 1}. Word - {st.session_state.keywords[i].lower()}, context - {contexts[str(random.randint(0, 515))].lower()}.'''}
                        prompt += prompts[st.session_state.level]+"\n"

                    
                    # time.sleep(2)
                    st.session_state.data.append({"role": "user", "content": prompt})

                    try:
                        with st.spinner('Генерация упражнения...'):
                            url = "https://api.theb.ai/v1/chat/completions"
                            res = bot(st.session_state.data, url, st.session_state.acsses_key, 1)

                            response = res[0]
                            st.session_state.tokens = res[1]
                            st.session_state.data.append({"role": "assistant", "content": response})

                            list_of_sentences = response.split("\n")

                            for word in list_of_sentences:
                                if word == "":
                                    i = list_of_sentences.index(word)
                                    del list_of_sentences[i]

                            status = True
                            for i in range(len(st.session_state.keywords)):

                                item = st.session_state.keywords[i]
                                sentence = list_of_sentences[i]

                                st.session_state.unique_key += 1
                                st.session_state.responses.append(list_of_sentences[i])
                                st.session_state.formated_responses.append([word_formater(item, sentence)[0], word_formater(item, sentence)[2]])

                                if word_formater(item, sentence)[3]:
                                    pass
                                else:
                                    status = False

                            if status:
                                gens_number = int(data["gens_number"])
                                updated_value = gens_number - 1
                                database.update({"gens_number": updated_value}, acsses_key)

                                st.session_state.gens_number = updated_value

                            st.session_state.number_of_sentenses = len(st.session_state.responses)

                            random.shuffle(st.session_state.formated_responses)

                            st.session_state.show_submit_form = True
                    except:
                        try:
                            with st.spinner("Генерация упражнения..."):
                                url = "https://api.baizhi.ai/v1/chat/completions"
                                res = bot(st.session_state.data, url, st.session_state.acsses_key, 1)
                        
                                response = res[0]
                                st.session_state.tokens = res[1]
                                st.session_state.data.append({"role": "assistant", "content": response})

                                list_of_sentences = response.split("\n")

                                for word in list_of_sentences:
                                    if word == "":
                                        i = list_of_sentences.index(word)
                                        del list_of_sentences[i]

                                status = True
                                for i in range(len(st.session_state.keywords)):

                                    item = st.session_state.keywords[i]
                                    sentence = list_of_sentences[i]

                                    st.session_state.unique_key += 1
                                    st.session_state.responses.append(list_of_sentences[i])
                                    st.session_state.formated_responses.append([word_formater(item, sentence)[0], word_formater(item, sentence)[2]])

                                    if word_formater(item, sentence)[3]:
                                        pass
                                    else:
                                        status = False

                                if status:
                                    gens_number = int(data["gens_number"])
                                    updated_value = gens_number - 1
                                    database.update({"gens_number": updated_value}, acsses_key)

                                    st.session_state.gens_number = updated_value

                                st.session_state.number_of_sentenses = len(st.session_state.responses)

                                random.shuffle(st.session_state.formated_responses)

                                st.session_state.show_submit_form = True
                        except:
                            st.error("Соединение с сервером прервано, попробуйте создать задание еще раз.\n Если ошибка продолжает появляться, пожалуйста, обратитесь в тех. поддержку!", icon="💔")
                else:

                    if st.session_state.gens_number == 0:
                        st.warning("К сожалению, число генераций исчерпано, обратитесь к представителю LexisGen, чтобы пополнить его", icon="😔")
                    if len(st.session_state.keywords) < 2:
                        st.warning("  Пожалуйста, введите хотя бы 2 слова для генерации задания", icon="🙊")
                    if st.session_state.propriate_length == False:
                        st.warning(f'  "{st.session_state.error_item}" относится к категории словосочетаний, фраз или идиом. К сожалению, пока доступна генерация на основе только отдельных слов.', icon="⚠️")
                    if st.session_state.check_language == False:
                        st.info(f'  "{st.session_state.input_item}" не является словом, относящимся к Английскому языку', icon="🌐")
                    if st.session_state.propriate_spell == "impossible_word" and st.session_state.check_language:
                        st.warning(f'  Нейронная сеть не смогла догадаться, что Вы имели в виду под "{st.session_state.input_item}"...', icon="😢")
                    if st.session_state.propriate_spell == False:
                        st.warning(f'   Слова "{st.session_state.input_item}" не существует. Возможно, Вы имели в виду "{st.session_state.error_item}"?', icon="⚠️")
                    if st.session_state.not_in_sw == False:
                        st.warning(f'   Только "{st.session_state.error_item}" недостаточно для генерации полноценного предложения...', icon="😕")
            else:
                st.warning("Пожалуйста, введите ключ доступа", icon="🔑")

    if st.session_state.show_submit_form:
        st.info('Заполните пропуски в предложениях правильной формой слова из спика выше.')

        with st.form("my_form"):

            if len(st.session_state.answers) == 0:
                for answer in st.session_state.formated_responses:
                    st.session_state.answers.append(answer[1])

            
            for i in range(st.session_state.number_of_sentenses):
                try:
                    time.sleep(0.15)
                    st.session_state.user_answers[i] = input_field(st.session_state.formated_responses[i][0], key=st.session_state.unique_key + i)
                except:
                    pass

            if st.form_submit_button("Проверить"):
                try:
                    st.session_state.results = ""
                    for i in range(len(st.session_state.user_answers)):
                        if len(st.session_state.user_answers[i]) != 0:
                            if st.session_state.user_answers[i][0].lower() == st.session_state.answers[i].lower():
                                st.session_state.results += f" ✔️ :green[{st.session_state.answers[i].lower()}]"
                            elif len(st.session_state.user_answers[i][0].strip()) > 0:
                                st.session_state.results += f" ❌ :red[{st.session_state.user_answers[i][0].lower()}]"

                    st.write(st.session_state.results)
                except:
                    pass

        with st.expander("Ответы"):
            for i in range(st.session_state.number_of_sentenses):
                st.write(st.session_state.formated_responses[i][0].replace("[G_A_P]", f":blue[{st.session_state.answers[i]}]"))
        st.write(st.session_state.tokens)


main_grid.write("")

with st.sidebar:
    if st.session_state.key_is_provided:
        st.title(f"Осталось генераций: {st.session_state.gens_number}")


    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")


    st.link_button("⚡ Получить доступ", "https://vk.com/lexisgen",)
    st.link_button("🔗 Сообщество в ВК", "https://vk.com/lexisgen",)
    st.link_button("⚙️ Тех. поддержка &nbsp; &nbsp;", "https://vk.com/lostconcepts",)