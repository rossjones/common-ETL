
from HTMLParser import HTMLParser

class LinkExtractor(HTMLParser):

    def reset(self):
        HTMLParser.reset(self)
        self.links      = []

    def setPattern(self, url, mask, type):
        self.mask = mask
        self.type = type
        if "/" in url:
            self.base = url[0:url.rfind("/")] + "/"
        else:
            self.base = url + "/"

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            attrs = dict(attrs)   # store attributes in object
        if tag == "a" and "href" in attrs:
            href = attrs["href"]
            if "/" in href:
                file = href[href.rfind("/")+1:].lower()
            else:
                file = href.lower()
#            if href.lower().endswith("."+self.type) and (href.lower().maskswith(self.mask) or ("/"+self.mask) in href.lower()):
            if file.endswith("." + self.type) and fnmatch.fnmatch(file, self.mask):
                if not href.lower().startswith("http://") and not href.lower().startswith("https://"):
                    href = self.base + href
                self.links.append(href)

