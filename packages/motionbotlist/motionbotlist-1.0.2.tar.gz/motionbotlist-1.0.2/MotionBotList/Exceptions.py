
class IntError(Exception):
    def __init__(self, value):
        super().__init__("\"{}\" was not a interger".format(value))

class ConnectionError(Exception):
    def __init__(self):
        super().__init__("Connetion Timeout, failed to connect to website. Most likely the site is offline, try again later")

class ServerError(Exception):
    def __init__(self, value):
        super().__init__("{}".format(value))

class Unauthorized(Exception):
    def __init__(self):
        super().__init__("You did not pass in a vailid API key".format())

class Forbidden(Exception):
    def __init__(self):
        super().__init__("You do not have the permission to make that request".format())

class BotNotFound(Exception):
    def __init__(self, bot_id):
        super().__init__("The bot with \"{}\" was not found".format(bot_id))

