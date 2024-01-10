from telegram.ext import CommandHandler, MessageHandler, Filters, TypeHandler, InlineQueryHandler, CallbackQueryHandler

from Filters import pass_filter, DBPassFilter
from functions import start, exit, test, command, passwd, allmessages, openkee, process_file, list_db, open_db
from variables import dispatcher, updater

stop_all = False


"""Commands"""
start_handler = CommandHandler('start', start)
exit_handler = CommandHandler('exit', exit)
test_handler = CommandHandler('test', test)
command_handler = CommandHandler('command', command)
command_handler2 = CommandHandler('c', command)
adddb_handler = CommandHandler('add_db', openkee)
listdb_handler = CommandHandler('list_db', list_db)
"""Inlines"""
opendb_handler = CallbackQueryHandler(open_db,pattern=r"[a-z,A-Z,0-9]+.kdbx")
"""Filters"""
opendb_handler2 = MessageHandler(DBPassFilter('COMMAND'),open_db)

passwd_handler = MessageHandler(pass_filter, passwd)
keepassfile_handler = MessageHandler(Filters.document, process_file)
allmessage_handler = MessageHandler(Filters.all, allmessages)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(exit_handler)
dispatcher.add_handler(test_handler)
dispatcher.add_handler(passwd_handler)
dispatcher.add_handler(command_handler)
dispatcher.add_handler(command_handler2)
dispatcher.add_handler(adddb_handler)
dispatcher.add_handler(listdb_handler)
dispatcher.add_handler(keepassfile_handler)
dispatcher.add_handler(opendb_handler)
dispatcher.add_handler(opendb_handler2)
dispatcher.add_handler(allmessage_handler)

updater.start_polling()  # start bot
