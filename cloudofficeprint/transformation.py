from typing import Optional

class TransformationFunction:
    """
   Represents a transformation function for Cloud Office Print (AOP).
    Args:
        js_code (str, optional): Inline JavaScript code for transformation.
        filename (str, optional): Filename from AOP's `assets/transformation_function/` directory.
    """

    def __init__(
        self,
        js_code: Optional[str] = None,
        filename: Optional[str] = None
    ):
        self._js_code: Optional[str] = None
        self._filename: Optional[str] = None

        if js_code is not None:
            self.js_code = js_code
        if filename is not None:
            self.filename = filename

    @property
    def js_code(self) -> Optional[str]:
        return self._js_code

    @js_code.setter
    def js_code(self, code: str):
        if self._filename is not None:
            raise ValueError("Cannot set js_code when filename is already set")
        if not isinstance(code, str) or not code.strip():
            raise ValueError("js_code must be a non‑empty string")
        self._js_code = code

    @property
    def filename(self) -> Optional[str]:
        return self._filename

    @filename.setter
    def filename(self, name: str):
        if self._js_code is not None:
            raise ValueError("Cannot set filename when js_code is already set")
        if not isinstance(name, str) or not name.lower().endswith(".js"):
            raise ValueError("Filename must be a string ending with '.js'")
        if "/" in name or "\\" in name:
            raise ValueError("Filename must not include any path separators")
        self._filename = name

    def as_dict(self) -> Optional[str]:
        """
        Return the transformation_function
        """
        return self._js_code or self._filename
