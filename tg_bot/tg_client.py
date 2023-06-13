import telebot
import logging
from telebot import types
import constants

tb = telebot.TeleBot(constants.TOKEN)

def run():
    telebot.logger.setLevel(logging.DEBUG) 
    tb.infinity_polling()

@tb.message_handler(commands=['start'])
def start(msg: types.Message):
    tb.send_message(msg.from_user.id, "дайте файл")


@tb.message_handler(commands=['check'])
def check(msg: types.Message):
    tb.send_message(msg.from_user.id, "пока не готово")


"""
Save files
TODO: Send data to S3 Server
["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact",
"new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo",
"group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
"migrate_from_chat_id", "pinned_message"]
==> "audio", "document", "photo", "video", "voice"
"""

@tb.message_handler(content_types=["audio", "document", "photo", "video", "voice"])
def handle_document(message : types.Message):
    try:
        doc_id = message.document.file_id
        doc_file = tb.get_file(doc_id)
        doc_bytes = tb.download_file(doc_file.file_path)
        with open('data/'+message.document.file_id+'_'+message.document.file_name, 'wb') as f:
            f.write(doc_bytes)
        tb.reply_to(message, 'Файл успешно загружен!\nНо пока бот не работает с документами')
    except Exception as er:
        tb.reply_to(message, er)
