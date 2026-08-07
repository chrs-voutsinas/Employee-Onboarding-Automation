class WikipediaPage:
    def __init__(self, page):
        self.page = page

    def open(self):
        self.page.goto("https://www.wikipedia.org")        
        