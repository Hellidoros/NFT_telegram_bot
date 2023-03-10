import stat

import my_bot.config as config
import my_bot.wallet as ton
from telebot import types
import asyncio
import random

# Logging module
import logging

# Aiogram imports
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


class DataInput(StatesGroup):
    firstState = State()
    secondState = State()
    WalletState = State()
    PayState = State()


# commands_set_bool = await bot.set_my_commands(
#     commands=[
#         BotCommand('/start', 'description for name1'),
#         BotCommand('/help', 'description for name2'),
#         BotCommand('/getnft', 'description for name3')
#     ],
# )


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    # Keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Home")
    item2 = types.KeyboardButton("Get NFT")

    markup.add(item1, item2)

    await message.answer("Welcome {0.first_name}!\n  I'm NFT project named - <b> {1.first_name} </b> Here "
                         "you can get your free NFT token!".format(message.from_user, await bot.get_me()),
                         reply_markup=markup,
                         parse_mode=ParseMode.HTML)
    await DataInput.firstState.set()


@dp.message_handler(commands=['help'], state='*')
async def help_command(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton('Message the developer', url='telegram.me/artiomtb')
    )
    await message.answer(
        '1) To receive a list of available currencies press /exchange.\n' +
        '2) Click on the currency you are interested in.\n' +
        '3) You will receive a message containing information regarding the source and the target currencies, ' +
        'buying rates and selling rates.\n' +
        '4) Click ???Update??? to receive the current information regarding the request. ' +
        'The bot will also show the difference between the previous and the current exchange rates.\n' +
        '5) The bot supports inline. Type in any chat and the first letters of a currency.',
        reply_markup=keyboard, parse_mode=ParseMode.HTML
    )


@dp.message_handler(commands=['cancel'], state="*")
async def cmd_cancel(message: types.Message):
    await message.answer("Canceled")
    await message.answer("/start to restart")
    await DataInput.firstState.set()


@dp.message_handler(commands=['getnft'], content_types='text', state=DataInput.firstState)
async def return_home(message: types.Message, state: FSMContext):
    await DataInput.secondState.set()
    await message.answer('Enter Wallet address:')
    if message.text == 'Get NFT':
        await DataInput.secondState.set()
        await message.answer('Enter Wallet address:')


@dp.message_handler(state=DataInput.secondState)
async def check_user_wallet(message: types.Message, state: FSMContext):
    if len(message.text) == 48:
        ton.account_to_send = message.text
        markup = InlineKeyboardMarkup(row_width=2)

        item1 = InlineKeyboardButton("Correct", callback_data='correct')
        item2 = InlineKeyboardButton("Incorrect", callback_data='incorrect')

        markup.add(item1, item2)

        await message.reply('Check you wallet number!', reply_markup=markup)
    else:
        await message.answer("Wrong wallet address")
        await DataInput.firstState.set()


@dp.callback_query_handler(lambda call: True, state="*")
async def send_nft(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'correct':
        await call.answer('Nice sending NFT')
        await call.message.answer('Nice sending NFT')
        await ton.send_nft_async(ton.account_to_send)


# @dp.callback_query_handler(func=lambda call: True)
# async def callback_inline(call: types.callback_query):
#     try:
#         if call.message:
#             if call.data == 'correct':
#                 await message.answer(call.message.chat.id, 'Nice sending NFT')
#                 return asyncio.run(ton.send_nft_async(account_to_transfer))
#             elif call.data == 'incorrect':
#                 await message.answer(call.message.chat.id, 'Retype your wallet number')
#                 msg = bot.send_message(call.message.chat.id, 'Enter Wallet address:')
#                 bot.register_next_step_handler(msg, check_user_wallet)
#             bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                   text="Check you wallet number!",
#                                   reply_markup=None)
#
#     except Exception as e:
#         print(repr(e))


# asyncio.get_event_loop().run_until_complete(ton.send_nft(account_to_transfer))


# async def send_users_wallet(call):
#     try:
#         return run(ton.wallet.transfer(account_to_transfer, ton.client.to_nano(0.1), comment='test'))
#         bot.send_message(call.message.chat.id, 'Finished!')
#     except Exception as e:
#         print(repr(e))

if __name__ == '__main__':
    # Create Aiogram executor for our bot
    executor.start_polling(dp, skip_updates=True)

    # Launch the deposit waiter with our executor
