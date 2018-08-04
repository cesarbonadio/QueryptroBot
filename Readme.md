## QueryptroBot

Este bot de telegram te permite consultar el valor actual de las criptomonedas.

Necesita instalar el modulo de [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)


### Instalación de pyTelegramBotAPI

⋅⋅* Usando PIP:

```
$ pip install pyTelegramBotAPI

```

..* Usando el repositorio original (requiere git):

``` 
$ git clone https://github.com/eternnoir/pyTelegramBotAPI.git
$ cd pyTelegramBotAPI
$ python setup.py install

```

Se puede actualizar el módulo usando ` pip install pytelegrambotapi --upgrade `


### Api key

Para crear tu bot buscar en telegram el bot  ` @BotFather ` el cual te dará un token secreto.
Sustituir:

``` 
 bot = telebot.TeleBot(secret.api_token, threaded=False)

```

Por:

```
 bot = telebot.TeleBot("tokensecretoaqui", threaded=False)

```

Diseñado para uso personal. Deshabilitado el threading para evitar caida del polling
con los servidores de telegram.

Probado solo en python 2.7.15. Para correr: ` python bot.py `