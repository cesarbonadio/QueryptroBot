# Se necesita importar primero el modulo telebot
# Luego crear el bot en @BotFather desde telegram
# E instalar pytelegrambot

#modulos
import telebot,datetime,requests,json
#modulos propios
import reference
#types 
from telebot import types
bot = telebot.TeleBot(reference.api_token)


@bot.message_handler(commands=['start','help'])
def send_welcome(message):
	#print message
	name = message.chat.first_name
	
	if hasattr(message.chat, 'last_name') and message.chat.last_name is not None:
		name += u" {}".format(message.chat.last_name)

	if hasattr(message.chat, 'username') and message.chat.username is not None:
		name += u" (@{})".format(message.chat.username)

	bot.reply_to(message, reference.text_messages['welcome'].format(name=name))	



# Para respoder sin reply ante un comando en especifico
@bot.message_handler(commands=['/source'])
def send_something(message):
	bot.send_message(message.chat.id, "Hi")


#el comando "bitcoin" default
@bot.message_handler(func=lambda m: m.text is not None and m.text == 'bitcoin')
def send_bitcoin(message):
	r = requests.get(reference.link+"?limit=1")
	json_data = json.loads(r.text)
	#print r.text
	price = json_data['data']['1']['quotes']['USD']['price']
	#print r.text
	print price
	#print r.status_code
	#print r.headers['content-type']
	bot.send_message(message.chat.id, "BTC: "+str(price)+" $")


#10 criptomonedas
@bot.message_handler(func=lambda m: m.text is not None and m.text == '10')
def top_cryptocurrency(message):
	
	#logs
	print message.text
	mes = str(message.text)
	print type(mes)
	print mes
	#

	r = requests.get(reference.link+"?limit=10")
	json_data = json.loads(r.text)
	#for i in range (1,10):
		#price = json_data['data'][str(i)]['quotes']['USD']['price']
		#name = json_data['data'][str(i)]['']
		#bot.send_message(message.chat.id, "BTC: "+str(price)+" $")

	for k,v in json_data['data'].items():
		price = v['quotes']['USD']['price']
		name = v['name']
		symbol = v['symbol']
		#print price
		bot.send_message(message.chat.id, str(name) + "(" + str(symbol) + ")" + ": " + str(price) + " $")



#Handler para el query Ln
@bot.message_handler(func=lambda m: m.text is not None and 'L' in m.text and str(m.text)[0]=='L')
def Ln_cryptocurrency(message):

	#logs
	print message.text
	mes = str(message.text)
	print type(mes)
	print mes
	#

	number_cryptocurrencies = 0
	d = 0
	for i in range (1,len(mes)):
		try:
			d = int(mes[i])
			number_cryptocurrencies = (number_cryptocurrencies*10)+d
		except ValueError as err:
			bot.send_message(message.chat.id, reference.text_messages['wrong_query'].format(query=mes))
			return	

	#logs
	print number_cryptocurrencies
	#

	r = requests.get(reference.link+"?limit=" + str(number_cryptocurrencies))
	json_data = json.loads(r.text)

	for k,v in json_data['data'].items():
		price = v['quotes']['USD']['price']
		name = v['name']
		symbol = v['symbol']
		#print price
		bot.send_message(message.chat.id, str(name) + "(" + str(symbol) + ")" + ": " + str(price) + " $")			





######handlers miscelaneos########

#log de mensaje
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

	print "Message from " + name + ": " + message.text
	bot.send_message(message.chat.id, "Thanks for your feedback! ")


#numero de criptomonedas
@bot.message_handler(commands=['num'])
def send_num(message):
	r = requests.get(reference.link+"?limit=1")
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


bot.polling(none_stop=True)