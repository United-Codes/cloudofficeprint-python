from typing import Dict, Union,Any, FrozenSet
from .elements import Element

class Textbox(Element):
    """PDF form textbox element 

    Args:
        name (str): the PDF field name
        value (str, optional): text to put into the box
        height (int|str, optional): box height
        width (int|str, optional): box width
        multiline (bool, optional): True for multiline input (serialized as 1/0)
    """
    def __init__(self,
                 name: str,
                 value: str = None,
                 height: Union[int, str] = None,
                 width: Union[int, str] = None,
                 multiline: bool = None):
        super().__init__(name)
        self.type = "text"
        self.value = value
        self.height = height
        self.width = width
        self.multiline = multiline
    @property
    def as_dict(self) -> Dict[str, Any]:
        result = {"type": self.type, "name": self.name}
        if self.value is not None:
            result["value"] = self.value
        if self.height is not None:
            result["height"] = self.height
        if self.width is not None:
            result["width"] = self.width
        if self.multiline is not None:
            result["multiline"] = self.multiline  
        return result
    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset([f"{{?form {self.name}}}"])


class RadioButton(Element):
    """PDF form radio button element 

    Args:
        name (str): the PDF field name
        value (str, optional): the field’s export values
        text (str, optional): visible caption next to the button
        selected (bool, optional): True if this button is chosen (serialized as 1/0)
        height (int|str, optional): control height
        width (int|str, optional): control width
    """
    def __init__(self,
                 name: str,
                 value: str = None,
                 text: str = None,
                 selected: bool = None,
                 height: Union[int, str] = None,
                 width: Union[int, str] = None):
        super().__init__(name)
        self.type = "radio"
        self.value = value
        self.text = text
        self.selected = selected
        self.height = height
        self.width = width
    
    @property
    def as_dict(self) -> Dict[str, Any]:
        result = {"type": self.type, "name": self.name}
        if self.value is not None:
            result["value"] = self.value
        if self.text is not None:
            result["text"] = self.text
        if self.selected is not None:
            result["selected"] = 1 if self.selected else 0
        if self.height is not None:
            result["height"] = self.height
        if self.width is not None:
            result["width"] = self.width
        return result

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset([f"{{?form {self.name}}}"])

class Checkbox(Element):
    """PDF form checkbox element 

    Args:
        name (str): the PDF field name
        value (bool, optional): True if checked (serialized as 1/0)
        text (str, optional): visible caption next to the box
        height (int|str, optional): control height
        width (int|str, optional): control width
    """
    
    def __init__(self, name: str, value: bool = None, 
                 text: str = None, 
                 height: Union[int, str] = None,
                 width: Union[int, str] = None):
        super().__init__(name)
        self.type = "checkbox"
        self.value = value
        self.text = text
        self.height = height
        self.width = width

    @property
    def as_dict(self) -> Dict[str, Any]:
        result = {"type": self.type, "name": self.name}
        if self.value is not None:
            result["value"] = 1 if self.value else 0
        if self.text is not None:
            result["text"] = self.text
        if self.height is not None:
            result["height"] = self.height
        if self.width is not None:
            result["width"] = self.width
        return result

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset([f"{{?form {self.name}}}"])