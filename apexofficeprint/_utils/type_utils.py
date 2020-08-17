import mimetypes
from os import path

supported_resource_types = [
    "txt",
    "md",
    "html",
    "docx",
    "xlsx",
    "pptx",
]


def path_to_extension(file_path: str) -> str:
    """Cut off the extension from a file path.

    Example: "/path/to/file.docx" -> "docx"

    Args:
        file_path (str): file path to handle

    Returns:
        str: the file's file type / extension
    """
    return path.splitext(file_path)[1][1:]


def extension_to_mimetype(ext: str) -> str:
    """Map an extension / file type to a mime type.

    Args:
        ext (str): extension

    Returns:
        str: mime type corresponding to the extension
    """
    # append "a." because mimetypes can handle a format like "filename.extension", but not just "extension"
    return mimetypes.guess_type(f"a.{ext}")[0]


def mimetype_to_extension(mimetype: str) -> str:
    """Map a mime type to an extension / file type.

    Args:
        mimetype (str): mime type

    Returns:
        str: file type / extension corresponding to the mime type
    """
    # mimetypes returns a string in ".extension", so we strip off the first character
    return mimetypes.guess_extension(mimetype)[1:]
