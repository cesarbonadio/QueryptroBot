# Se necesita importar primero el modulo telebot
# Luego crear el bot en @BotFather desde telegram
# E instalar pytelegrambot
import telebot,datetime,requests,json
bot = telebot.TeleBot("645801202:AAG9BLwp7vbccfktvuL3volLA4C-nxpcamA")
link = "https://api.coinmarketcap.com/v2/ticker/"



text_messages = {
	'welcome':
		u'Please welcome {name}!\n\n'
		u'This bot chat is intended for queries about the price of cryptocurrencies.\n\n'
		u'Available commands: \n'
		u'/help or /start for welcome\n'
		u'/num to see the numbers of cryptocurrencies\n'
		u'/ping to see if you are connected to me\n'
		u'/time to see the current time\n\n'
		u'How to query:\n'
		u'ln will return n cryptocurrencies randomly\n' 
}





@bot.message_handler(commands=['start','help'])
def send_welcome(message):
	print message
	name = message.chat.first_name
	
	if hasattr(message.chat, 'last_name') and message.chat.last_name is not None:
		name += u" {}".format(message.chat.last_name)

	if hasattr(message.chat, 'username') and message.chat.username is not None:
		name += u" (@{})".format(message.chat.username)

	bot.reply_to(message, text_messages['welcome'].format(name=name))	

		


@bot.message_handler(commands=['query'])
def send_something(message):
	bot.send_message(message.chat.id, "Choose first limit:")
	bot.message_handler(func=lambda m: True)
	bot.send_message(message.chat.id, "Nice")


# Para respoder sin reply ante un comando en especifico
@bot.message_handler(commands=['prueba'])
def send_something(message):
	bot.send_message(message.chat.id, "Choose one letter:")



@bot.message_handler(func=lambda m: m.text is not None and m.text == 'hola')
def echo_all(message):
	bot.send_message(message.chat.id, "hola que tal")

@bot.message_handler(func=lambda m: m.text is not None and m.text == 'como estas')
def echo_all2(message):
	bot.send_message(message.chat.id, "bien y tu")

@bot.message_handler(func=lambda m: m.text is not None and m.text == 'chao')
def echo_saludo(message):
	bot.send_message(message.chat.id, "Adios")



@bot.message_handler(func=lambda m: m.text is not None and m.text == 'bitcoin')
def echo_bitcoin(message):
	r = requests.get(link+"?limit=1")
	json_data = json.loads(r.text)
	#print r.text
	price = json_data['data']['1']['quotes']['USD']['price']
	print r.text
	print price
	print r.status_code
	print r.headers['content-type']
	bot.send_message(message.chat.id, "BTC: "+str(price)+" $")


#'limit-' is in m.text m.text == '10')
@bot.message_handler(func=lambda m: m.text is not None and m.text == '10')
def echo_cryptocurrency(message):
	print message.text
	mes = str(message.text)
	print type(mes)
	print mes
	r = requests.get(link+"?limit=10")
	json_data = json.loads(r.text)
	#print r.text
	#for i in range (1,10):
		#price = json_data['data'][str(i)]['quotes']['USD']['price']
		#name = json_data['data'][str(i)]['']
		#bot.send_message(message.chat.id, "BTC: "+str(price)+" $")

	for k,v in json_data['data'].items():
		price = v['quotes']['USD']['price']
		name = v['name']
		symbol = v['symbol']
		print price
		bot.send_message(message.chat.id, str(name) + "(" + str(symbol) + ")" + ": " + str(price) + " $")



#'limit-' is in m.text m.text == '10')
@bot.message_handler(func=lambda m: m.text is not None and 'l' in m.text and str(m.text)[0]=='l')
def echo_cryptocurrency(message):
	print message.text
	mes = str(message.text)
	print type(mes)
	print mes

	number_cryptocurrencies = 0
	d = 0
	for i in range (1,len(mes)):
		d = int(mes[i])
		number_cryptocurrencies = (number_cryptocurrencies*10)+d

	
	print number_cryptocurrencies

	r = requests.get(link+"?limit=" + str(number_cryptocurrencies))
	json_data = json.loads(r.text)
	#print r.text
	#for i in range (1,10):
		#price = json_data['data'][str(i)]['quotes']['USD']['price']
		#name = json_data['data'][str(i)]['']
		#bot.send_message(message.chat.id, "BTC: "+str(price)+" $").	

	for k,v in json_data['data'].items():
		price = v['quotes']['USD']['price']
		name = v['name']
		symbol = v['symbol']
		print price
		bot.send_message(message.chat.id, str(name) + "(" + str(symbol) + ")" + ": " + str(price) + " $")			





#handlers miscelaneos
@bot.message_handler(commands=['num'])
def echo_num(message):
	r = requests.get(link+"?limit=1")
	json_data = json.loads(r.text)
	q = json_data['metadata']['num_cryptocurrencies']
	bot.send_message(message.chat.id, " Current Number of"\
	   +" Cryptocurrencies in the market: "\
	   +str(q))

@bot.message_handler(commands=['time'])
def echo_all(message):
	bot.send_message(message.chat.id, "Current time:" + str(datetime.datetime.now()))


@bot.message_handler(commands=["ping"])
def on_ping(message):
	bot.reply_to(message, "I'm still alive")


bot.polling(none_stop=True)