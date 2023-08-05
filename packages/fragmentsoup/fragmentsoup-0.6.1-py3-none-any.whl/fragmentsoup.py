"""
A wrapper for BeautifulSoup4 that restores the ability to work with HTML fragments
"""

__version__ = "0.6.1"

from bs4 import (
    BeautifulSoup,
    NavigableString,
    Tag,
    Comment,
)  # pylint: disable=unused-import

try:
    import lxml  # pylint: disable=unused-import

    best_parser = "lxml"
except ImportError:
    try:
        import html5lib  # pylint: disable=unused-import

        best_parser = "html5lib"
    except ImportError:
        best_parser = "html.parser"


def find_parser(*args, **kwargs):
    "If the user set a parser, use the same one"
    parsers = "lxml", "lxml-xml", "xml", "html5lib", "html.parser"
    current_parser = best_parser
    if "features" in kwargs:
        current_parser = kwargs["features"]
        return current_parser
    else:
        user_set_parser = False
        for arg in args:
            if user_set_parser:
                continue
            for p in parsers:
                if arg == p:
                    current_parser = p
                    user_set_parser = True
                    break
                if user_set_parser:
                    continue
    return current_parser


class FragmentSoup:
    def __init__(self, *args, **kwargs):
        if args:
            # We have an HTML snippet
            htmlsnippet = args[0]
        else:
            htmlsnippet = ""
        parser = find_parser(*args[1:], **kwargs)
        kwargs["features"] = parser
        self.snippet = htmlsnippet
        self._wellformed = False
        is_fragment = False
        if "<fragmentsoup>" in str(htmlsnippet):
            is_fragment = True
        self._rawsoup = BeautifulSoup(**kwargs)
        if (
            str(htmlsnippet).strip().startswith("<!DOCTYPE")
            or str(htmlsnippet).strip().lower().startswith("<html")
        ) and not is_fragment:
            self._wellformed = True
            self._soup = BeautifulSoup(htmlsnippet, **kwargs)
        else:
            if is_fragment:
                self._soup = BeautifulSoup(str(htmlsnippet), **kwargs)
            else:
                self._soup = BeautifulSoup(
                    "<fragmentsoup>%s</fragmentsoup>" % htmlsnippet, **kwargs
                )

    def render(self, pretty=False):
        if pretty:
            if self._wellformed:
                return self._soup.prettify()
            else:
                return (
                    self._soup.fragmentsoup.prettify()
                    .replace("<fragmentsoup>", "")
                    .replace("</fragmentsoup>", "")
                )
        else:
            if self._wellformed:
                return str(self._soup)
            else:
                return (
                    str(self._soup.fragmentsoup)
                    .replace("<fragmentsoup>", "")
                    .replace("</fragmentsoup>", "")
                )

    def prettify(self):
        return self.render(pretty=True)

    def wrap(self, tag):
        if self._wellformed:
            raise ValueError(
                "Fragment is well-formed (starts with <!DOCTYPE or <html). Cannot wrap outer element of a tree with an inner tag."
            )
        new_tag = tag.name
        self._soup.fragmentsoup.wrap(tag)
        getattr(self._soup, new_tag).wrap(self.new_tag("fragmentsoup"))
        getattr(self._soup.fragmentsoup, new_tag).fragmentsoup.unwrap()
        return self

    def new_tag(self, tagname):
        if self._wellformed:
            return self._soup.new_tag(tagname)
        else:
            return self._rawsoup.new_tag(tagname)

    def __repr__(self):
        return self.render()

    def __str__(self):
        return self.render()

    def __getattribute__(self, item):
        if item in [
            "__init__",
            "__repr__",
            "__str__",
            "_wellformed",
            "_soup",
            "_rawsoup",
            "wrap",
            "render",
            "snippet",
            "prettify",
            "new_tag",
        ]:
            return super(FragmentSoup, self).__getattribute__(item)
        else:
            return getattr(self._soup, item)
