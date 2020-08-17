from typing import Union
import json


class PDFOptions:
    """Class of optional PDF options.

    The properties of this class define all possible PDF output options.
    All of them are optional, which is why passing an instance of this class in an OutputConfig is also optional.

    The getters for the properties return the value the server uses as default value if the value is set to None.
    These default values are not passed to the json or dict representation of the object and thus not explicitly sent to the AOP server.
    """

    _even_page = None
    _merge_making_even = None
    _read_password = None
    _modify_password = None
    _password_protection_flag = None
    _watermark = None
    _lock_form = None
    _copies = None
    _page_margin = None
    _landscape = False
    _page_width = None
    _page_height = None
    _page_format = None
    _merge = None

    def __str__(self):
        return self.json

    @property
    def json(self) -> str:
        """Get the json representation of these PDF options.

        The json representation is a direct json dump of the dict representation.
        The dict representation is accessed through the as_dict property.

        Returns:
            str: json string
        """
        return json.dumps(self.as_dict)

    @property
    def as_dict(self) -> dict:
        """Get the dict representation of these PDF options.

        Returns:
            dict: options as dict
        """
        result = {}
        if self._even_page is not None:
            result["output_even_page"] = self._even_page
        if self._merge_making_even is not None:
            result["output_merge_making_even"] = self._merge_making_even
        if self._modify_password is not None:
            result["output_modify_password"] = self._modify_password
        if self._read_password is not None:
            result["output_read_password"] = self._read_password
        if self._password_protection_flag is not None:
            result["output_password_protection_flag"] = self._password_protection_flag
        if self._watermark is not None:
            result["output_watermark"] = self._watermark
        if self._lock_form is not None:
            result["lock_form"] = self._lock_form
        if self._copies is not None:
            result["output_copies"] = self._copies
        if self.page_margin is not None:
            if isinstance(self._page_margin, dict):
                for pos, value in self._page_margin.items():
                    result[f"output_page_margin_{pos}"] = value
            else:
                result["output_page_margin"] = self._page_margin
        if self._page_width is not None:
            result["output_page_width"] = self._page_width
        if self._page_height is not None:
            result["output_page_height"] = self._page_height
        if self._page_format is not None:
            result["output_page_format"] = self._page_format
        if self._merge is not None:
            result["output_merge"] = self._merge

    @property
    def even_page(self) -> bool:
        """If you want your output to have even pages, for example printing on both sides after merging, you can set this to be true.

        Returns:
            bool: even_page
        """
        return False if self._even_page is None else self._even_page

    @even_page.setter
    def even_page(self, value: bool):
        # set to None instead of False to omit from the json
        self._even_page = True if value else None

    @property
    def merge_making_even(self) -> bool:
        """Merge each given document making even paged.

        Returns:
            bool: merge_making_even
        """
        return False if self._merge_making_even is None else self._merge_making_even

    @merge_making_even.setter
    def merge_making_even(self, value: bool):
        self._merge_making_even = True if value else None

    @property
    def read_password(self) -> str:
        """The password needed to open the PDF.

        Returns:
            str: read_password
        """
        return self._read_password

    @read_password.setter
    def read_password(self, value: str):
        self._read_password = value

    @property
    def modify_password(self) -> str:
        """The password needed to modify the PDF.

        Returns:
            str: modify_password
        """
        return self.read_password if self._modify_password is None else self._modify_password

    @modify_password.setter
    def modify_password(self, value: str):
        self._modify_password = value

    @property
    def password_protection_flag(self) -> int:
        """Bit field explained in the PDF specs in table 3.20 in section 3.5.2, should be given as an integer.

        [more info](https://pdfhummus.com/post/147451287581/hummus-1058-and-pdf-writer-updates-encryption)

        Returns:
            int: password_protection_flag
        """
        return 4 if self._password_protection_flag is None else self._password_protection_flag

    @password_protection_flag.setter
    def password_protection_flag(self, value: int):
        self._password_protection_flag = int(value)

    @property
    def watermark(self) -> str:
        """Setting this generates a diagonal custom watermark on every page in the PDF file

        Returns:
            str: watermark
        """
        return self._watermark

    @watermark.setter
    def watermark(self, value: str):
        self._watermark = value

    @property
    def lock_form(self) -> bool:
        """Locks / flattens the forms in the PDF.

        Returns:
            bool: lock_form
        """
        return False if self._lock_form is None else self._lock_form

    @lock_form.setter
    def lock_form(self, value: bool):
        self._lock_form = True if value else None

    @property
    def copies(self) -> int:
        """Repeats the output pdf for the given number of times.

        Returns:
            int: copies
        """
        return self._copies

    @copies.setter
    def copies(self, value: int):
        self._copies = int(value)

    @property
    def page_margin(self) -> Union[int, dict]:
        """Margin in px.

        Returns either a dict containing:
        {
            "top": int,
            "bottom": int,
            "left": int,
            "right": int
        }
        or just an int to be used on all sides.

        Returns:
            Union[int, dict]: page_margin
        """
        return self._page_margin

    def set_page_margin_at(self, value: int, position: str = None):
        """Set page_margin

        Either set the position for all margin positions (if position is None) or set a specific one.
        The setter for the page_margin property sets the margin for all positions.

        Args:
            value (int): page margin
            position (str, optional): "top", "bottom", "left" or "right". Defaults to None.
        """
        if position is not None:
            if isinstance(self._page_margin, dict):
                # page margin is already a dict, add/change this position
                self._page_margin[position] = value
            elif self._page_margin is None:
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

    @page_margin.setter
    def page_margin(self, value: int):
        self.set_page_margin_at(value, position = None)

    @property
    def page_orientation(self) -> str:
        """The page orientation, portrait or landscape.

        Returns:
            str: page_orientation
        """
        return "landscape" if self._landscape else "portrait"

    @page_orientation.setter
    def page_orientation(self, value: str):
        self._landscape = True if value is "landscape" else False

    @property
    def page_width(self) -> Union[str, int]:
        """Page width in px, mm, cm, in. No unit means px.

        Returns:
            Union[str, int]: page_width
        """
        return self._page_width

    @page_width.setter
    def page_width(self, value: Union[str, int]):
        self._page_width = value

    @property
    def page_height(self):
        """Page height in px, mm, cm, in. No unit means px.

        Returns:
            Union[str, int]: page_height
        """
        return self._page_height

    @page_height.setter
    def page_height(self, value: Union[str, int]):
        self._page_height = value

    @property
    def page_format(self) -> str:
        """The page format: "a4" (default) or "letter"

        Returns:
            str: page_format
        """
        return "a4" if self._page_format is None else self._page_format

    @page_format.setter
    def page_format(self, value: str):
        self._page_format = value

    @property
    def merge(self) -> bool:
        """If True: instead of returning back a zip file for multiple output, merge it.

        Returns:
            bool: merge
        """
        return False if self._merge is None else self._merge

    @merge.setter
    def merge(self, value: bool):

        self._merge = value
