import telebot

text_messages = {
	'welcome':
		u'Please welcome {name}!\n\n\n'
		u'This bot chat is intended to query the price of cryptocurrencies.\n\n\n'
		u'Available commands: \n\n'
		u'/help or /start for welcome\n\n'
		u'/num to see the number of cryptocurrencies\n\n'
		u'/ping to see if you are connected to me\n\n'
		#u'/time to see the current time-zone\n\n'
		u'/value to start searching a specific coin\n\n'
		u'/file followed by coin name to generate a file with all coin data\n\n'
		u'/contact to send a short message to the bot creator\n\n'
		u'/global to see the summary of the currency market. Follow it by "f" if you want to generate file\n\n\n'
		u'How to query:\n\n'
		u'- Just type "Ln" and I will return n cryptocurrencies picked randomly (the limit is 100)\n\n'
		u'- If you want to know only the value of a specific currency send the command /value and then send the coin name.'
		u'You can find the price by name or symbol. Remember that if the original name consist in two words or more,'
		u'you'u"'" u'll need to put them all\n\n'
		u'- If you want to generate a file with all coin data send /file followed by the coin name\n\n'
		u'- If you want to know only the value of bitcoin send "bitcoin"\n\n'
		u'- If you want to know the value of the 10 most important crytocurrencies just send "10"\n\n',

	'wrong_query_l' :
		u' Wrong query "{query}", after the L you should type a number\n',

	'wrong_query_file':
		u' Wrong query, command /file should have at least one parameter\n',

	'wrong_query_global':
		u' Wrong query, command /global only accepts "f" as parameter\n',	

	'wrong_query_final':
		u'send /help and request some help'		 	  
}



link = "https://api.coinmarketcap.com/v2/"
