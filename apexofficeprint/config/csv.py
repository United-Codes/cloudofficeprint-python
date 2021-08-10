import json
from typing import Dict

class CsvOptions:
    """Class of optional PDF options.

    The properties of this class define all possible PDF output options.
    All of them are optional, which is why passing an instance of this class in an OutputConfig is also optional.
    These options can be used when the template is xlsx and the output is csv.
    """
    
    def __init__(
        self,
        text_delimiter: str = None,
        field_separator: str = None,
        character_set: int = None,
    ):
        """
        Args:
            text_delimiter (str, optional): this option will specify the text delimiter. Can be " or ' (default "). Defaults to None.
            field_separator (str, optional): this option will specify the field separator. Default ,.
                Can be any ascii character or 'tab' for tab and 'space' for space. Defaults to None.
            character_set (str, optional): this option will determine the character set. Should be an integer.
                See: https://wiki.openoffice.org/wiki/Documentation/DevGuide/Spreadsheets/Filter_Options#Filter_Options_for_Lotus.2C_dBase_and_DIF_Filters
                for possible values. Default 0 or system encoding. Defaults to None.
        """
        self.text_delimiter: str = text_delimiter
        self.field_separator: str = field_separator
        self.character_set: int = character_set
    
    def __str__(self) -> str:
        """Get the string representation of these csv options.

        Returns:
            str: string representation of these csv options
        """
        return self.json

    @property
    def json(self) -> str:
        """The JSON representation of these csv options.

        The JSON representation is a direct JSON dump of the dict representation.
        The dict representation is accessed through the `as_dict` property.

        Returns:
            str: JSON representation of these csv options
        """
        return json.dumps(self.as_dict)

    @property
    def as_dict(self) -> Dict:
        """The dict representation of these csv options.

        Returns:
            Dict: the dict representation of these csv options
        """
        result = {}

        if self.text_delimiter is not None:
            result['output_text_delimiter'] = self.text_delimiter
        if self.field_separator is not None:
            result['output_field_separator'] = self.field_separator
        if self.character_set is not None:
            result['output_character_set'] = self.character_set

        return result