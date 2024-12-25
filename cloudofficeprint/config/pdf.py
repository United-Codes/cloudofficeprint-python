import json
from typing import Union, Dict, Mapping

from ..resource import Base64Resource, ServerPathResource, URLResource


class PDFOptions:
    """Class of optional PDF options.

    The properties of this class define all possible PDF output options.
    All of them are optional, which is why passing an instance of this class in an OutputConfig is also optional.
    """

    def __init__(
        self,
        even_page: bool = None,
        merge_making_even: bool = None,
        remove_last_page: bool = None,
        modify_password: str = None,
        read_password: str = None,
        password_protection_flag: int = None,
        watermark: str = None,
        watermark_color: str = None,
        watermark_font: str = None,
        watermark_opacity: int = None,
        watermark_size: int = None,
        lock_form: bool = None,
        copies: int = None,
        page_margin: Union[int, dict] = None,
        landscape: bool = None,
        page_width: Union[str, int] = None,
        page_height: Union[str, int] = None,
        page_format: str = None,
        merge: bool = None,
        split: bool = None,
        identify_form_fields: bool = None,
        sign_certificate: str = None,
        sign_certificate_password: str = None,
        sign_certificate_txt: str = None,
        convert_to_pdfa: str = None,
        
    ):
        """
        Args:
            even_page (bool, optional): If you want your output to have even pages, for example printing on both sides after merging, you can set this to be true. Defaults to None.
            merge_making_even (bool, optional): Merge each given document making even paged. Defaults to None.
            remove_last_page (bool, optional): Remove the last page from the given PDF document. Defaults to None.
            modify_password (str, optional): The password needed to modify the PDF. Defaults to None.
            read_password (str, optional): The password needed to open the PDF. Defaults to None.
            password_protection_flag (int, optional): Bit field explained in the PDF specs in table 3.20 in section 3.5.2, should be given as an integer. [More info](https://pdfhummus.com/post/147451287581/hummus-1058-and-pdf-writer-updates-encryption). Defaults to None.
            watermark (str, optional): Requires PDF output, generates a diagonal custom watermark on every page of the PDF file. Defaults to None.
            watermark_color (str, optional): Requires PDF output, specifies the font of the watermark specified, with a default of "black". Defaults to None.
            watermark_font (str, optional): Requires PDF output, specifies the font of the watermark text specified, with a default of "Arial". Defaults to None.
            watermark_opacity (int, optional): Requires PDF output, specifies the opacity of the watermark text specified, should be as a percentage, i.e. 45. Defaults to None.
            watermark_size (int, optional): Requires PDF output, specifies the size of watermark text specified, should be a number in px, i.e. 45. Defaults to None.
            lock_form (bool, optional): Locks / flattens the forms in the PDF. Defaults to None.
            copies (int, optional): Repeats the output pdf for the given number of times. Defaults to None.
            page_margin (Union[int, dict], optional): Only for HTML to PDF. Margin in px. Returns either a dict containing: { "top": int, "bottom": int, "left": int, "right": int } or just an int to be used on all sides. Defaults to None.
            landscape (bool, optional): Only for HTML to PDF. If True: the orientation of the output file is landscape; else portrait (default). Defaults to None.
            page_width (Union[str, int], optional): Only for HTML to PDF. Page width in px, mm, cm, in. No unit means px. Defaults to None.
            page_height (Union[str, int], optional): Only for HTML to PDF. Page height in px, mm, cm, in. No unit means px. Defaults to None.
            page_format (str, optional): Only for HTML to PDF. The page format: "a4" (default) or "letter". Defaults to None.
            merge (bool, optional): If True: instead of returning back a zip file for multiple output, merge it. Defaults to None.
            split (bool, optional): You can specify to split a PDF in separate files. You will get one file per page in a zip file. Defaults to None.
            identify_form_fields (bool, optional): Identify the form fields in a PDF-form by filling the name of each field into the respective field. Defaults to None.
            sign_certificate (str, optional): Signing certificate for the output PDF (pkcs #12 .p12/.pfx) as a base64 string, URL, FTP location or a server path. The function read_file_as_base64() from file_utils.py can be used to read local .p12 or .pfx file as base64. Defaults to None.
            sign_certificate_password (str, optional): If you are signing with a password protected certificate, you can specify the password as a plain string. Defaults to None.
            sign_certificate_txt (str, optional) Add custom text in any language to the signature field
            convert_to_pdfa (str, optional): For generating PDF/A format. While converting using openoffice converter, specifying it will create PDF/A format, values can be either 1b or 2b which are the variants of PDF/A specification.
        """
        self.even_page: bool = even_page
        self.merge_making_even: bool = merge_making_even
        self.remove_last_page: bool = remove_last_page
        self.modify_password: str = modify_password
        self.read_password: str = read_password
        self.password_protection_flag: int = password_protection_flag
        self.watermark: str = watermark
        self.watermark_color: str = watermark_color
        self.watermark_font: str = watermark_font
        self.watermark_opacity: int = watermark_opacity
        self.watermark_size: int = watermark_size
        self.lock_form: bool = lock_form
        self.copies: int = copies
        self.page_margin: Union[int, dict] = page_margin
        self._landscape: bool = landscape
        self.page_width: Union[str, int] = page_width
        self.page_height: Union[str, int] = page_height
        self.page_format: str = page_format
        self.merge: bool = merge
        self.split: bool = split
        self.identify_form_fields: bool = identify_form_fields
        self.sign_certificate: str = sign_certificate
        self.sign_certificate_password: str = sign_certificate_password
        self.sign_certificate_txt: str = sign_certificate_txt
        self.convert_to_pdfa: str = convert_to_pdfa

    def __str__(self) -> str:
        """Get the string representation of these PDF options.

        Returns:
            str: string representation of these PDF options
        """
        return self.json

    @property
    def json(self) -> str:
        """The JSON representation of these PDF options.

        The JSON representation is a direct JSON dump of the dict representation.
        The dict representation is accessed through the `as_dict` property.

        Returns:
            str: JSON representation of these PDF options
        """
        return json.dumps(self.as_dict)

    @property
    def as_dict(self) -> Dict:
        """The dict representation of these PDF options.

        Returns:
            Dict: the dict representation of these PDF options
        """
        result = {}

        if self.even_page is not None:
            result["output_even_page"] = self.even_page
        if self.merge_making_even is not None:
            result["output_merge_making_even"] = self.merge_making_even
        if self.remove_last_page is not None:
            result["output_remove_last_page"] = self.remove_last_page
        if self.modify_password is not None:
            result["output_modify_password"] = self.modify_password
        if self.read_password is not None:
            result["output_read_password"] = self.read_password
        if self.password_protection_flag is not None:
            result["output_password_protection_flag"] = self.password_protection_flag
        if self.watermark is not None:
            result["output_watermark"] = self.watermark
        if self.watermark_color is not None:
            result["output_watermark_color"] = self.watermark_color
        if self.watermark_font is not None:
            result["output_watermark_font"] = self.watermark_font
        if self.watermark_opacity is not None:
            result["output_watermark_opacity"] = self.watermark_opacity
        if self.watermark_size is not None:
            result["output_watermark_size"] = self.watermark_size
        if self.lock_form is not None:
            result["lock_form"] = self.lock_form
        if self.copies is not None:
            result["output_copies"] = self.copies
        if self.page_margin is not None:
            # For Cloud Office Print versions later than 21.1.1, output_page_margin will also be supported
            result["page_margin"] = self.page_margin
        if self._landscape is not None:
            # For Cloud Office Print versions later than 21.1.1, output_page_orientation will also be supported
            result["page_orientation"] = self.page_orientation
        if self.page_width is not None:
            result["output_page_width"] = self.page_width
        if self.page_height is not None:
            result["output_page_height"] = self.page_height
        if self.page_format is not None:
            result["output_page_format"] = self.page_format
        if self.merge is not None:
            result["output_merge"] = self.merge
        if self.split is not None:
            result["output_split"] = self.split
        if self.identify_form_fields is not None:
            result["identify_form_fields"] = self.identify_form_fields
        if self.sign_certificate is not None:
            result["output_sign_certificate"] = self.sign_certificate
        if self.sign_certificate_password is not None:
            result["output_sign_certificate_password"] = self.sign_certificate_password
        if self.sign_certificate_txt is not None:
            result["output_sign_certificate_txt"] = self.sign_certificate_txt
        if self.convert_to_pdfa is not None:
            result["output_convert_to_pdfa"] = self.convert_to_pdfa

        return result

    def set_watermark(
        self,
        text: str = None,
        color: str = None,
        font: str = None,
        opacity: int = None,
        size: int = None,
    ):
        """Set watermark

        Set a diagonal custom watermark on every page in the PDF file with a specific text, color, font, opacity and size.
        Setting all to None will remove the watermark.

        Args:
            text (str, optional): Requires PDF output, generates a diagonal custom watermark on every page of the PDF file. Defaults to None.
            color (str, optional): Requires PDF output, specifies the font of the watermark specified, with a default of "black". Defaults to None.
            font (str, optional): Requires PDF output, specifies the font of the watermark text specified, with a default of "Arial". Defaults to None.
            opacity (int, optional): Requires PDF output, specifies the opacity of the watermark text specified, should be as a percentage, i.e. 45. Defaults to None.
            size (int, optional): Requires PDF output, specifies the size of watermark text specified, should be a number in px, i.e. 45. Defaults to None.
        """
        self.watermark = text
        self.watermark_color = color
        self.watermark_font = font
        self.watermark_opacity = opacity
        self.watermark_size = size

    def set_page_margin_at(self, value: int, position: str = None):
        """Set page_margin

        Either set the position for all margin positions (if position is None) or set a specific one.

        Args:
            value (int): page margin in px
            position (str, optional): "all", "top", "bottom", "left" or "right". Defaults to None.
        """
        if position is not None:
            if isinstance(self.page_margin, Mapping):
                # page margin is already a dict, add/change this position
                self.page_margin[position] = value
            elif self.page_margin is None:
                # page margin not yet defined, set it to a dict with this position defined
                self.page_margin = {position: value}
            else:
                # page margin defined but no dict, convert to dict first
                current = self.page_margin
                self.page_margin = {
                    "top": current,
                    "bottom": current,
                    "left": current,
                    "right": current,
                }
                self.page_margin[position] = value
        else:
            self.page_margin = value

    @property
    def page_orientation(self) -> str:
        """The page orientation, portrait or landscape.

        Returns:
            str: the page orientation, portrait or landscape
        """
        return "landscape" if self._landscape else "portrait"

    @page_orientation.setter
    def page_orientation(self, value: str):
        """Setter for the page orientation.

        Args:
            value (str): the page orientation
        """
        self._landscape = value == "landscape"

    def sign(
        self,
        certificate: Union[Base64Resource, ServerPathResource, URLResource],
        password: str = None,
    ):
        """Sign the output PDF with a certificate file.

        Args:
            certificate (str): Resource of the certificate file.
            password (str): password of the certificate. Defaults to None.
        """
        self.sign_certificate = certificate.data
        self.sign_certificate_password = password
