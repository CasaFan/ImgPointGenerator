from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):

    polygone_collection = []

    def handle_starttag(self, tag, attrs):
        self.polygone_collection.append(attrs)
