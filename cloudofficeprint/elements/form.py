from typing import Dict, Union,Any, FrozenSet
from .elements import FormElement

class Textbox(FormElement):
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


class RadioButton(FormElement):
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
            result["selected"] = self.selected
        if self.height is not None:
            result["height"] = self.height
        if self.width is not None:
            result["width"] = self.width
        return result

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset([f"{{?form {self.name}}}"])

class Checkbox(FormElement):
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
            result["value"] = self.value
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


class Dropdown(FormElement):
    """PDF form dropdown (non-editable combo box) element

    Args:
        name (str): the PDF field name
        options (list): the selectable options, each a {"value": str, "label": str} dict
        value (str, optional): the value of the option to pre-select
        height (int|str, optional): control height
        width (int|str, optional): control width
        lock (bool, optional): True to lock (make read-only) the field
    """
    def __init__(self,
                 name: str,
                 options: list,
                 value: str = None,
                 height: Union[int, str] = None,
                 width: Union[int, str] = None,
                 lock: bool = None):
        super().__init__(name)
        self.type = "dropdown"
        self.options = options
        self.value = value
        self.height = height
        self.width = width
        self.lock = lock

    @property
    def as_dict(self) -> Dict[str, Any]:
        result = {"type": self.type, "name": self.name, "options": self.options}
        if self.value is not None:
            result["value"] = self.value
        if self.height is not None:
            result["height"] = self.height
        if self.width is not None:
            result["width"] = self.width
        if self.lock is not None:
            result["lock"] = self.lock
        return result

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset([f"{{?form {self.name}}}"])


class ComboBox(Dropdown):
    """PDF form combobox element. Behaves like a Dropdown but the user can also type a free-text value.

    Args:
        name (str): the PDF field name
        options (list): the selectable options, each a {"value": str, "label": str} dict
        value (str, optional): pre-fills the editable field; may be an option value or free text
        height (int|str, optional): control height
        width (int|str, optional): control width
        lock (bool, optional): True to lock (make read-only) the field
    """
    def __init__(self,
                 name: str,
                 options: list,
                 value: str = None,
                 height: Union[int, str] = None,
                 width: Union[int, str] = None,
                 lock: bool = None):
        super().__init__(name, options, value, height, width, lock)
        self.type = "combobox"


class ListBox(FormElement):
    """PDF form listbox element. An always-visible scrollable list that supports multi-selection.

    Args:
        name (str): the PDF field name
        options (list): the selectable options, each a {"value": str, "label": str} dict
        values (list, optional): list of option values to pre-select
        multi_select (bool, optional): True to allow selecting multiple rows
        height (int|str, optional): control height (a taller height shows more rows)
        width (int|str, optional): control width
        lock (bool, optional): True to lock (make read-only) the field
    """
    def __init__(self,
                 name: str,
                 options: list,
                 values: list = None,
                 multi_select: bool = None,
                 height: Union[int, str] = None,
                 width: Union[int, str] = None,
                 lock: bool = None):
        super().__init__(name)
        self.type = "listbox"
        self.options = options
        self.values = values
        self.multi_select = multi_select
        self.height = height
        self.width = width
        self.lock = lock

    @property
    def as_dict(self) -> Dict[str, Any]:
        result = {"type": self.type, "name": self.name, "options": self.options}
        if self.values is not None:
            result["values"] = self.values
        if self.multi_select is not None:
            result["multiSelect"] = self.multi_select
        if self.height is not None:
            result["height"] = self.height
        if self.width is not None:
            result["width"] = self.width
        if self.lock is not None:
            result["lock"] = self.lock
        return result

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset([f"{{?form {self.name}}}"])


class PushButton(FormElement):
    """PDF form push button element. A clickable button widget that carries no value.

    Args:
        name (str): the PDF field name
        caption (str, optional): text shown on the button face
        height (int|str, optional): control height
        width (int|str, optional): control width
        lock (bool, optional): True to lock (make read-only) the field
    """
    def __init__(self,
                 name: str,
                 caption: str = None,
                 height: Union[int, str] = None,
                 width: Union[int, str] = None,
                 lock: bool = None):
        super().__init__(name)
        self.type = "pushbutton"
        self.caption = caption
        self.height = height
        self.width = width
        self.lock = lock

    @property
    def as_dict(self) -> Dict[str, Any]:
        result = {"type": self.type, "name": self.name}
        if self.caption is not None:
            result["caption"] = self.caption
        if self.height is not None:
            result["height"] = self.height
        if self.width is not None:
            result["width"] = self.width
        if self.lock is not None:
            result["lock"] = self.lock
        return result

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset([f"{{?form {self.name}}}"])


class Password(FormElement):
    """PDF form password element. A single-line text input that masks the entered characters.

    Args:
        name (str): the PDF field name
        value (str, optional): pre-fills the field (displayed as masked characters)
        height (int|str, optional): control height
        width (int|str, optional): control width
        lock (bool, optional): True to lock (make read-only) the field
    """
    def __init__(self,
                 name: str,
                 value: str = None,
                 height: Union[int, str] = None,
                 width: Union[int, str] = None,
                 lock: bool = None):
        super().__init__(name)
        self.type = "password"
        self.value = value
        self.height = height
        self.width = width
        self.lock = lock

    @property
    def as_dict(self) -> Dict[str, Any]:
        result = {"type": self.type, "name": self.name}
        if self.value is not None:
            result["value"] = self.value
        if self.height is not None:
            result["height"] = self.height
        if self.width is not None:
            result["width"] = self.width
        if self.lock is not None:
            result["lock"] = self.lock
        return result

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset([f"{{?form {self.name}}}"])