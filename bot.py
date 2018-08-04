#modulos
import telebot,datetime,requests,json,os
from datetime import datetime
#modulos propios
import reference,util,secret
#types 
from telebot import types
import schedule,time


#Bot
bot = telebot.TeleBot(secret.api_token, threaded=False)



#No handler
def find_by_name(name_currency,chat_id):
    try:
        r = requests.get(reference.link+"listings")
        json_data = json.loads(r.text)

        for i in range (len(json_data['data'])):
            if json_data['data'][i]['name'].lower() == name_currency.lower() or \
            json_data['data'][i]['symbol'].lower() == name_currency.lower() or \
            json_data['data'][i]['website_slug'].lower() == name_currency.lower():
                coin_id = int(json_data['data'][i]['id'])
                break
            if i == len(json_data['data']) - 1:
                raise Exception('error')    
            
        r2 = requests.get(reference.link+"/ticker/"+str(coin_id))
        json_data2 = json.loads(r2.text) 
        return json_data2['data']       

    except Exception:
        bot.send_message(chat_id, 'I could not find any currency called "' + name_currency + '"')
        return





#Handler bienvenida
@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    name = message.chat.first_name
    
    if hasattr(message.chat, 'last_name') and message.chat.last_name is not None:
        name += u" {}".format(message.chat.last_name)

    if hasattr(message.chat, 'username') and message.chat.username is not None:
        name += u" (@{})".format(message.chat.username)

    bot.reply_to(message, reference.text_messages['welcome'].format(name=name)) 




#Handler bitcoin solo
@bot.message_handler(func=lambda m: m.text is not None and m.text == 'bitcoin')
def send_bitcoin(message):
    r = requests.get(reference.link+"ticker/?limit=1")
    json_data = json.loads(r.text)
    price = json_data['data']['1']['quotes']['USD']['price']
    print (r.status_code)
    print (r.headers['content-type'])
    bot.send_message(message.chat.id, "BTC: "+str(price)+" $")  




#Handler de criptomonedas por nombre
@bot.message_handler(commands=['value'])
def value(message):
    markup = types.ForceReply(selective=False)
    msg = bot.send_message(message.chat.id, "Ok, send the name of the cryptocurrency", reply_markup=markup)
    bot.register_next_step_handler(msg, search_cryptocurrency)

def search_cryptocurrency(message):
    v = find_by_name(message.text,str(message.chat.id))
    if v:
        price = v['quotes']['USD']['price']
        bot.send_message(message.chat.id, str(v['name']) + "(" + str(v['symbol']) + ")" + ": " + str(v['quotes']['USD']['price']) + " $")              





#Handler para el query Ln
@bot.message_handler(func=lambda m: m.text is not None and 'L' in m.text and str(m.text)[0]=='L')
def Ln_cryptocurrency(message):

    mes = str(message.text)
    number_cryptocurrencies = 0
    d = 0
    for i in range (1,len(mes)):
        try:
            d = int(mes[i])
            number_cryptocurrencies = (number_cryptocurrencies*10)+d
        except ValueError as err:
            bot.send_message(message.chat.id, reference.text_messages['wrong_query_l'].format(query=mes)\
                                            + reference.text_messages['wrong_query_final'])
            return  

    r = requests.get(reference.link+"ticker/?limit=" + str(number_cryptocurrencies))
    json_data = json.loads(r.text)

    for k,v in json_data['data'].items():
        price = v['quotes']['USD']['price']
        name = v['name']
        symbol = v['symbol']
        bot.send_message(message.chat.id, str(name) + "(" + str(symbol) + ")" + ": " + str(price) + " $")           





#Handler para el top 10 de criptomonedas
@bot.message_handler(func=lambda m: m.text is not None and m.text == '10')
def top_cryptocurrency(message):
    mes = str(message.text)
    r = requests.get(reference.link+"ticker/?limit=10")
    json_data = json.loads(r.text)

    for k,v in json_data['data'].items():
        price = v['quotes']['USD']['price']
        name = v['name']
        symbol = v['symbol']
        bot.send_message(message.chat.id, str(name) + "(" + str(symbol) + ")" + ": " + str(price) + " $")





#Handler para generar el archivo
@bot.message_handler(commands=['file'])
def generate_file(message):
    status = util.extract_arg(message.text)

    if len(status)==0:
        bot.send_message(message.chat.id, reference.text_messages['wrong_query_file']\
                                         +reference.text_messages['wrong_query_final'])
        return

    currency_name = util.concat_arg(status)
    v = find_by_name(str(currency_name),str(message.chat.id))

    if v:
        doc = open(str(v['name']) + '.txt', 'w+')

        coin_data = 'Name: ' + v['name'] + '\n' + \
                    'Symbol: ' + v['symbol'] + '\n' + \
                    'Global rank: '+ str(v['rank']) + '\n' + \
                    'Circulating supply: ' + str(v['circulating_supply']) + '\n' + \
                    'Total supply: '  + str(v['total_supply']) + '\n' + \
                    'Max supply: ' + str(v['max_supply']) + '\n\n' + \
                    'Price \n\n' + \
                    'Price now: ' + str(v['quotes']['USD']['price']) + '$' + '\n' + \
                    'Volume 24h: ' + str(v['quotes']['USD']['volume_24h']) + '\n' + \
                    'Market capital: ' + str(v['quotes']['USD']['market_cap']) + '\n' + \
                    'Percent change 1h: ' + str(v['quotes']['USD']['percent_change_1h']) + '\n' + \
                    'Percent change 24h: ' + str(v['quotes']['USD']['percent_change_24h']) + '\n' + \
                    'Percent change 7d: ' + str(v['quotes']['USD']['percent_change_24h']) + '\n' 

        doc.write(coin_data)
        doc.close
        doc = open(str(v['name']) + '.txt' , 'rb')
        bot.send_document(message.chat.id, doc)
        os.remove(str(v['name']) + '.txt')

    




######handlers miscelaneos########
# Para respoder sin reply ante un comando en especifico
@bot.message_handler(commands=['global'])
def find_global(message):
    status = util.extract_arg(message.text)

    r = requests.get(reference.link + "global")
    json_data = json.loads(r.text)
    last_update = datetime.fromtimestamp(int(json_data['data']['last_updated'])).strftime("%A, %B %d, %Y %I:%M:%S")

    
    global_stats = 'Cryptocurrencies: ' + str(json_data['data']['active_cryptocurrencies'])+\
                   '\nActive markets: ' + str(json_data['data']['active_markets'])+\
                   '\nBitcoin market percentaje: ' + str(json_data['data']['bitcoin_percentage_of_market_cap'])+ \
                   '\nMarket capital: ' + str(int(float(json_data['data']['quotes']['USD']['total_market_cap'])))+\
                   '\nVolume 24h: ' + str(json_data['data']['quotes']['USD']['total_volume_24h'])+\
                   '\n\nLast update: ' + str(last_update)               

    if len(status)==0:
        bot.send_message(message.chat.id, global_stats)
    elif status[0] == 'f':
        doc = open('global.txt','w+')
        doc.write(str(global_stats))
        doc.close
        doc = open('global.txt','rb')
        bot.send_document(message.chat.id, doc)
        os.remove('global.txt')
    else:
        bot.send_message(message.chat.id, reference.text_messages['wrong_query_global'] + reference.text_messages['wrong_query_final'])                          
 


#test
@bot.message_handler(commands=['test'])
def send_all(message):            
    pass




#Handler para enviar algun comentario
@bot.message_handler(commands=['contact'])
def contact(message):
    markup = types.ForceReply(selective=False)
    msg = bot.send_message(message.chat.id, "Ok, send your message", reply_markup=markup)
    bot.register_next_step_handler(msg, send_admin)



def send_admin(message):
    name = message.chat.first_name
    if hasattr(message.chat, 'last_name') and message.chat.last_name is not None:
        name += u" {}".format(message.chat.last_name)

    if hasattr(message.chat, 'username') and message.chat.username is not None:
        name += u" (@{})".format(message.chat.username)

    print("Message from " + name + ": " + message.text)
    doc = open('comments.txt','a+')
    doc.write('Message from ' + name + ': ' + message.text + '\n')
    doc.close
    bot.send_message(message.chat.id, "Thanks for your feedback!")


#numero de criptomonedas
@bot.message_handler(commands=['num'])
def send_num(message):
    r = requests.get(reference.link+"ticker/?limit=1")
    json_data = json.loads(r.text)
    q = json_data['metadata']['num_cryptocurrencies']
    bot.send_message(message.chat.id, " Current Number of"\
       +" Cryptocurrencies in the market: "\
       +str(q))

#hora
@bot.message_handler(commands=['time'])
def send_time(message):
    bot.send_message(message.chat.id, "Current time:" + str(datetime.datetime.now()))

#ping
@bot.message_handler(commands=["ping"])
def on_ping(message):
    bot.reply_to(message, "I'm still alive")






#Polling
def principal():
    while True:
        try:
            bot.infinity_polling(True)
            bot.polling(none_stop=True)
        except:
            time.sleep(10)

principal()

schedule.every(10).minutes.do(principal)
while True:
        schedule.run_pending()
        time.sleep(1)        
#bot.polling(none_stop=True)