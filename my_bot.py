# encoding: utf-8
import telebot
import conf
import urllib.request
import re
#import flask


#WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
#WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN) 
#bot.remove_webhook()

#bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

#app = flask.Flask(__name__)


@bot.message_handler(commands=['start', 'help'])
def choose_corpora(message):
    bot.send_message(message.chat.id, "Здравствуйте! Это бот, который осуществляет поиск в историческом древнерусском подкорпусе НКРЯ. \nВведите 1, если вы хотите найти точную словоформу. \nВведите 2, если вы хотите выбрать грамматические признаки леммы.")

    
@bot.message_handler(regexp="1")
def certain_form(message):
    bot.send_message(message.chat.id, "Отлично. Теперь введите 'поиск ' и точную словоформу, которую нужно найти в корпусе.")


@bot.message_handler(regexp='(п|П)оиск*')
def search_certain_form(message):
    user_word = message.text.split(' ')
    word0 = user_word[1]
    word = urllib.parse.quote(word0, safe = '')
    search_link = 'http://search.ruscorpora.ru/search.xml?mode=old_rus&text=lexgramm&sort=gr_created&lang=ru&doc_docid=1%7C16%7C7%7C4%7C2%7C5%7C3%7C6%7C10%7C11%7C13%7C0%7C15%7C8%7C14%7C12%7C9&f=fi&formi1=' + word 
    req = urllib.request.Request(search_link)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('windows-1251')
        html.encode('utf-8')

    regCorpDoc = re.compile('explain=".*?">.*?<span class="on', flags=re.U | re.DOTALL)
    database = regCorpDoc.findall(html)
    dtbs = database[:30]
    data = ''
    for element in dtbs:
        data +=element + ' '

    regTitle = re.compile('explain="[0-9]*">(.*?)<span class="on', flags=re.U | re.DOTALL)
    
    titles = regTitle.findall(data)
    for tit in titles:
        tit_new = "\n Источник: " + tit + "\n"
        data = re.sub(tit, tit_new, data)

    regNewLine = re.compile('explain="%.*?">(.*?)<span class="doc">', flags=re.U | re.DOTALL)
    new_lines = regNewLine.findall(data)
    for nl in new_lines:
        nl_new = nl + "\n"
        data = re.sub(nl, nl_new, data)
    regCorpText = re.compile('explain=".*?">(.*?)<span class=', flags=re.U | re.DOTALL)
    documents = regCorpText.findall(data)
    all_results = ''
           
    for words in documents:
        w = ''
        w += words   
        w_space = w.replace ("  ", " ")
        w0 = w_space.replace("</span>", "")
        w1 = w0.replace("&#1121;", "ѡ")
        w2 = w1.replace("&#1123;", "ѣ")
        w3 = w2.replace("&#1125;", "ѥ")
        w4 = w3.replace("&#1127;", "ѧ")
        w5 = w4.replace("&#1145;", "ѹ")
        w6 = w5.replace("&#1147;", "ѻ") 
        w7 = w6.replace("&#1151;", "ѿ")
        w8 = w7.replace("&#1155;", "҃")
        w9 = w8.replace("&#1231;", "ӏ")
        w10 = w9.replace("&#903;", "·")
        w11 = w10.replace("&#42571;", "ꙋ‎")
        w12 = w11.replace("&#8729;", "∙")
        w13 = w12.replace("&#785;", "̑")
        w14 = w13.replace("&#42577;", "ꙑ")
        w15 = w14.replace("&lt;", "<")
        w16 = w15.replace("&gt;", ">")
        w17 = w16.replace("&#949", "ε")
        w18 = w17.replace("&#8280;", "⁘")
        w19 = w18.replace("&#729;", "˙")
        w20 = w19.replace("&#773;", "̅")
        w21 = w20.replace("&#42729;", "ꛩ")
        w22 = w21.replace("&#42582;", "Ꙗ‎")
        w23 = w22.replace("&#1137;", "ѱ")
        w24 = w23.replace("&#1154", "҂")
        w25 = w24.replace("&#769", "́")
        w26 = w25.replace("&#42583;", "ꙗ")
        w27 = w26.replace("&#61759;", "")
        w28 = w27.replace("&#1120;", "Ѡ")
        w29 = w28.replace("&#1135;", "ѯ")
        w30 = w29.replace("&#1134:", "Ѯ")
        w31 = w30.replace("&#1139;", "ѳ‎")
        w32 = w31.replace("&#1138;", "‎Ѳ")
        w33 = w32.replace("&#768;", "̀")
        w34 = w33.replace("&#830;", "̾")
        w35 = w34.replace("&#1144;", "Ѹ")
        w36 = w35.replace("&#775;", "•")
        w37 = w36.replace("&#180;", "´")
        w38 = w37.replace("&#8258;", "⁂")
        all_results += w38
    all_results += '\n'
    if all_results == '\n':
        bot.send_message (message.chat.id, 'К сожалению, ничего найти не удалось. Попробуйте изменить запрос и убедитесь, что используете древнерусскую орфографию.')
    else:
        array = all_results.split('\n')
        final_array = array[:30]
        lines = ''
        for f in final_array:
            lines += f + '\n'
        bot.send_message(message.chat.id, 'Результат поиска:\n' + lines)
    

@bot.message_handler(regexp='2')
def word_gram(message):
    bot.send_message(message.chat.id, "Очень хорошо! Теперь введите 'грам ', лемму и грамматические признаки через пробел. Если признаки не нужны, введите 0. Если вам необходима подсказка, введите '/gramhelp'")


@bot.message_handler(commands=['gramhelp'])
def gram_helper (message):
    bot.send_message(message.chat.id, "__ Падежи: __\n nom - именительный\n voc - звательный\n acc - винительный\n gen - родительный\n dat - дательный\n ins - творительный\n loc - местный\n\
__ Род: __\n m - мужской\n f - женский\n n - средний\n\
__ Число: __\n sg - единственное\n du - двойственное\n pl - множественное\n adnum - счётная форма\n\
__ Наклонение: __\n imper - повелительное\n cond - сослагательное\n\
__ Время: __\n praes - настоящее\n nonpast - настоящее-будущее\n fut - будущее\n iperf - имперфект\n aor - аорист\n perf - перфект\n pqperf- плюсквамперфект\n past - прошедшее (прич)\n\
__ Лицо: __\n 1p - 1 лицо\n 2p - 2 лицо\n 3p - 3 лицо")


@bot.message_handler(regexp='(Г|г)рам*')
def search_word_gram(message):
    user_word = message.text.split(' ')
    word0 = user_word[1]
    word = urllib.parse.quote(word0, safe = '')
    
    if user_word[2] == '0':
        search_link = 'http://search.ruscorpora.ru/search.xml?mode=old_rus&text=lexgramm&sort=gr_created&lang=ru&doc_docid=1%7C16%7C7%7C4%7C2%7C5%7C3%7C6%7C10%7C11%7C13%7C0%7C15%7C8%7C14%7C12%7C9&parent1=0&level1=0&lexi1=' + word + '&parent2=0&level2=0&min1=1&max1=1'
    else:
        attributes = user_word[2]
        gram_attributes = user_word[3:]
        for att in gram_attributes:
            attributes += '%2C' + att
        search_link = 'http://search.ruscorpora.ru/search.xml?mode=old_rus&text=lexgramm&sort=gr_created&lang=ru&doc_docid=1%7C16%7C7%7C4%7C2%7C5%7C3%7C6%7C10%7C11%7C13%7C0%7C15%7C8%7C14%7C12%7C9&parent1=0&level1=0&lexi1=' + word +'&gramm1=' + attributes + '&parent2=0&level2=0&min1=1&max1=1'

    
    req = urllib.request.Request(search_link)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('windows-1251')
        html.encode('utf-8')

    regCorpDoc = re.compile('explain=".*?">.*?<span class="on', flags=re.U | re.DOTALL)
    database = regCorpDoc.findall(html)
    dtbs = database[:30]
    data = ''
    for element in dtbs:
        data +=element + ' '

    regTitle = re.compile('explain="[0-9]*">(.*?)<span class="on', flags=re.U | re.DOTALL)
    
    titles = regTitle.findall(data)
    for tit in titles:
        tit_new = "\n Источник: " + tit + "\n"
        data = re.sub(tit, tit_new, data)

    regNewLine = re.compile('explain="%.*?">(.*?)<span class="doc">', flags=re.U | re.DOTALL)
    new_lines = regNewLine.findall(data)
    for nl in new_lines:
        nl_new = nl + "\n"
        data = re.sub(nl, nl_new, data)
    regCorpText = re.compile('explain=".*?">(.*?)<span class=', flags=re.U | re.DOTALL)
    documents = regCorpText.findall(data)
    all_results = ''
           
    for words in documents:
        w = ''
        w += words   
        w_space = w.replace ("  ", " ")
        w0 = w_space.replace("</span>", "")
        w1 = w0.replace("&#1121;", "ѡ")
        w2 = w1.replace("&#1123;", "ѣ")
        w3 = w2.replace("&#1125;", "ѥ")
        w4 = w3.replace("&#1127;", "ѧ")
        w5 = w4.replace("&#1145;", "ѹ")
        w6 = w5.replace("&#1147;", "ѻ") 
        w7 = w6.replace("&#1151;", "ѿ")
        w8 = w7.replace("&#1155;", "҃")
        w9 = w8.replace("&#1231;", "ӏ")
        w10 = w9.replace("&#903;", "·")
        w11 = w10.replace("&#42571;", "ꙋ‎")
        w12 = w11.replace("&#8729;", "∙")
        w13 = w12.replace("&#785;", "̑")
        w14 = w13.replace("&#42577;", "ꙑ")
        w15 = w14.replace("&lt;", "<")
        w16 = w15.replace("&gt;", ">")
        w17 = w16.replace("&#949", "ε")
        w18 = w17.replace("&#8280;", "⁘")
        w19 = w18.replace("&#729;", "˙")
        w20 = w19.replace("&#773;", "̅")
        w21 = w20.replace("&#42729;", "ꛩ")
        w22 = w21.replace("&#42582;", "Ꙗ‎")
        w23 = w22.replace("&#1137;", "ѱ")
        w24 = w23.replace("&#1154", "҂")
        w25 = w24.replace("&#769", "́")
        w26 = w25.replace("&#42583;", "ꙗ")
        w27 = w26.replace("&#61759;", "")
        w28 = w27.replace("&#1120;", "Ѡ")
        w29 = w28.replace("&#1135;", "ѯ")
        w30 = w29.replace("&#1134:", "Ѯ")
        w31 = w30.replace("&#1139;", "ѳ‎")
        w32 = w31.replace("&#1138;", "‎Ѳ")
        w33 = w32.replace("&#768;", "̀")
        w34 = w33.replace("&#830;", "̾")
        w35 = w34.replace("&#1144;", "Ѹ")
        w36 = w35.replace("&#775;", "•")
        w37 = w36.replace("&#180;", "´")
        w38 = w37.replace("&#8258;", "⁂")
        all_results += w38
        
    all_results += '\n'
    if all_results == '\n':
        bot.send_message (message.chat.id, 'К сожалению, ничего найти не удалось. Попробуйте изменить запрос и убедитесь, что используете древнерусскую орфографию.')
    else:
        array = all_results.split('\n')
        final_array = array[:30]
        lines = ''
        for f in final_array:
            lines += f + '\n'
        bot.send_message(message.chat.id, 'Результат поиска:\n' + lines)

    
@bot.message_handler(content_types=['text'])
def random_text(message):
    bot.send_message(message.chat.id, "Кажется, то, что вы написали, не является поисковым запросом.\nВведите 1, если вы хотите найти точную словоформу.\nВведите 2, если вы хотите выбрать грамматические признаки леммы. ")
    
#@app.route('/', methods=['GET', 'HEAD'])
#def index():
#    return 'ok'

#@app.route(WEBHOOK_URL_PATH, methods=['POST'])
#def webhook():
#    if flask.request.headers.get('content-type') == 'application/json':
#        json_string = flask.request.get_data().decode('utf-8')
#        update = telebot.types.Update.de_json(json_string)
#        bot.process_new_updates([update])
#        return ''
#    else:
#        flask.abort(403)

if __name__ == '__main__':
    bot.polling(none_stop=True)
    
#if __name__ == '__main__':
#    import os
#    app.debug = True
#    port = int(os.environ.get("PORT", 5000))
#    app.run(host='0.0.0.0', port=port)
