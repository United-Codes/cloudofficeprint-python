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

# TODO: update docs

def path_to_extension(file_path: str) -> str:
    return path.splitext(file_path)[1][1:]

def extension_to_mimetype(ext):
    """
    Map an extension to a mime type.
    """
    # append "a." because mimetypes can handle a format like "filename.extension", but not just "extension"
    return mimetypes.guess_type(f"a.{ext}")[0]


def mimetype_to_extension(mimetype):
    """
    Map a mime type to an extension.
    """
    # mimetypes returns a string in ".extension", so we strip off the first character
    return mimetypes.guess_extension(mimetype)[1:]
