"""
Python Pastebin API Wrapper.

Provide one-liner functions for reqing JSON files and handling any
errors provided by the PasteBin API.
"""

import json
import requests

from ppaw import __author__, __version__
from ppaw.errors import PPAWBaseException

USERAGENT = "PPAW v{} by {}".format(__version__, __author__)

def _handle(req):
    """
    Parse JSON from a request string and handle any errors
    thrown by Pastebin's API.

    Args:
        req (str): A JSON string returned from Pastebin's API.

    Returns:
        dict: Result from parsing the inputted JSON string.

    Raises:
        PPAWBaseException: when Pastebin's API returns an error.
    """

    req = req.strip()
    if "Bad API request" in req:
        raise PPAWBaseException(req.replace("Bad API request, ", ""))
    else:
        try:
            return json.loads(req)
        except ValueError:
            return req

def post(url, params={}):
    """
    Performs a POST request to the specified URL
    with the specified paramaters.

    Args:
        url (str): URL to perform POST request to.
        params (Optional[dict]): Paramaters for the POST request. Defaults to {}.

    Returns:
        dict: Result from parsing the JSON returned by the POST request.
    """

    return _handle(requests.post(url, data=params, headers={"User-Agent": USERAGENT}).text)

def get(url, params={}):
    """
    Performs a GET request to the specified URL
    with the specified paramaters.

    Args:
        url (str): URL to perform GET request to.
        params (Optional[dict]): Paramaters for the GET request. Defaults to {}.

    Returns:
        dict: Result from parsing the JSON returned by the GET request.
    """

    return _handle(requests.get(url, params=params, headers={"User-Agent": USERAGENT}).text)
