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
