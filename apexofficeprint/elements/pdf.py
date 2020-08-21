from abc import ABC, abstractmethod
from typing import Union, FrozenSet, Iterable, Mapping
from .elements import Element, Object

class PDFInsertObject(ABC):
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
    """# TODO"""
    # there can only be one or they will overwrite
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
    """# TODO"""
    # there can only be one or they will overwrite
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
    # there can only be one or they will overwrite
    def __init__(self, **form_data: Mapping[str, Union[str, bool]]):
        super().__init__("aop_pdf_form_data")
        self.form_data = form_data

    @property
    def as_dict(self):
        return self.form_data

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset()
