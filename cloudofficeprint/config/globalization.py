from typing import Dict, List, Mapping


class NativeLanguageSupport:
    """Class for optional native language support options.
    All of them are optional, which is why passing an instance of this class
    in a Globalization object is also optional.
    """

    def __init__(self,
                 sort: str = None,
                 comp: str = None,
                 numeric_characters_dec_grp: str = None,
                 currency: str = None,
                 territory: str = None,
                 language: str = None,
                 ):
        """
        Args:
            sort (str): the native language support sort. Defaults to None.
            comp (str): the native language support comp. Defaults to None.
            numeric_characters_dec_grp (str): the native language support numeric characters decimal group. Defaults to None.
            currency (str): the native language support currency. Defaults to None.
            territory (str): the native language support territory. Defaults to None.
            language (str): the native language support language. Defaults to None.
        """
        self.sort: str = sort
        self.comp: str = comp
        self.numeric_characters_dec_grp: str = numeric_characters_dec_grp
        self.currency: str = currency
        self.territory: str = territory
        self.language: str = language

    @property
    def as_dict(self) -> Dict:
        """The dict representation of these native language support options.

                Returns:
                    Dict: the dict representation of these native language support options.
                """
        result = {}

        if self.sort is not None:
            result["nls_sort"] = self.sort
        if self.comp is not None:
            result["nls_comp"] = self.comp
        if self.numeric_characters_dec_grp is not None:
            result["nls_numeric_characters_dec_grp"] = self.numeric_characters_dec_grp
        if self.currency is not None:
            result["nls_currency"] = self.currency
        if self.territory is not None:
            result["nls_territory"] = self.territory
        if self.language is not None:
            result["nls_language"] = self.language

        return result


class Globalization:
    """Class for optional globalization options.
    The properties of this class define all possible globalization options.
    All of them are optional, which is why passing an instance of this class
    in an PrintJob is also optional.
    """

    def __init__(self,
                 date_format: str = None,
                 date_time_format: str = None,
                 timestamp_format: str = None,
                 timestamp_tz_format: str = None,
                 direction: str = None,
                 application_primary_language: str = None,
                 native_language_support: NativeLanguageSupport = None,
                 ):
        """
        Args:
            date_format (str): The date format. Defaults to None.
            date_time_format (str): The date time format. Defaults to None.
            timestamp_format (str): The timestamp format. Defaults to None.
            timestamp_tz_format (str): The timestamp tz format. Defaults to None.
            direction (str): The direction. Defaults to None.
            application_primary_language (str): The application primary language. Defaults to None.
            native_language_support (NativeLanguageSupport): The native language support options. Defaults to None.
        """
        self.date_format: str = date_format
        self.date_time_format: str = date_time_format
        self.timestamp_format: str = timestamp_format
        self.timestamp_tz_format: str = timestamp_tz_format
        self.direction: str = direction
        self.application_primary_language: str = application_primary_language
        self.native_language_support: NativeLanguageSupport = native_language_support

    @property
    def as_dict(self) -> Dict:
        """The dict representation of these globalization options.

                Returns:
                    Dict: the dict representation of these globalization options.
                """
        result = {}

        if self.date_format is not None:
            result["date_format"] = self.date_format
        if self.date_time_format is not None:
            result["date_time_format"] = self.date_time_format
        if self.timestamp_format is not None:
            result["timestamp_format"] = self.timestamp_format
        if self.timestamp_tz_format is not None:
            result["timestamp_tz_format"] = self.timestamp_tz_format
        if self.direction is not None:
            result["direction"] = self.direction
        if self.application_primary_language is not None:
            result["application_primary_language"] = self.application_primary_language
        if self.native_language_support is not None:
            result.update(self.native_language_support.as_dict)

        return result
