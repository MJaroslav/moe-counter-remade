import os

import yattag

import moe.utils as utils


class ThemeManager(object):
    def __init__(self, default_theme: str = "asoul"):
        self.themes = {}
        self.default_theme = default_theme
        self.__load_themes__()

    def build_image(self, number: int = 0, max_length: int = 7, demo: bool = False, lead_zeros: bool = False,
                    theme: str = None):
        if theme not in self.themes:
            theme = self.default_theme
        if demo:
            number = 123456789
            max_length = 10
            lead_zeros = True
        doc, tag, text = yattag.Doc().tagtext()
        doc.asis('<?xml version="1.0" encoding="UTF-8"?>')
        with tag('svg', version="1.1", xmlns="http://www.w3.org/2000/svg",
                 **{'xmlns:xlink': "http://www.w3.org/1999/xlink"}):
            with tag('title'):
                text("Moe Count")
            with tag("g"):
                x = y = 0
                for i in utils.trim_and_str_number(number, max_length, lead_zeros):
                    data, width, height = self.themes[theme][i].values()
                    with tag("image", x=x, y=0, width=width, height=height, **{'xlink:href': data}):
                        x += width
                        y = max(height, y)
            doc.attr(width=x, height=y)
        return doc.getvalue()

    def __load_themes__(self):
        for theme in os.listdir("./assets/themes/"):
            print("Found theme {}".format(theme))
            for file in os.listdir("./assets/themes/{}/".format(theme)):
                path = "./assets/themes/{}/{}".format(theme, file)
                if os.path.isfile(path):
                    mime = utils.get_mime_type(path)
                    if mime.startswith("image"):
                        data = "data:{};base64,{}".format(mime, utils.to_base64(path))
                        width, height = utils.get_image_dimensions(path)
                        number = os.path.splitext(file)[0]
                        body = {"data": data, "width": width, "height": height}
                        if theme not in self.themes:
                            self.themes[theme] = {number: body}
                        else:
                            self.themes[theme][number] = body
