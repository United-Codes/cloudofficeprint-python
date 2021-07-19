from typing import Dict, FrozenSet, Union
from .elements import Element

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
    def as_dict(self) -> Dict:
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
    def __init__(self, name: str, data: str, type: str):
        super().__init__(name, data, type)

        self.dotscale: float = None
        """For body block, must be greater than 0, less than or equal to 1. default is 1"""
        self.logo: str = None
        """Logo Image (At center of QR)"""
        self.background_image: str = None
        """Background Image"""
        self.color_dark: str = None
        self.color_light: str = None
        self.logo_width: Union[str, int] = None
        """Width of logo"""
        self.logo_height: Union[str, int] = None
        """Height of logo"""
        self.logo_background_color: str = None
        self.quiet_zone: int = None
        """For padding around qr code"""
        self.quiet_zone_color: str = None
        """Color of padding area"""
        self.background_image_alpha: float = None
        """Background image transparency, value between 0 and 1. default is 1"""
        self.po_color: str = None
        """Global Position Outer color. if not set, the defaut is `colorDark`"""
        self.pi_color: str = None
        """Global Pisotion Inner color. if not set, the defaut is `colorDark`"""
        self.po_tl_color: str = None
        """Position Outer color - Top Left """
        self.pi_tl_color: str = None
        """Position Inner color - Top Left"""
        self.po_tr_color: str = None
        """Position Outer color - Top Right"""
        self.pi_tr_color: str = None
        """Position Inner color - Top Right"""
        self.po_bl_color: str = None
        """Position Outer color - Bottom Left"""
        self.pi_bl_color: str = None
        """Position Inner color - Bottom Left"""
        self.timing_v_color: str = None
        """Vertical timing color"""
        self.timing_h_color: str = None
        """Horizontal timing color"""
        self.timing_color: str = None
        """Global Timing color. if not set"""
        self.auto_color: bool = None
        """Automatic color adjustment(for data block) (default is false) (set to false if using background images)"""
        self.auto_color_dark: str = None
        """Automatic color: dark CSS color (only required when qr_auto_color is set true) (dark color prefered, otherwise may lead to undetectable QR)"""
        self.auto_color_light: str = None
        """Automatic color: light CSS color (only required when qr_auto_color is set true)"""
    
    def set_dotscale(self, dotscale: float):
        self.dotscale = dotscale
    def set_logo(self, logo: str):
        self.logo = logo
    def set_background_image(self, background_image: str):
        self.background_image = background_image
    def set_color_dark(self, color_dark: str):
        self.color_dark = color_dark
    def set_color_light(self, color_light: str):
        self.color_light = color_light
    def set_logo_width(self, logo_width: Union[str, int]):
        self.logo_width = logo_width
    def set_logo_height(self, logo_height: Union[str, int]):
        self.logo_height = logo_height
    def set_logo_background_color(self, logo_background_color: str):
        self.logo_background_color = logo_background_color
    def set_quiet_zone(self, quiet_zone: int):
        self.quiet_zone = quiet_zone
    def set_quiet_zone_color(self, quiet_zone_color: str):
        self.quiet_zone_color = quiet_zone_color
    def set_background_image_alpha(self, background_image_alpha: float):
        self.background_image_alpha = background_image_alpha
    def set_po_color(self, po_color: str):
        self.po_color = po_color
    def set_pi_color(self, pi_color: str):
        self.pi_color = pi_color
    def set_po_tl_color(self, po_tl_color: str):
        self.po_tl_color = po_tl_color
    def set_pi_tl_color(self, pi_tl_color: str):
        self.pi_tl_color = pi_tl_color
    def set_po_tr_color(self, po_tr_color: str):
        self.po_tr_color = po_tr_color
    def set_pi_tr_color(self, pi_tr_color: str):
        self.pi_tr_color = pi_tr_color
    def set_po_bl_color(self, po_bl_color: str):
        self.po_bl_color = po_bl_color
    def set_pi_bl_color(self, pi_bl_color: str):
        self.pi_bl_color = pi_bl_color
    def set_timing_v_color(self, timing_v_color: str):
        self.timing_v_color = timing_v_color
    def set_timing_h_color(self, timing_h_color: str):
        self.timing_h_color = timing_h_color
    def set_timing_color(self, timing_color: str):
        self.timing_color = timing_color
    def set_auto_color(self, auto_color: bool):
        self.auto_color = auto_color
    def set_auto_color_dark(self, auto_color_dark: str):
        self.auto_color_dark = auto_color_dark
    def set_auto_color_light(self, auto_color_light: str):
        self.auto_color_light = auto_color_light


    @property
    def _dict_suffixes(self):
        result = super()._dict_suffixes

        if self.dotscale is not None:
            result['_dotscale'] = self.dotscale
        if self.logo is not None:
            result['_logo'] = self.logo
        if self.background_image is not None:
            result['_background_image'] = self.background_image
        if self.color_dark is not None:
            result['_color_dark'] = self.color_dark
        if self.color_light is not None:
            result['_color_light'] = self.color_light
        if self.logo_width is not None:
            result['_logo_width'] = self.logo_width
        if self.logo_height is not None:
            result['_logo_height'] = self.logo_height
        if self.logo_background_color is not None:
            result['_logo_background_color'] = self.logo_background_color
        if self.quiet_zone is not None:
            result['_quiet_zone'] = self.quiet_zone
        if self.quiet_zone_color is not None:
            result['_quiet_zone_color'] = self.quiet_zone_color
        if self.background_image_alpha is not None:
            result['_background_image_alpha'] = self.background_image_alpha
        if self.po_color is not None:
            result['_po_color'] = self.po_color
        if self.pi_color is not None:
            result['_pi_color'] = self.pi_color
        if self.po_tl_color is not None:
            result['_po_tl_color'] = self.po_tl_color
        if self.pi_tl_color is not None:
            result['_pi_tl_color'] = self.pi_tl_color
        if self.po_tr_color is not None:
            result['_po_tr_color'] = self.po_tr_color
        if self.pi_tr_color is not None:
            result['_pi_tr_color'] = self.pi_tr_color
        if self.po_bl_color is not None:
            result['_po_bl_color'] = self.po_bl_color
        if self.pi_bl_color is not None:
            result['_pi_bl_color'] = self.pi_bl_color
        if self.timing_v_color is not None:
            result['_timing_v_color'] = self.timing_v_color
        if self.timing_h_color is not None:
            result['_timing_h_color'] = self.timing_h_color
        if self.timing_color is not None:
            result['_timing_color'] = self.timing_color
        if self.auto_color is not None:
            result['_auto_color'] = self.auto_color
        if self.auto_color_dark is not None:
            result['_auto_color_dark'] = self.auto_color_dark
        if self.auto_color_light is not None:
            result['_auto_color_light'] = self.auto_color_light

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