"""
libs.strings

By default, uses `en-gb.json` file inside the `strings` top-level folder.

If language changes, set `libs.strings.default_locale` and run `libs.strings.refresh()`.
"""
import json
import os

default_locale = "en-gb"
cached_strings = {}


def refresh():
    dir_path=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'strings'))
    print("Refreshing...")
    global cached_strings
    with open(f"{dir_path}\{default_locale}.json") as f:
        cached_strings = json.load(f)


def gettext(name):
    return cached_strings[name]


refresh()
