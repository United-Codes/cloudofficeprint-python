import json
from .._utils import file_utils
from copy import deepcopy
from typing import Union, Iterable, Mapping, Set, FrozenSet, Dict, List
from abc import abstractmethod, ABC


class CellStyle:
    def __init__(self, background_color: str = None, width: str = None):
        self.background_color: str = background_color
        self.width: Union[str, int] = width

    def get_dict(self, property_name: str):
        result = {}
        for suffix, value in self._dict_suffixes.items():
            result[property_name + suffix] = value
        return result

    @property
    def _dict_suffixes(self):
        result = {}

        if self.background_color:
            result["_background_color"] = self.background_color
        if self.width:
            result["_width"] = self.width

        return result


class Element(ABC):
    """ The abstract base class for elements."""

    def __init__(self, name: str):
        self.name = name
        """Name for this element

        Returns:
            str: element name
        """

    def __str__(self):
        return self.json

    def __repr__(self):
        return self.json

    @property
    def json(self) -> str:
        """json representation of this `Element`.

        Isomorphic with the dict representation (`Element.as_dict`).

        Returns:
            str: json representation
        """
        return json.dumps(self.as_dict)

    @property
    @abstractmethod
    def as_dict(self) -> dict:
        """Dictionary representation of this `Element`.

        Isomorphic with the json representation (`Element.json`).

        Returns:
            dict: dictionary representation
        """
        pass

    @property
    @abstractmethod
    def available_tags(self) -> FrozenSet[str]:
        """A `frozenset` containing all available template tags this `Element` reacts to.

        Returns:
            FrozenSet[str]: set of tags associated with this `Element`
        """
        pass


class Property(Element):
    """The most basic `Element`. It simply consists of a name and a value.

    In a template, `{name}` is replaced by `value`.
    """

    def __init__(self, name: str, value: str):
        super().__init__(name)
        self.value: Union[int, str] = value
        """Value of this property."""

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{" + self.name + "}"})

    @property
    def as_dict(self) -> dict:
        return {
            self.name: self.value
        }


class CellStyleProperty(Property):
    def __init__(self, name: str, value: str, cell_style: CellStyle):
        super().__init__(name, value)
        self.cell_style: CellStyle = cell_style
        """Cell style as a `CellStyle`."""

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{" + self.name + "$}"})

    @property
    def as_dict(self):
        result = {
            self.name: self.value
        }

        for suffix, value in self.cell_style._dict_suffixes.items():
            result[self.name + suffix] = value

        return result


class Html(Property):
    def __init__(self, name: str, value: str):
        super().__init__(name, value)

    @property
    def available_tags(self):
        return frozenset({"{_" + self.name + "}"})


class RightToLeft(Property):
    def __init__(self, name: str, value: str):
        super().__init__(name, value)

    @property
    def available_tags(self):
        return frozenset({"{<" + self.name + "}"})


class FootNote(Property):
    def __init__(self, name: str, value: str):
        super().__init__(name, value)

    @property
    def available_tags(self):
        return frozenset({"{+" + self.name + "}"})


class HyperLink(Element):
    def __init__(self, name: str, url: str, text: str = None):
        super().__init__(name)
        self.url: str = url
        self.text: str = text

    @property
    def available_tags(self):
        return frozenset({"{*" + self.name + "}"})

    @property
    def as_dict(self):
        result = {
            self.name: self.url
        }

        if self.text:
            result[self.name + "_text"] = self.text

        return result


class TableOfContents(Element):
    def __init__(self, name: str, title: str, depth: int = None, tab_leader: str = None):
        super().__init__(name)
        self.title: str = title
        self.depth: int = None
        self.tab_leader: str = None

    @property
    def available_tags(self):
        return frozenset({"{~" + self.name + "}"})

    @property
    def as_dict(self):
        result = dict()

        if self.title:
            result[self.name + "_title"] = self.title
        if self.depth:
            result[self.name + "_show_level"] = self.depth
        if self.tab_leader:
            result[self.name + "_tab_leader"] = self.tab_leader

        return result


class Raw(Property):
    def __init__(self, name: str, value: str):
        super().__init__(name, value)

    @property
    def available_tags(self):
        return frozenset({"{@" + self.name + "}"})


class Span(Property):
    def __init__(self, name: str, value: str, columns: int, rows: int):
        super().__init__(name, value)
        self.columns = columns
        self.rows = rows

    @property
    def available_tags(self):
        return frozenset({"{" + self.name + "#}"})

    @property
    def as_dict(self):
        return {
            self.name: self.value,
            self.name + "_row_span": self.rows,
            self.name + "_col_span": self.columns
        }


class Formula(Property):
    def __init__(self, name: str, formula: str):
        super().__init__(name, formula)

    @property
    def available_tags(self):
        return frozenset({"{>" + self.name + "}"})


class StyledProperty(Property):
    def __init__(self,
                 name: str,
                 value: str,
                 font: str = None,
                 font_size: Union[str, int] = None,
                 font_color: str = None,
                 bold: bool = None,
                 italic: bool = None,
                 underline: bool = None,
                 strikethrough: bool = None,
                 highlight_color: bool = None):
        super().__init__(name, value)
        self.font: str = font,
        self.font_size: Union[str, int] = font_size,
        self.font_color: str = font_color,
        self.bold: bool = bold,
        self.italic: bool = italic,
        self.underline: bool = underline,
        self.strikethrough: bool = strikethrough,
        self.highlight_color: bool = highlight_color

    @property
    def available_tags(self):
        return frozenset({"{style " + self.name + "}"})

    @property
    def as_dict(self):
        result = {
            self.name: self.value
        }

        if self.font:
            result[self.name + "_font_family"] = self.font
        if self.font_size:
            result[self.name + "_font_size"] = self.font_size
        if self.font_color:
            result[self.name + "_font_color"] = self.font_color
        if self.bold is not None:
            result[self.name + "_bold"] = self.bold
        if self.italic is not None:
            result[self.name + "_italic"] = self.italic
        if self.underline is not None:
            result[self.name + "_underline"] = self.underline
        if self.strikethrough is not None:
            result[self.name + "_strikethrough"] = self.strikethrough
        if self.font_color:
            result[self.name + "_font_color"] = self.font_color

        return result


class Watermark(Property):
    def __init__(self,
                 name: str,
                 text: str,
                 color: str = None,
                 font: str = None,
                 width: Union[int, str] = None,
                 height: Union[int, str] = None,
                 opacity: float = None,
                 rotation: int = None):
        super().__init__(name, text)
        self.color: str = color,
        self.font: str = font,
        self.width: Union[int, str] = width,
        self.height: Union[int, str] = height,
        self.opacity: float = opacity,
        self.rotation: int = rotation

    @property
    def available_tags(self):
        return frozenset({"{watermark " + self.name + "}"})

    @property
    def as_dict(self):
        result = {
            self.name: self.value
        }

        if self.color:
            result[self.name + "_color"] = self.color
        if self.font:
            result[self.name + "_font"] = self.font
        if self.width:
            result[self.name + "_width"] = self.width
        if self.height:
            result[self.name + "_height"] = self.height
        if self.opacity:
            result[self.name + "_opacity"] = self.opacity
        if self.rotation:
            result[self.name + "_rotation"] = self.rotation

        return result


class D3Code(Property):
    def __init__(self, name: str, code: str):
        super().__init__(name, code)

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{$d3 " + self.name + "}"})


class Code(Element):
    """Superclass for QR-codes and barcodes"""
    def __init__(self, name: str, data: str, type: str):
        super().__init__(name)
        self.data: str = data
        self.type: str = type
        """For the different types of QR-codes and barcodes, we refer to the AOP documentation: http://www.apexofficeprint.com/docs/#barcode-qrcode-tags"""
    
    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{|" + self.name + "}"})

    @property
    def _dict_suffixes(self):
        result = {}

        if self.type is not None:
            result["_type"] = self.type

        return result

    @property
    def as_dict(self) -> dict:
        result = {
            self.name: self.data
        }

        for suffix, value in self._dict_suffixes.items():
            result[self.name + suffix] = value

        return result
    
class BarCode(Code):
    """This class is a subclass of Code and is used to generate a barcode element"""
    def __init__(
            self,
            name: str,
            data: str,
            type: str,
            height: int = None,
            width: int = None,
            errorcorrectlevel: str = None,
            url: str = None,
            rotation: int = None,
            background_color: str = None,
            padding_width: int = None,
            padding_height: int = None,
            extra_options: str = None
        ):
        super().__init__(name, data, type)
        self.height: int = height
        """ This field contains the height for the generated image. Default is 200 for QR, 50 for the rest."""
        self.width: int = width
        """This field contains the width for the generated image. Default is 200."""
        self.errorcorrectlevel: str = errorcorrectlevel
        """This field contains the level of which the QR code should be recoverable. The options are:
            "L" (up to 7% damage)
            "M" (up to 15% damage)
            "Q" (up to 25% damage)
            "H" (up to 30% damage)
        """
        self.url: str = url
        """The URL to hyperlink to when the barcode/qrcode is clicked"""
        self.rotation: int = rotation
        """The rotation angle of the barcode/qrcode (in degrees, counterclockwise)"""
        self.background_color: str = background_color
        """The background color for the barcode/qrcode. default: white/ffffff.
        You can provide hex value; html named colors like red, white, purple; rgb(255, 0, 0) ; or any other css supported format."""
        self.padding_width: int = padding_width
        """The padding of the inserted qrcode/barcode. default 10. In pixels"""
        self.padding_height: int = padding_height
        """The padding of the inserted qrcode/barcode. default 10. In pixels"""
        self.extra_options: str = extra_options
        """If you want to include extra options like including barcode text on the bottom. 
        The options should be space separated and should be followed by a "=" and their value.
        E.g.: "includetext guardwhitespace guardwidth=3 guardheight=3".
        Please visit: https://github.com/bwipp/postscriptbarcode/wiki/Symbologies-Reference for all option availability."""
    
    @property
    def _dict_suffixes(self):
        result = super()._dict_suffixes

        if self.height is not None:
            result['_height'] = self.height
        if self.width is not None:
            result['_width'] = self.width
        if self.errorcorrectlevel is not None:
            result['_errorcorrectlevel'] = self.errorcorrectlevel
        if self.url is not None:
            result['_url'] = self.url
        if self.rotation is not None:
            result['_rotation'] = self.rotation
        if self.background_color is not None:
            result['_background_color'] = self.background_color
        if self.padding_width is not None:
            result['_padding_width'] = self.padding_width
        if self.padding_height is not None:
            result['_padding_height'] = self.padding_height
        if self.extra_options is not None:
            result['_extra_options'] = self.extra_options

        return result


class QRCode(Code):
    """This class is a subclass of Code and serves as a superclass for the different types of QR-codes"""
    # TODO: create setters (or constructor) for QR-code options (see documentation)
    def __init__(self, name: str, data: str, type: str):
        super().__init__(name, data, type)
    
    @property
    def _dict_suffixes(self):
        result = super()._dict_suffixes

        return result


class WiFiQRCode(QRCode):
    """This class is a subclass of QRCode and is used to generate a WiFi QR-code element"""
    def __init__(
        self,
        name: str,
        ssid: str,
        wifi_encryption: str,
        wifi_password: str = None,
        wifi_hidden: bool = None
    ):
        super().__init__(name, ssid, 'qr_wifi')
        self.wifi_password: str = wifi_password
        self.wifi_encryption: str = wifi_encryption
        self.wifi_hidden: bool = wifi_hidden
    
    @property
    def _dict_suffixes(self):
        result = super()._dict_suffixes

        if self.wifi_password is not None:
            result['_wifi_password'] = self.wifi_password
        if self.wifi_hidden is not None:
            result['_wifi_encryption'] = self.wifi_encryption
        result['_wifi_hidden'] = self.wifi_hidden

        return result
    
class TelephoneNumberQRCode(QRCode):
    """This class is a subclass of QRCode and is used to generate a telephone number QR-code element"""
    def __init__(self, name: str, number: str):
        super().__init__(name, number, 'qr_telephone')

class EmailQRCode(QRCode):
    """This class is a subclass of QRCode and is used to generate an email QR-code element"""
    def __init__(
        self,
        name: str,
        receiver: str,
        cc: str = None,
        bcc: str = None,
        subject: str = None,
        body: str = None
    ):
        super().__init__(name, receiver, 'qr_email')
        self.cc: str = cc
        self.bcc: str = bcc
        self.subject: str = subject
        self.body: str = body
    
    @property
    def _dict_suffixes(self):
        result = super()._dict_suffixes

        if self.cc is not None:
            result['_email_cc'] = self.cc
        if self.bcc is not None:
            result['_email_bcc'] = self.bcc
        if self.subject is not None:
            result['_email_subject'] = self.subject
        if self.body is not None:
            result['_email_body'] = self.body

        return result


class SMSQRCode(QRCode):
    """This class is a subclass of QRCode and is used to generate an SMS QR-code element"""
    def __init__(self, name: str, receiver: str, sms_body: str = None):
        super().__init__(name, receiver, 'qr_sms')
        self.sms_body: str = sms_body

    @property
    def _dict_suffixes(self):
        result = super()._dict_suffixes

        if self.sms_body is not None:
            result['_sms_body'] = self.sms_body

        return result


class URLQRCode(QRCode):
    """This class is a subclass of QRCode and is used to generate a URL QR-code element"""
    def __init__(self, name: str, url: str):
        super().__init__(name, url, 'qr_url')


class VCardQRCode(QRCode):
    """This class is a subclass of QRCode and is used to generate a vCard QR-code element"""
    def __init__(self, name: str, first_name: str, last_name: str = None, email: str = None, website: str = None):
        super().__init__(name, first_name, 'qr_vcard')
        self.last_name: str = last_name
        self.email: str = email
        self.website: str = website

    @property
    def _dict_suffixes(self):
        result = super()._dict_suffixes

        if self.last_name is not None:
            result['_vcard_last_name'] = self.last_name
        if self.email is not None:
            result['_vcard_email'] = self.email
        if self.website is not None:
            result['_vcard_website'] = self.website

        return result


class MeCard(QRCode):
    """This class is a subclass of QRCode and is used to generate a MeCard QR-code element"""
    def __init__(
        self,
        name: str,
        first_name: str,
        last_name: str = None,
        nickname: str = None,
        email: str = None,
        contact_primary: str = None,
        contact_secondary: str = None,
        contact_tertiary: str = None,
        website: str = None,
        birthday: str = None,
        notes: str = None
    ):
        super().__init__(name, first_name, 'qr_me_card')
        self.last_name: str = last_name
        self.nickname: str = nickname
        self.email: str = email
        self.contact_primary: str = contact_primary
        self.contact_secondary: str = contact_secondary
        self.contact_tertiary: str = contact_tertiary
        self.website: str = website
        self.birthday: str = birthday
        self.notes: str = notes
    
    @property
    def _dict_suffixes(self):
        result = super()._dict_suffixes

        if self.last_name is not None:
            result['_me_card_last_name'] = self.last_name
        if self.nickname is not None:
            result['_me_card_nickname'] = self.nickname
        if self.email is not None:
            result['_me_card_email'] = self.email
        if self.contact_primary is not None:
            result['_me_card_contact_primary'] = self.contact_primary
        if self.contact_secondary is not None:
            result['_me_card_contact_secondary'] = self.contact_secondary
        if self.contact_tertiary is not None:
            result['_me_card_contact_tertiary'] = self.contact_tertiary
        if self.website is not None:
            result['_me_card_website'] = self.website
        if self.birthday is not None:
            result['_me_card_birthday'] = self.birthday
        if self.notes is not None:
            result['_me_card_notes'] = self.notes

        return result


class GeolocationQRCode(QRCode):
    """This class is a subclass of QRCode and is used to generate a geolocation QR-code element"""
    def __init__(self, name: str, latitude: str, longitude: str = None, altitude: str = None):
        super().__init__(name, latitude, 'qr_geolocation')
        self.longitude: str = longitude
        self.altitude: str = altitude

    @property
    def _dict_suffixes(self):
        result = super()._dict_suffixes

        if self.longitude is not None:
            result['_geolocation_longitude'] = self.longitude
        if self.altitude is not None:
            result['_geolocation_altitude'] = self.altitude

        return result


class EventQRCode(QRCode):
    """This class is a subclass of QRCode and is used to generate an event QR-code element"""
    def __init__(self, name: str, summary: str, startdate: str = None, enddate: str = None):
        super().__init__(name, summary, 'qr_event')
        self.startdate: str = startdate
        self.enddate: str = enddate

    @property
    def _dict_suffixes(self):
        result = super()._dict_suffixes

        if self.startdate is not None:
            result['_event_startdate'] = self.startdate
        if self.enddate is not None:
            result['_event_enddate'] = self.enddate

        return result


class AOPChart(Element):
    def __init__(self,
                 name: str,
                 x_data: Iterable,
                 y_datas: Union[Iterable[Iterable], Mapping[str, Iterable]],
                 title: str = None,
                 x_title: str = None,
                 y_title: str = None,
                 y2_title: str = None,
                 x2_title: str = None):
        super().__init__(name)
        self.x_data: List = list(x_data)

        self.y_datas: Dict[str, Iterable[Union[str, int, float]]] = None
        if isinstance(y_datas, Mapping):
            self.y_datas = {
                name: list(data) for name, data in y_datas.items()
            }
        elif isinstance(y_datas, Iterable):
            self.y_datas = {
                f"series {i+1}": list(data) for i, data in enumerate(y_datas)
            }
        else:
            raise TypeError(
                f'Expected Mapping or Iterable for y_data, got "{type(y_datas)}"')

        self.title: str = title
        self.x_title: str = x_title
        self.y_title: str = y_title
        self.x2_title: str = x2_title
        self.y2_title: str = y2_title

    @classmethod
    def from_dataframe(cls,
                       name: str,
                       data: 'pandas.DataFrame',
                       title: str = None,
                       x_title: str = None,
                       y_title: str = None,
                       y2_title: str = None,
                       x2_title: str = None):
        x_data = list(data.iloc[:, 0])

        y_frame = data.iloc[:, 1:]
        y_datas = {}
        for col_name, col_data in y_frame.iteritems():
            y_datas[col_name] = col_data

        return cls(name, x_data, y_datas, title, x_title, y_title, x2_title, y2_title)

    @property
    def as_dict(self) -> dict:
        result = {
            "xAxis": {
                "data": self.x_data,
            },
            "yAxis": {
                "series": [{
                    "name": name,
                    "data": data
                } for name, data in self.y_datas.items()]
            }
        }

        if self.title is not None:
            result["title"] = self.title
        if self.x_title is not None:
            result["xAxis"]["title"] = self.x_title
        if self.y_title is not None:
            result["yAxis"]["title"] = self.y_title
        if self.x2_title is not None:
            result['x2Axis'] = {}
            result["x2Axis"]["title"] = self.x2_title
        if self.y2_title is not None:
            result['y2Axis'] = {}
            result["y2Axis"]["title"] = self.y2_title

        return {self.name: result}

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{aopchart " + self.name + "}"})


class Object(list, Element):
    """A collection used to group multiple elements together.
    It can contain nested `Object`s and should be used to pass multiple `Element`s as PrintJob data, as well as to allow for nested elements.
    Its name is used as a key name when nested, but ignored for all purposes when it's the outer object.
    """
    # Object inherits from list, which may look odd or overkill (why not set, tuple ...?).
    # It's because we need it to be mutable and also to be able to contain itself.
    # A tuple is not mutable.
    # A set is mutable but needs its contents to be hashable. A set itself is not hashable, so it cannot contain other sets.
    def __init__(self, name: str = "", elements: Iterable[Element] = ()):
        # name is not used for the outer object, but needed for nested objects
        list.__init__(self, elements)
        Element.__init__(self, name)

    def __str__(self):
        return self.json

    def __repr__(self):
        return self.json

    def copy(self):
        return self.__class__(self)

    def deepcopy(self):
        return deepcopy(self)

    @property
    def json(self):
        return json.dumps(self.as_dict)

    def add(self, element: Element):
        self.append(element)

    # The reason we use 'Object' (a string) in cases like this is that
    # Object is actually a forward reference here,
    # which doesn't work, the interpreter will have no idea what Object is.
    # It is supposed to work out of the box in future Python (>= 3.10)
    # and with >= 3.7 using "from __future__ import annotations"
    def add_all(self, obj: 'Object'):
        for element in obj:
            self.add(element)

    def remove_element_by_name(self, element_name: str):
        self.remove(
            next(element for element in self if element.name == element_name)
        )

    @property
    def as_dict(self) -> dict:
        """Merge the `Object`'s contents as one dict.

        Returns:
            dict: merged element
        """
        result = {}
        for element in self:
            if isinstance(element, Object):
                result.update({element.name: element.as_dict})
            else:
                result.update(element.as_dict)
        return result

    @property
    def available_tags(self) -> FrozenSet[str]:
        result = set()
        for element in self:
            result |= element.available_tags
        return frozenset(result)

    @classmethod
    def element_to_object(cls, element: Element, name: str = "") -> 'Object':
        return cls.from_mapping(element.as_dict, name)

    @classmethod
    def from_mapping(cls, mapping: Mapping, name: str = "") -> 'Object':
        result_set = set()
        for key, value in mapping.items():
            result_set.add(Property(key, value))
        return cls(name, result_set)

    @classmethod
    def from_json(cls, json_str: str, name: str = "") -> 'Object':
        return cls.from_mapping(json.loads(json_str), name)
