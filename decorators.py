from variables import logged_in_users, dispatcher, last_functions


def logged_in(func):
    def wrapper(bot, update):
        from functions import allmessages
        import logging
        if update.message.from_user.name in logged_in_users:
            return func(bot, update)
        else:
            logging.warning("User %s does not have permissions for function \"%s\"" % (update.message.from_user.name, func.__name__))
            dispatcher.run_async(allmessages, bot, update)

    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    return wrapper


def add_to_queue(func):
    def wrapper(bot, update):
        return func(bot, update)

    last_functions.put_nowait(func.__name__)
    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    return wrapper

