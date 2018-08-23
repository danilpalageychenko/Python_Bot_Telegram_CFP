from subprocess import Popen, PIPE
from threading import Thread

import libkeepass
import os
from telegram import File, InlineKeyboardMarkup, InlineKeyboardButton

from dbmanagment import User, PassDB, IntegrityError
from config import PASS_DBS_FOLDER
from decorators import logged_in, add_to_queue
from variables import logging, logged_in_users, bot, last_functions


def start(bot, update):
    """
    Command: start
    """
    bot.send_message(chat_id=update.message.chat_id, text="Please enter your password")


def exit(bot, update):
    """
    Command: exit
    """
    logging.info("User logged out")
    bot.send_message(chat_id=update.message.chat_id, text="Bye Gaara631")
    logged_in_users.pop(logged_in_users.index(update.message.from_user.id))


def passwd(bot, update):
    """
    Type: Message
    """
    username = update.message.from_user.name
    logging.info("User %s logged in" % username)
    bot.send_message(chat_id=update.message.chat_id, text="Hi, %s" % username.replace("@", ""))
    try:
        User.create(username=username)
        logging.info("Entry for user %s created" % username)
    except IntegrityError:
        pass

    logged_in_users.append(update.message.from_user.name)


def allmessages(bot, update):
    if update.message.from_user.name not in logged_in_users:
        logging.info("User %s pass incorect password:\"%s\"" % (update.message.from_user.name, update.message.text))
        bot.send_message(chat_id=update.message.chat_id, text="Please enter your password")
    else:
        bot.send_message(chat_id=update.message.chat_id, text="Command \"%s\" does not exists" % update.message.text)


"""Command hadler"""


def run(command, real_time):
    global stop_all
    process = Popen(command, stderr=PIPE, stdout=PIPE, shell=True)
    if real_time:
        while not stop_all:
            line = process.stdout.readline().rstrip()
            if not line and process.stderr:
                line = process.stderr.readline().rstrip()

            if not line:
                break
            yield line
    else:
        stdout, stderr = process.communicate()
        yield stdout + stderr


def proc(update, command, real_time):
    for path in run(command, real_time):
        bot.send_message(chat_id=update.message.chat_id, text=path.decode("utf-8"))


@logged_in
def command(bot, update):
    """
    Command: command
    """
    command = update.message.text.replace('/command ', '').replace('/c ', '')
    logging.info("User %s run command \"%s\"" % (update.message.from_user.name, command))
    global stop_all
    if command == "stop":
        stop_all = True
    elif command == "unstop":
        stop_all = False
    else:
        if command.startswith("-"):
            real_time = True
            command = command[1:]
        else:
            real_time = False

        thr = Thread(target=proc, args=(update, command, real_time))
        thr.start()


@logged_in
def openkee(bot, update):
    """
    Command: add_db
    """
    last_command.append('/add_db')
    bot.send_message(chat_id=update.message.chat_id, text="Please send me .kdbx file")


@logged_in
def process_file(bot, update):
    """
    Wait for file after open
    """
    global last_command
    if last_command == '/add_db':
        last_command = ""
        if update.message.document.file_name.endswith(".kdbx"):
            username = update.message.from_user.name[1:]
            """Creating folder"""
            if not os.path.isfile(PASS_DBS_FOLDER + username):
                os.mkdir(PASS_DBS_FOLDER + username)

            """Downloading file"""
            file_id = update.message.document.file_id
            f = bot.get_file(file_id)
            f.download(PASS_DBS_FOLDER + username + '/' + file_id + '.kdbx')

            try:

                passdb = PassDB(real_filename="file", user=User.get(username=update.message.from_user.name), filename=PASS_DBS_FOLDER + username + '/' + file_id + '.kdbx')
                passdb.save()
                bot.send_message(chat_id=update.message.chat_id, text="File added to your library")
            except IntegrityError:
                bot.send_message(chat_id=update.message.chat_id, text="Database file already exist.")

        else:
            bot.send_message(chat_id=update.message.chat_id, text="Wrong filetype, try again")


@add_to_queue
@logged_in
def list_db(bot, update):
    """
    Command: list_db
    """
    dbs = PassDB.get_user_dbs(update.message.from_user.name)
    print(dbs)
    custom_inline_keyboard = []
    tmp_keyboard = []
    i = 0
    for i, db in enumerate(dbs):
        if i % 2 == 0:
            custom_inline_keyboard.append(tmp_keyboard)
            tmp_keyboard.clear()
        tmp_keyboard.append(InlineKeyboardButton(text=db.real_filename, callback_data=db.filename))
    else:
        if i and i % 2 != 0:
            custom_inline_keyboard.append(tmp_keyboard)

    inline_keyboard_markup = InlineKeyboardMarkup(custom_inline_keyboard)
    bot.send_message(chat_id=update.message.chat_id, text="Select db to open", reply_markup=inline_keyboard_markup)

@logged_in
def open_db(bot, update):
    #TODO last command var
    username = update.callback_query.from_user.name
    user = User.get(username=username)
    pass_db = PassDB.get(user=user)

    file_path = PASS_DBS_FOLDER + username + '/' + pass_db.filename

    if last_functions.get() == 'list_db':
        bot.send_message(chat_id=update.callback_query.message.chat_id, text="Please enter password")
    elif last_functions.get() == 'open_db':
        print("Password arived")
        last_command = ""
    else:
        print(last_command)
        print("No last command")


def test(bot, update):
    """
    Command: test
    """
    bot.send_message(chat_id=update.message.chat_id, text="This is private file")
