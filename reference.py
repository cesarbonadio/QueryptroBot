import telebot

text_messages = {
	'welcome':
		u'Please welcome {name}!\n\n'
		u'This bot chat is intended for queries about the price of cryptocurrencies.\n\n'
		u'Available commands: \n'
		u'/help or /start for welcome\n'
		u'/num to see the numbers of cryptocurrencies\n'
		u'/ping to see if you are connected to me\n'
		u'/time to see the current time-zone\n'
		u'/value for start searching a specific coin\n'
		u'/contact to send a short message to the bot creator\n\n'
		u'How to query:\n'
		u'* Just type "Ln" and I will return n cryptocurrencies picked randomly (the limit is 100)\n'
		u'* If you want to know only the value of a specific currency send the name after /value command\n'
		u'* If you want to know only the value of bitcoin send "bitcoin"\n'
		u'* If you want to know the value of the 10 most important crytocurrencies just send "10"\n',

	'wrong_query' :
		u' Wrong query "{query}"\n'
		u'send /help and request some help' 	  
}


api_token = "645801202:AAG9BLwp7vbccfktvuL3volLA4C-nxpcamA"
link = "https://api.coinmarketcap.com/v2/ticker/"