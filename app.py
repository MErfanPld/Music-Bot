import telebot
import requests

token_bot = "6686435049:AAE7nmLFinVJYawoOsXQn7pc9Z_MeWVdAZA"
bot = telebot.TeleBot(token_bot)

url_api = "http://127.0.0.1:8000/music/"

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_chat_action(message.chat.id, action='typing')
    bot.send_message(message.chat.id, "به ربات تلگرامی اهنگی خوش امدید 👋​")
    bot.send_message(message.chat.id, "برای دیدن روش کار دستور '/help' وارد کنید 🛠️​​")

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_chat_action(message.chat.id, action='typing')
    bot.send_message(message.chat.id, "برای مشاهده لیست اهنگ ها : '/music' 🎙️")

@bot.message_handler(commands=['music'])
def music_list(message):
    bot.send_chat_action(message.chat.id, action='typing')

    headers = {
        "AUTHORIZATION":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk1MDI4NTg3LCJpYXQiOjE2OTQ5NDIxODcsImp0aSI6IjBlNTNlMjVlMzkyMzRhZjhhZmEwNWVlMDY2YzQwNzVjIiwidXNlcl9pZCI6NH0.AuX5MdmZlDIwFsE5QT6QGIpakWH3QCbsxaYnbXiH89w"
    }
    response = requests.request("GET", url_api, headers=headers)

    btn_items = []
    for item in response.json():
        btn_items.append(telebot.types.InlineKeyboardButton(str(item["title"]), url = str(item["audio_link"])))
    reply_markup=telebot.types.InlineKeyboardMarkup(build_menu(btn_items,n_cols=1))
    bot.send_message(message.chat.id, text='لطفا اهنگ مورد نظر خود را انتخاب کنید',reply_markup=reply_markup)


def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
  menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
  if header_buttons:
    menu.insert(0, header_buttons)
  if footer_buttons:
    menu.append(footer_buttons)
  return menu


bot.polling()