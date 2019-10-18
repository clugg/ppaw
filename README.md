# PPAW: The Python Pastebin API Wrapper.

PPAW, an acronym for "Python Pastebin API Wrapper", is a Python package that allows for simple access to Pastebin's API. PPAW aims to be as easy to use as possible and is developed based on official documentation [found here](http://pastebin.com/api).

## Prerequisites

* Python 2.7+ or Python 3.0+
* [python-requests](https://requests.kennethreitz.org/)

A compatible version of `python-requests` can be installed via `$ pip install -r requirements.txt`.

## Documentation

### Importing

PPAW can be imported in a number of ways due to how the package is structued.

* `import ppaw` will allow PPAW's main features to be accessed via `ppaw.pastebin.Pastebin`
* `from ppaw import pastebin` will allow PPAW's main features to be accessed via `pastebin.Pastebin`

For the sake of the usage guide we will be using `import ppaw`.

### User-Agent

In order to change the User-Agent that all requests are performed with, you must set the `ppaw.pastebin.request.USERAGENT` variable to whatever you wish the User-Agent to be.

```python
ppaw.pastebin.request.USERAGENT = "my app v1.0.0"
```

### Error Handling

PPAW's `request` module handles all GET and POST requests performed to the API, and more specifically detects when an error is returned by the API. All errors the `request` module detects will be raised as `ppaw.errors.PPAWBaseException` exceptions. The `ppaw.errors.PPAWBaseException` exception has two main important properties: `code` and `msg`. `code` is the error-code returned by the API (if there is one), and `msg` is the error string returned by the API.

```python
>>> import ppaw
>>> pb = ppaw.pastebin.Pastebin("bad_api_key")
>>> try:
...     trending = pb.get_trending_pastes()
... except ppaw.errors.PPAWBaseException as e:
...     print("Error: {}".format(e.msg))
...
Error: invalid api_dev_key
```

### Usage

### The `Paste` Object

Both getting and creating a paste will return a `Paste` object. The `Paste` object has the following properties:

* str `key`: Key of the paste.
* int `date`: Timestamp of when paste was created.
* str `title`: Title of the paste.
* int `size`: Size of the paste in bytes.
* int `expire_date`: Timestamp of when the paste will expire. (?)
* int `private`: Level of paste privacy. {0: Public, 1: Unlisted, 2: Private}
* str `format_short`: Short display of the paste's format.
* str `format_long`: Long display of the paste's format.
* str `url`: Full URL of paste.
* int `hits`: Amount of views paste has.
* str `data`: Data the paste contains.

Note that almost all of this information will be `None` when the `Paste` object is created by fetching an existing poll, as the API does not return this information. Specifically, only `key`, `url` and `data` will have actual information from the paste. The rest of these fields will be filled when creating new pastes or when the paste is fetched from `Pastebin.get_trending_pastes()`.

You can call `fetch()` on a `Paste` object at any time in order to get an up to date copy of the data in the paste. The result will not be returned, but rather stored in the `data` property.

#### Getting a Paste

```python
>>> import ppaw
>>> pb = ppaw.pastebin.Pastebin("good_api_key")
>>> paste = pb.get_paste("2qbRKh3R")
>>> paste.data[:100]
u'**** LEAK ****\r\nALL CREDIT CARD PIN CODES IN THE WORLD LEAKED\r\n\r\n0000 0001 0002 0003 0004 0005 0006 '
```

#### Creating a Paste

```python
>>> import ppaw
>>> pb = ppaw.pastebin.Pastebin("good_api_key")
>>> paste = pb.create_paste("Created with Python Pastebin API Wrapper", "ppaw test", "python", 1, "N", True)
>>> paste.key
u'tRgT1Uyq'
```
