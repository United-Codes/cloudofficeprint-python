from abc import ABC, abstractmethod
from typing import Union, FrozenSet, Iterable, Mapping
from .elements import Element, Object

class PDFInsertObject(ABC):
    """Abstract base class for PDF's insertable objects."""
    def __init__(self,
                 x: int,
                 y: int,
                 page: Union[int, str] = "all"):
        self.x: int = x
        """X component of this object's position."""
        self.y: int = y
        """Y component of this object's position."""
        self.page: Union[int, str] = page
        """Page to include this object on. Either "all" or an integer."""

    @property
    @abstractmethod
    def _inner_dict(self) -> dict:
        pass

    @property
    @abstractmethod
    def _identifier(self) -> str:
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
            text (str): `PDFText.text`
            x (int): `PDFText.x`
            y (int): `PDFText.y`
            page (Union[int, str], optional): `PDFText.page`. Defaults to "all".
            rotation (int, optional): `PDFText.rotation`. Defaults to None.
            bold (bool, optional): `PDFText.bold`. Defaults to None.
            italic (bool, optional): `PDFText.italic`. Defaults to None.
            font (str, optional): `PDFText.font`. Defaults to None.
            font_color (str, optional): `PDFText.font_color`. Defaults to None.
            font_size (int, optional): `PDFText.font_size`. Defaults to None.
        """
        super().__init__(x, y, page)
        self.text: str = text
        """Text to insert."""
        self.rotation: int = rotation
        """Text rotation in degrees."""
        self.bold: bool = bold
        """Should text be bold?"""
        self.italic: bool = italic
        """Should text be in italics?"""
        self.font: str = font
        """Text font name."""
        self.font_color: str = font_color
        """Text font color, CSS notation."""
        self.font_size: int = font_size
        """Text font size."""

    @property
    def _identifier(self) -> str:
        return "AOP_PDF_TEXTS"

    def _inner_dict(self) -> dict:
        result = {
            "text": self.text,
            "x": self.x,
            "y": self.y
        }

        if self.rotation:
            result["rotation"] = self.rotation
        if self.bold:
            result["bold"] = self.bold
        if self.italic:
            result["italic"] = self.italic
        if self.font:
            result["font"] = self.font
        if self.font_color:
            result["font_color"] = self.font_color
        if self.font_size:
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
        super().__init__(x, y, page)
        self.image: str = image
        """Image base64 or URL."""
        self.rotation: int = rotation
        """Rotation in degrees."""
        self.width: int = width
        """Image width in px."""
        self.height: int = height
        """Image height in px."""
        self.max_width: int = max_width
        """Max image height in px (for scaling purposes)."""

    @property
    def _identifier(self) -> str:
        return "AOP_PDF_IMAGES"

    @property
    def _inner_dict(self) -> dict:
        result = {
            "image": self.image,
            "x": self.x,
            "y": self.y
        }

        if self.rotation:
            result["rotation"] = self.rotation
        if self.width:
            result["image_width"] = self.width
        if self.height:
            result["image_height"] = self.height
        if self.max_width:
            result["image_max_width"] = self.max_width

        return result

class PDFTexts(Element):
    """Group of PDF texts as an `Element`.
    
    There can only be one of this `Element`.
    (Element name is fixed and important to the server, so multiple will just overwrite)
    and it should be at the outer level of an `Object`.
    """
    # TODO: it may make more sense to do these (PDFTexts, PDFImages, PDFFormData) as config options,
    # then PrintJob has to add the "AOP_PDF_TEXTS" Object to the data.
    def __init__(self, texts: Iterable[PDFText]):
        super().__init__("AOP_PDF_TEXTS")
        self.texts = texts
    
    @property
    def as_dict(self):
        return {
            str(txt.page): txt._inner_dict for txt in self.texts
        }

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset()


class PDFImages(Element):
    """Group of PDF images as an `Element`.
    
    There can only be one of this `Element`.
    (Element name is fixed and important to the server, so multiple will just overwrite)
    and it should be at the outer level of an `Object`.
    """
    def __init__(self, images: Iterable[PDFImage]):
        super().__init__("AOP_PDF_IMAGES")
        self.images = images
    
    @property
    def as_dict(self):
        return {
            str(img.page): img._inner_dict for img in self.images
        }

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset()

class PDFFormData(Element):
    """PDF form data as an `Element`.
    
    There can only be one of this `Element`.
    (Element name is fixed and important to the server, so multiple will just overwrite)
    and it should be at the outer level of an `Object`.
    """
    def __init__(self, **form_data: Mapping[str, Union[str, bool]]):
        super().__init__("aop_pdf_form_data")
        self.form_data = form_data

    @property
    def as_dict(self):
        return self.form_data

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset()
