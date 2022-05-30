from abc import ABC, abstractmethod
from typing import Dict, Union, FrozenSet, Iterable, Mapping
from .elements import Element, ElementCollection

class PDFInsertObject(ABC):
    """Abstract base class for PDF's insertable objects."""
    def __init__(self,
                 x: int,
                 y: int,
                 page: Union[int, str] = "all"):
        """
        Args:
            x (int): X component of this object's position.
            y (int): Y component of this object's position.
            page (Union[int, str], optional): Page to include this object on. Either "all" or an integer. Defaults to "all".
        """
        self.x: int = x
        self.y: int = y
        self.page: Union[int, str] = page        

    @property
    @abstractmethod
    def _inner_dict(self) -> Dict:
        """Get the dict representation of this PDFInsertObject.

        Returns:
            Dict: dict representation of this PDFInsertObject
        """
        pass

    @staticmethod
    @abstractmethod
    def _identifier() -> str:
        """Get the identifier for this PDFInsertObject.

        Returns:
            str: identifier for this PDFInsertObject
        """
        pass


class PDFText(PDFInsertObject):
    """Adds text to a PDF"""
    def __init__(self,
                 text: str,
                 x: int,
                 y: int,
                 page: Union[int, str] = "all",
                 rotation: int = None,
                 bold: bool = None,
                 italic: bool = None,
                 font: str = None,
                 font_color: str = None,
                 font_size: int = None):
        """
        Args:
            text (str): Text to insert.
            x (int): X component of this object's position.
            y (int): Y component of this object's position.
            page (Union[int, str], optional): Page to include this object on. Either "all" or an integer. Defaults to "all".
            rotation (int, optional): Text rotation in degrees. Defaults to None.
            bold (bool, optional): Whether or not the text should be in bold. Defaults to None.
            italic (bool, optional): Whether or not the text should be in italic. Defaults to None.
            font (str, optional): The text font name. Defaults to None.
            font_color (str, optional): The text font color, CSS notation. Defaults to None.
            font_size (int, optional): The text font size. Defaults to None.
        """
        super().__init__(x, y, page)
        self.text: str = text
        self.rotation: int = rotation
        self.bold: bool = bold
        self.italic: bool = italic
        self.font: str = font
        self.font_color: str = font_color
        self.font_size: int = font_size

    @staticmethod
    def _identifier() -> str:
        return "AOP_PDF_TEXTS"

    @property
    def _inner_dict(self) -> Dict:
        result = {
            "text": self.text,
            "x": self.x,
            "y": self.y
        }

        if self.rotation is not None:
            result["rotation"] = self.rotation
        if self.bold is not None:
            result["bold"] = self.bold
        if self.italic is not None:
            result["italic"] = self.italic
        if self.font is not None:
            result["font"] = self.font
        if self.font_color is not None:
            result["font_color"] = self.font_color
        if self.font_size is not None:
            result["font_size"] = self.font_size

        return result


class PDFImage(PDFInsertObject):
    """Inserts an image into a PDF."""
    def __init__(self,
                 image: str,
                 x: int,
                 y: int,
                 page: Union[int, str] = "all",
                 rotation: int = None,
                 width: int = None,
                 height: int = None,
                 max_width: int = None):
        """
        Args:
            image (str): The image's base64 string or URL.
            x (int): X component of this object's position.
            y (int): Y component of this object's position.
            page (Union[int, str], optional): Page to include this object on. Either "all" or an integer. Defaults to "all".
            rotation (int, optional): Rotation in degrees. Defaults to None.
            width (int, optional): Image width in px. Defaults to None.
            height (int, optional): Image height in px. Defaults to None.
            max_width (int, optional): Max image height in px (for scaling purposes). Defaults to None.
        """
        super().__init__(x, y, page)
        self.image: str = image
        self.rotation: int = rotation
        self.width: int = width
        self.height: int = height
        self.max_width: int = max_width

    @staticmethod
    def _identifier() -> str:
        return "AOP_PDF_IMAGES"

    @property
    def _inner_dict(self) -> Dict:
        result = {
            "image": self.image,
            "x": self.x,
            "y": self.y
        }

        if self.rotation is not None:
            result["rotation"] = self.rotation
        if self.width is not None:
            result["image_width"] = self.width
        if self.height is not None:
            result["image_height"] = self.height
        if self.max_width is not None:
            result["image_max_width"] = self.max_width

        return result

class PDFTexts(Element):
    """Group of PDF texts as an `Element`.
    There can only be one of this `Element`.
    Element name is fixed and important to the server, so multiple will just overwrite.
    """
    def __init__(self, texts: Iterable[PDFText]):
        """
        Args:
            texts (Iterable[PDFText]): An iterable consisting of `PDFText`-objects.
        """
        super().__init__(PDFText._identifier())
        self.texts: Iterable[PDFText] = texts

    @property
    def as_dict(self) -> Dict:
        result = {}
        for txt in self.texts:
            # If there already is text for this page -> update entry in dictionary
            #   else -> create new entry in dictionary
            if str(txt.page) in result:
                result[str(txt.page)].append(txt._inner_dict)
            else:
                result[str(txt.page)] = [txt._inner_dict]
        return {self.name: [result]}

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset()


class PDFImages(Element):
    """Group of PDF images as an `Element`.
    There can only be one of this `Element`.
    Element name is fixed and important to the server, so multiple will just overwrite.
    """
    def __init__(self, images: Iterable[PDFImage]):
        """
        Args:
            images (Iterable[PDFImage]): An iterable consisting of `PDFImage`-objects.
        """
        super().__init__(PDFImage._identifier())
        self.images = images
    
    @property
    def as_dict(self) -> Dict:
        result = {}
        for img in self.images:
            # If there already is an image for this page -> update entry in dictionary
            #   else -> create new entry in dictionary
            if str(img.page) in result:
                result[str(img.page)].append(img._inner_dict)
            else:
                result[str(img.page)] = [img._inner_dict]
        return {self.name: [result]}

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset()

class PDFFormData(Element):
    """Class used for filling in PDF forms.
    There can only be one of this `Element`.
    Element name is fixed and important to the server, so multiple will just overwrite.
    """
    def __init__(self, form_data: Mapping[str, Union[str, bool]]):
        """
        Args:
            form_data (Mapping[str, Union[str, bool, int, float]]): a mapping containing the keys and values of the fields that need to be entered in the PDF form
        """
        super().__init__(PDFFormData._identifier())
        self.form_data = form_data

    @staticmethod
    def _identifier() -> str:
        """Get the identifier for this element.

        Returns:
            str: identifier for this element
        """
        return 'aop_pdf_form_data'

    @property
    def as_dict(self) -> Dict:
        return {self.name: self.form_data}

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset()


class PDFFormElement(Element):
    """
    Abstract base class for PDF form elements.
    """
    def __init__(self,
                 name: str,
                 width: int = None,
                 height: int = None,
                 ):
        """
        Args:
            name (str): The name for this element.
            width (int): The width in px. Optional.
            height (int): The height in px. Optional.
        """
        super().__init__(name)
        self.width: int = width
        self.height: int = height

    @property
    @abstractmethod
    def type(self) -> str:
        """ Type of this PDF form element.

        Returns:
            The type of this PDF form element.
        """
        pass

    @property
    def _inner_dict(self) -> Dict:
        """ Inner dict of this PDF form element.

        Returns:
            The inner dict of this PDF form element.
        """
        result = {
            "name": self.name,
            "type": self.type,
        }

        if self.width is not None:
            result['width'] = self.width
        if self.height is not None:
            result['height'] = self.height

        return result

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{?form " + self.name + "}"})


class PDFFormTextBox(PDFFormElement):
    """
    Class for a PDF form text box element.
    """
    def __init__(self,
                 name: str,
                 value: str = None,
                 width: int = None,
                 height: int = None,
                 ):
        """
        Args:
            name (str): The name for this element.
            value (str): The value for this text box. Optional
            width (int): The width in px. Optional.
            height (int): The height in px. Optional.
        """
        super().__init__(name, width, height)
        self.value: str = value

    @property
    def type(self) -> str:
        return "text"

    @property
    def as_dict(self) -> Dict:
        result = super()._inner_dict

        if self.value is not None:
            result['value'] = self.value

        return {self.name: result}


class PDFFormCheckBox(PDFFormElement):
    """
        Class for a PDF form checkbox element.
    """
    def __init__(self,
                 name: str,
                 check: bool = None,
                 text: str = None,
                 width: int = None,
                 height: int = None,
                 ):
        """
        Args:
            name (str): The name for this element.
            check (str): Whether the checkbox is checked. Optional.
            width (int): The width in px. Optional.
            height (int): The height in px. Optional.
        """
        super().__init__(name, width, height)
        self.check: bool = check
        self.text: str = text

    @property
    def type(self) -> str:
        return "checkbox"

    @property
    def as_dict(self) -> Dict:
        result = super()._inner_dict

        if self.check is not None:
            result['value'] = self.check
        if self.text is not None:
            result['text'] = self.text

        return {self.name: result}


class PDFFormRadioButton(PDFFormElement):
    """
        Class for a PDF form radio button element.
    """
    def __init__(self,
                 name: str,
                 group: str = None,
                 value: str = None,
                 text: str = None,
                 selected: bool = None,
                 width: int = None,
                 height: int = None,
                 ):
        """
        Args:
            name (str): The name for this element.
            group (str): name of radio buttons that are interconnected. Optional.
            value (str): The value of this radio button. Optional
            text (str): The text used as label for the radio button. Optional
            selected (bool): Whether the radio button is selected. Optional
            width (int): The width in px. Optional.
            height (int): The height in px. Optional.
        """
        super().__init__(name, width, height)
        self.group: str = group
        self.value: str = value
        self.text: str = text
        self.selected: bool = selected

    @property
    def type(self) -> str:
        return "radio"

    @property
    def as_dict(self) -> Dict:
        result = super()._inner_dict

        if self.group is not None:
            result['name'] = self.group
        if self.value is not None:
            result['value'] = self.value
        if self.text is not None:
            result['text'] = self.text
        if self.selected is not None:
            result['selected'] = self.selected

        return {self.name: result}


class PDFFormSignature(PDFFormElement):
    """
        Class for a PDF form unsigned signature field element.
    """
    def __init__(self,
                 name: str,
                 width: int = None,
                 height: int = None,
                 ):
        """
        Args:
            name (str): The name for this element.
            width (int): The width in px. Optional.
            height (int): The height in px. Optional.
        """
        super().__init__(name, width, height)

    @property
    def type(self) -> str:
        return "signaturefieldunsigned"

    @property
    def as_dict(self) -> Dict:
        return {self.name: super()._inner_dict}

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{?sign " + self.name + "}"})


class PDFFormSignatureSigned(PDFFormSignature):
    """
        Class for a PDF form signed signature field element.
    """
    def __init__(self,
                 name: str,
                 value: str,
                 password: str = None,
                 size: str = None,
                 background_image: str = None,
                 width: int = None,
                 height: int = None,
                 ):
        """
        Args:
            name (str): The name for this element.
            value (str): The signing certificate as a base64 string, URL, FTP location or a server path.
            password (str): The password for if the certificate is encrypted. Optional.
            size (str): The size must either be "sm" for small, "md" for medium or "lg" for large. Optional.
            background_image (str): The background image as a base64 string, URL, FTP location or a server path. Optional.
            width (int): The width in px. Optional.
            height (int): The height in px. Optional.
        """
        super().__init__(name, width, height)
        self.value: str = value
        self.password: str = password
        self.size: str = size
        self.background_image: str = background_image

    @property
    def type(self) -> str:
        return "signaturefieldsigned"

    @property
    def as_dict(self) -> Dict:
        result = super()._inner_dict

        if self.value is not None:
            result['value'] = self.value
        if self.password is not None:
            result['password'] = self.password
        if self.size is not None:
            result['size'] = self.size
        if self.background_image is not None:
            result['background_image'] = self.background_image

        return {self.name: result}
