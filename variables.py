from queue import Queue

import telegram
from telegram.ext import Updater
import logging

from config import BOT_TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
bot = telegram.Bot(token=BOT_TOKEN)  # bot object
updater = Updater(token=BOT_TOKEN)  # updater object
dispatcher = updater.dispatcher  # dispatcher object
logged_in_users = ['@Gaara631', ]


last_functions = list()
