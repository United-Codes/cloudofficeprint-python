import json
from typing import Union, Iterable, Dict, Mapping

class PDFOptions:
    """Class of optional PDF options.

    The properties of this class define all possible PDF output options.
    All of them are optional, which is why passing an instance of this class in an OutputConfig is also optional.

    The getters for the properties return the value the server uses as default value if the value is set to None.
    These default values are not passed to the json or dict representation of the object and thus not explicitly sent to the AOP server.
    """

    def __init__(self,
                 read_password: str = None,
                 watermark: str = None,
                 page_width: Union[str, int] = None,
                 page_height: Union[str, int] = None,
                 even_page: bool = None,
                 merge_making_even: bool = None,
                 modify_password: str = None,
                 password_protection_flag: int = None,
                 lock_form: bool = None,
                 copies: int = None,
                 page_margin: Union[int, dict] = None,
                 landscape: bool = None,
                 page_format: str = None,
                 merge: bool = None,
                 sign_certificate: str = None):
        """
        Args:
            read_password (str, optional): `PDFOptions.read_password`. Defaults to None.
            watermark (str, optional): `PDFOptions.watermark`. Defaults to None.
            page_width (Union[str, int], optional): `PDFOptions.page_width`. Defaults to None.
            page_height (Union[str, int], optional): `PDFOptions.page_height`. Defaults to None.
            even_page (bool, optional): `PDFOptions.even_page`. Defaults to None.
            merge_making_even (bool, optional): `PDFOptions.merge_making_even`. Defaults to None.
            modify_password (str, optional): `PDFOptions.modify_password`. Defaults to None.
            password_protection_flag (int, optional): `PDFOptions.password_protection_flag`. Defaults to None.
            lock_form (bool, optional): `PDFOptions.lock_form`. Defaults to None.
            copies (int, optional): `PDFOptions.copies`. Defaults to None.
            page_margin (Union[int, dict], optional): `PDFOptions.page_margin`. Defaults to None.
            landscape (bool, optional): Whether the document should be in landscape orientation, affects `PDFOptions.page_orientation`. Defaults to None.
            page_format (str, optional): `PDFOptions.page_format`. Defaults to None.
            merge (bool, optional): `PDFOptions.merge`. Defaults to None.
            sign_certificate (str, optional): `PDFOptions.sign_certificate`. Defaults to None.
        """
        self.read_password: str = None
        """The password needed to open the PDF."""
        self.watermark: str = None
        """Setting this generates a diagonal custom watermark on every page in the PDF file"""
        self.page_width: Union[str, int] = None
        """Page width in px, mm, cm, in. No unit means px."""
        self.page_height: Union[str, int] = None
        """Page height in px, mm, cm, in. No unit means px."""

        self.even_page: bool = even_page
        """If you want your output to have even pages, for example printing on both sides after merging, you can set this to be true."""
        self.merge_making_even: bool = merge_making_even
        """Merge each given document making even paged."""
        self.modify_password: str = modify_password
        """The password needed to modify the PDF."""
        self.password_protection_flag: int = password_protection_flag
        """Bit field explained in the PDF specs in table 3.20 in section 3.5.2, should be given as an integer.

        [More info.](https://pdfhummus.com/post/147451287581/hummus-1058-and-pdf-writer-updates-encryption)
        """
        self.lock_form = lock_form
        """Locks / flattens the forms in the PDF."""
        self.copies = copies
        """Repeats the output pdf for the given number of times."""
        self.page_format = page_format
        """The page format: "a4" (default) or "letter"."""
        self.merge = merge
        """If True: instead of returning back a zip file for multiple output, merge it."""
        self.page_margin = page_margin
        """Margin in px.

        Returns either a dict containing:
        ```python
        {
            "top": int,
            "bottom": int,
            "left": int,
            "right": int
        }
        ```
        or just an int to be used on all sides."""
        self.sign_certificate: str = sign_certificate
        """Signing certificate for the output PDF (pkcs #12 .p12/.pfx) as a base64 string, URL, FTP location or a server path."""

        self._landscape = landscape

    def __str__(self):
        return self.json

    @property
    def json(self) -> str:
        """The json representation of these PDF options.

        The json representation is a direct json dump of the dict representation.
        The dict representation is accessed through the `as_dict` property.
        """
        return json.dumps(self.as_dict)

    @property
    def as_dict(self) -> dict:
        """The dict representation of these PDF options."""
        result = {}

        if self.even_page is not None:
            result["output_even_page"] = self.even_page
        if self.merge_making_even is not None:
            result["output_merge_making_even"] = self.merge_making_even
        if self.modify_password is not None:
            result["output_modify_password"] = self.modify_password
        if self.read_password is not None:
            result["output_read_password"] = self.read_password
        if self.password_protection_flag is not None:
            result["output_password_protection_flag"] = self.password_protection_flag
        if self.watermark is not None:
            result["output_watermark"] = self.watermark
        if self.lock_form is not None:
            result["lock_form"] = self.lock_form
        if self.copies is not None:
            result["output_copies"] = self.copies
        if self.page_margin is not None:
            if isinstance(self._page_margin, dict):
                for pos, value in self._page_margin.items():
                    result[f"output_page_margin_{pos}"] = value
            else:
                result["output_page_margin"] = self._page_margin
        if self.page_width is not None:
            result["output_page_width"] = self.page_width
        if self.page_height is not None:
            result["output_page_height"] = self.page_height
        if self.page_format is not None:
            result["output_page_format"] = self.page_format
        if self.merge is not None:
            result["output_merge"] = self.merge

        return result

    def set_page_margin_at(self, value: int, position: str = None):
        """Set page_margin

        Either set the position for all margin positions (if position is None) or set a specific one.
        The setter for the page_margin property sets the margin for all positions.

        Args:
            value (int): page margin
            position (str, optional): "all", "top", "bottom", "left" or "right". Defaults to None.
        """
        if position is not None:
            if isinstance(self.page_margin, Mapping):
                # page margin is already a dict, add/change this position
                self.page_margin[position] = value
            elif self.page_margin is None:
                # page margin not yet defined, set it to a dict with this position defined
                self._page_margin = {
                    position: value
                }
            else:
                # page margin defined but no dict, convert to dict first
                current = self._page_margin
                self._page_margin = {
                    "top": current,
                    "bottom": current,
                    "left": current,
                    "right": current
                }
                self._page_margin[position] = value
        else:
            self._page_margin = value

    @property
    def page_orientation(self) -> str:
        """The page orientation, portrait or landscape."""
        return "landscape" if self._landscape else "portrait"

    @page_orientation.setter
    def page_orientation(self, value: str):
        self._landscape = True if value == "landscape" else False
