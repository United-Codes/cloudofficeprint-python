class AOPError(Exception):
    """# TODO: document
    """
    def __init__(self, full_message):
        (self._user_message,
         self._contact_support_message,
         self._encoded_message) = self._split_message(full_message)
        super().__init__(self._user_message)

    @staticmethod
    def _split_message(message):
        separated = message.split("\n")
        user_message = "\n".join(separated[:-2]) # everything before the last 2 lines are considered user message
        contact_support_message = separated[-2] # second to last line contains the separated message
        encoded_message = separated[-1] # last line contains the encoded message
        return [user_message, contact_support_message, encoded_message]

    @property
    def encoded_message(self) -> str:
        """The encrypted and encoded part of the message, for AOP support.

        Returns:
            str: encoded message
        """
        return self._encoded_message

    @property
    def user_message(self) -> str:
        """The user-friendly part of the message.

        Returns:
            str: user-friendly message
        """
        return self._user_message

    @property
    def full_message(self) -> str:
        """The full error message as sent by the server.

        Returns:
            str: full error message
        """
        return self.user_message + "\n" + self._contact_support_message + "\n" + self.encoded_message