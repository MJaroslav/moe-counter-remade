import magic
import os
import base64
import re
import math


__themes__ = {}
__image__ = """<?xml version="1.0" encoding="UTF-8"?>
            <svg width="{}" height="{}" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                <title>Moe Count</title>
                <g>
                    {}
                </g>
            </svg>
            """


def __get_image_size__(file):
    data = magic.from_file(file)
    return re.search('(\d+) x (\d+)', data).groups()


def __get_mime__(file):
    return magic.from_file(file, mime=True)


def __to_base64__(file):
    with open(file, "rb") as file:
        return base64.b64encode(file.read()).decode('ascii')


def __load_themes__():
    for theme in os.listdir("./assets/theme/"):
        for file in os.listdir("./assets/theme/" + theme + "/"):
            path = "./assets/theme/" + theme + "/" + file
            name = os.path.splitext(file)[0]
            size = __get_image_size__(path)
            data = "data:{};base64,{}".format(__get_mime__(path), __to_base64__(path))
            if theme not in __themes__: __themes__[theme] = {}
            __themes__[theme][name] = {"width": int(size[0]), "height": int(size[1]), "data": data}

__load_themes__()


def get_count_image(count, theme="asoul", length=7, zeros=True):
    if theme not in __themes__: theme = "asoul"
    count = int(count % math.pow(10, length))
    numbers = "{:0" + str(length) + "d}" if zeros else "{}"
    parts = []
    x = 0
    y = 0
    for number in numbers.format(count):
        info = __themes__[theme][number]
        parts.append('<image x="{}" y="0" width="{}" height="{}" xlink:href="{}" />'.format(x, str(info["width"]), \
            str(info["height"]), info["data"]))
        x += info["width"]
        if y < info["height"]: y = info["height"]
    return __image__.format(x, y, "\n".join(parts))
