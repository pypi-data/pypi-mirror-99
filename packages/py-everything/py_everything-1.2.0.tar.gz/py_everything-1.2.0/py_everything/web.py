import webbrowser

google_url = 'https://google.com/search?q='
yt_url = 'https://youtube.com/results?search_query='
github_url = 'https://github.com/search?q='
so_url = 'https://stackoverflow.com/search?q='
amz_in_url = 'https://www.amazon.in/s?k='
amz_com_url = 'https://www.amazon.com/s?k='
pypi_url = 'https://pypi.org/search/?q='
rtdocs_url = 'https://readthedocs.io/search/?q='

def googleSearch(query):
    final_url = google_url + query
    webbrowser.open(final_url)

def ytSearch(query):
    final_url = yt_url + query
    webbrowser.open(final_url)

def githubSearch(query):
    final_url = github_url + query
    webbrowser.open(final_url)

def soSearch(query):
    final_url = so_url + query
    webbrowser.open(final_url)

def amz_inSearch(query):
    final_url = amz_in_url + query
    webbrowser.open(final_url)

def amz_comSearch(query):
    final_url = amz_com_url + query
    webbrowser.open(final_url)

def pypiSearch(query):
    final_url = pypi_url + query
    webbrowser.open(final_url)

def rtdocsSearch(query):
    final_url = rtdocs_url + query
    webbrowser.open(final_url)

def openNewTab(url, query):
    final_url = url + query
    webbrowser.open_new_tab(final_url)

def openNewWindow(url, query):
    final_url = url + query
    webbrowser.open_new(final_url)

class webSearchBase:
    def __init__(self):
        self.google_url = 'https://google.com/search?q='
        self.yt_url = 'https://youtube.com/results?search_query='
        self.github_url = 'https://github.com/search?q='
        self.so_url = 'https://stackoverflow.com/search?q='

    def googleSearch(self, query):
        final_url = self.google_url + query
        webbrowser.open(final_url)

    def ytSearch(self, query):
        final_url = self.yt_url + query
        webbrowser.open(final_url)

    def githubSearch(self, query):
        final_url = self.github_url + query
        webbrowser.open(final_url)

    def soSearch(self, query):
        final_url = self.so_url + query
        webbrowser.open(final_url)


class webSearchAdvanced:
    def __init__(self):
        self.google_url = 'https://google.com/search?q='
        self.yt_url = 'https://youtube.com/results?search_query='
        self.github_url = 'https://github.com/search?q='
        self.so_url = 'https://stackoverflow.com/search?q='
        self.amz_in_url = 'https://www.amazon.in/s?k='
        self.amz_com_url = 'https://www.amazon.com/s?k='
        self.pypi_url = 'https://pypi.org/search/?q='
        self.rtdocs_url = 'https://readthedocs.io/search/?q='

    def googleSearch(self, query):
        final_url = self.google_url + query
        webbrowser.open(final_url)

    def ytSearch(self, query):
        final_url = self.yt_url + query
        webbrowser.open(final_url)

    def githubSearch(self, query):
        final_url = self.github_url + query
        webbrowser.open(final_url)

    def soSearch(self, query):
        final_url = self.so_url + query
        webbrowser.open(final_url)

    def amz_inSearch(self, query):
        final_url = self.amz_in_url + query
        webbrowser.open(final_url)

    def amz_comSearch(self, query):
        final_url = self.amz_com_url + query
        webbrowser.open(final_url)

    def pypiSearch(self, query):
        final_url = self.pypi_url + query
        webbrowser.open(final_url)

    def rtdocsSearch(self, query):
        final_url = self.rtdocs_url + query
        webbrowser.open(final_url)

    def openNewTab(self, url, query):
        final_url = url + query
        webbrowser.open_new_tab(final_url)

    def openNewWindow(self, url, query):
        final_url = url + query
        webbrowser.open_new(final_url)
