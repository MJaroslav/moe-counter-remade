import base64
import hashlib
import re

import magic


def get_image_dimensions(file):
    data = magic.from_file(file)
    return tuple(map(int, re.search(r'(\d+) x (\d+)', data).groups()))


def get_mime_type(file):
    return magic.from_file(file, mime=True)


def to_base64(file, charset="UTF-8"):
    with open(file, "rb") as file:
        return base64.b64encode(file.read()).decode(charset)


def trim_and_str_number(number: int, max_length: int = 0, lead_zeros: bool = True):
    number = str(number)
    if max_length > 0:
        number = number[-max_length:]
        if lead_zeros:
            number = "0" * max(max_length - len(number), 0) + number
    return number


def hash_password(password, salt):
    return hashlib.sha1(password.encode("UTF-8") + salt.encode("UTF-8")).hexdigest()
