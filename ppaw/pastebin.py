"""
Python Pastebin API Wrapper.

Provide an object for easily accessible pastes and functions to
fetch existing pastes or create new ones.
"""

from ppaw import definitions, request
from ppaw.errors import PPAWBaseException

class Paste(object):
    def __init__(self, key, date=None, title=None, size=None, expire_date=None, private=None, format_short=None, format_long=None, url=None, hits=None):
        self.key = key
        self.date = date
        self.title = title
        self.size = size
        self.expire_date = expire_date
        self.private = private
        self.format_short = format_short
        self.format_long = format_long
        self.url = url if url else "http://pastebin.com/" + self.key
        self.hits = hits
        self.data = None

    @classmethod
    def fromString(cls, string):
        attributes = ["key", "date", "title", "size", "expire_date", "private", "format_short", "format_long", "url", "hits"]
        values = []
        for attr in attributes:
            opentag, closetag = "<paste_{0}>|</paste_{0}>".format(attr).split("|")
            try:
                values.append(string.split(opentag)[1].split(closetag)[0])
            except IndexError:
                values.append(None)

        return cls(**dict((attr, values[idx]) for idx, attr in enumerate(attributes)))

    def fetch(self):
        self.data = request.get("http://pastebin.com/raw.php?i=" + self.key)


class Pastebin:
    def __init__(self, dev_key):
        self.dev_key = dev_key
        self.user_key = ""

    def login(self, user_name, user_password):
        req = request.post(
            definitions.login_url,
            {
                "api_dev_key": self.dev_key,
                "api_user_name": user_name,
                "api_user_password": user_password
            }
        )
        self.user_key = req
        return True

    def get_trending_pastes(self):
        return [Paste.fromString(x) for x in request.post(
            definitions.post_url,
            {
                "api_option": "trends",
                "api_dev_key": self.dev_key
            }
        ).split("<paste>") if x]

    def get_paste(self, paste_key):
        paste = Paste(paste_key)
        paste.fetch()
        return paste

    def create_paste(self, paste_code, paste_name="", paste_format="",
                     paste_private="", paste_expire_date="", guest=False):
        user_key = "" if guest else self.user_key
        return Paste(request.post(
            definitions.post_url,
            {
                "api_option": "paste",
                "api_dev_key": self.dev_key,
                "api_user_key": user_key,
                "api_paste_code": paste_code,
                "api_paste_name": paste_name,
                "api_paste_format": paste_format,
                "api_paste_private": paste_private,
                "api_paste_expire_date": paste_expire_date
            }
        ).split("/")[-1])

    def delete_paste(self, paste_key):
        return request.post(
            definitions.post_url,
            {
                "api_option": "delete",
                "api_dev_key": self.dev_key,
                "api_user_key": self.user_key,
                "api_paste_key": paste_key
            }
        ) == "Paste Removed"

    def get_own_pastes(self, results_limit=50):
        return [Paste.fromString(x) for x in request.post(
            definitions.post_url,
            {
                "api_option": "list",
                "api_dev_key": self.dev_key,
                "api_user_key": self.user_key,
                "api_results_limit": results_limit
            }
        ).split("<paste>") if x]

    def get_own_info(self):
        return request.post(
            definitions.post_url,
            {
                "api_option": "userdetails",
                "api_dev_key": self.dev_key,
                "api_user_key": self.user_key
            }
        )
