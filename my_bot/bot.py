import telebot
import my_bot.config as config
import my_bot.wallet as ton
from telebot import types
import asyncio
import random

bot = telebot.TeleBot(config.TOKEN)

bot.set_my_commands(
   commands=[
      telebot.types.BotCommand('/start', 'description for name1'),
      telebot.types.BotCommand('/help', 'description for name2'),
      telebot.types.BotCommand('/getnft', 'description for name3')
   ],
)


account_to_transfer = ''


@bot.message_handler(commands=['start'])
def welcome(message):
    # Keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Home")
    item2 = types.KeyboardButton("Get NFT")

    markup.add(item1, item2)

    bot.send_message(message.chat.id, "Welcome {0.first_name}!\n  I'm NFT project named - <b> {1.first_name} </b> Here "
                                      "you can get your free NFT token!".format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['help'])
def help_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            'Message the developer', url='telegram.me/artiomtb'
        )
    )
    bot.send_message(
        message.chat.id,
        '1) To receive a list of available currencies press /exchange.\n' +
        '2) Click on the currency you are interested in.\n' +
        '3) You will receive a message containing information regarding the source and the target currencies, ' +
        'buying rates and selling rates.\n' +
        '4) Click “Update” to receive the current information regarding the request. ' +
        'The bot will also show the difference between the previous and the current exchange rates.\n' +
        '5) The bot supports inline. Type @<botusername> in any chat and the first letters of a currency.',
        reply_markup=keyboard
    )


@bot.message_handler(content_types=['text'])
def get_user_wallet(message):
    if message.chat.type == 'private':
        if message.text == 'Get NFT':
            msg = bot.send_message(message.from_user.id, 'Enter Wallet address:')
            bot.register_next_step_handler(msg, check_user_wallet)
        if message.text == 'Home':
            bot.send_message(message.chat.id,
                             "Welcome {0.first_name}!\n  I'm NFT project named - <b> {1.first_name} </b> Here "
                             "you can get your free NFT token!".format(message.from_user, bot.get_me()),
                             parse_mode='html')

        # elif message.text == 'Home':
        #     bot.send_message(message.chat.id, 'Hello world')


def check_user_wallet(message):
    account_to_transfer = message.text
    bot.send_message(message.chat.id, message.text)

    markup = types.InlineKeyboardMarkup(row_width=2)

    item1 = types.InlineKeyboardButton("Correct", callback_data='correct')
    item2 = types.InlineKeyboardButton("Incorrect", callback_data='incorrect')

    markup.add(item1, item2)

    bot.send_message(message.from_user.id, 'Check you wallet number!', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'correct':
                bot.send_message(call.message.chat.id, 'Nice sending NFT')
                return asyncio.run(ton.send_nft(account_to_transfer))
            elif call.data == 'incorrect':
                bot.send_message(call.message.chat.id, 'Retype your wallet number')
                msg = bot.send_message(call.message.chat.id, 'Enter Wallet address:')
                bot.register_next_step_handler(msg, check_user_wallet)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Check you wallet number!",
                                  reply_markup=None)

    except Exception as e:
        print(repr(e))

# asyncio.get_event_loop().run_until_complete(ton.send_nft(account_to_transfer))


# async def send_users_wallet(call):
#     try:
#         return run(ton.wallet.transfer(account_to_transfer, ton.client.to_nano(0.1), comment='test'))
#         bot.send_message(call.message.chat.id, 'Finished!')
#     except Exception as e:
#         print(repr(e))

bot.polling()