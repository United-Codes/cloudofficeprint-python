"""Custom exceptions for apexofficeprint."""

from typing import List


class AOPError(Exception):
    """The error that is thrown when the AOP server itself returns an error instead of a result.

    It contains a user message and an encoded message to be handed to AOP support if they are contacted.
    """
    def __init__(self, full_message: str):
        """
        Args:
            full_message (str): the full error message received from the AOP server
        """
        (self._user_message,
         self._contact_support_message,
         self._encoded_message) = self._split_message(full_message)
        super().__init__(self._user_message)

    @staticmethod
    def _split_message(message: str) -> List[str]:   
        """Split the AOP server error message into different parts: user message, contact support message and encoded message.

        Args:
            message (str): AOP server error message

        Returns:
            List[str]: a list with the split messages
        """
        separated = message.split("\n")
        user_message = "\n".join(separated[:-2]) # everything before the last 2 lines are considered user message
        contact_support_message = separated[-2] # second to last line contains the support message
        encoded_message = separated[-1] # last line contains the encoded message
        return [user_message, contact_support_message, encoded_message]

    @property
    def encoded_message(self) -> str:
        """The encrypted and encoded part of the message, for AOP support.

        Returns:
            str: the encrypted and encoded part of the message, for AOP support
        """
        return self._encoded_message

    @property
    def user_message(self) -> str:
        """The user-friendly part of the message.

        Returns:
            str: the user-friendly part of the message
        """
        return self._user_message

    @property
    def contact_support_message(self) -> str:
        """The contact support message.

        Returns:
            str: the contact support message
        """
        return self._contact_support_message

    @property
    def full_message(self) -> str:
        """The full error message as sent by the server.

        Returns:
            str: the full error message as sent by the server
        """
        return self.user_message + "\n" + self.contact_support_message + "\n" + self.encoded_message
