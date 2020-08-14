class AOPError:
    def __init__(self, user_message, encoded_message):
        self._user_message = user_message
        self._encoded_message = encoded_message

    @property
    def encoded_message(self):
        return self._encoded_message
    
    @property
    def user_message(self):
        return self._user_message

    @property
    def full_message(self):
        return self.user_message + "\n\n" + self.encoded_message
