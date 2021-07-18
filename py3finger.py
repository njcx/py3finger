import json
import re
import warnings
import logging
import pkg_resources
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(name=__name__)


class Req(object):

    def __init__(self, url, html, headers):
        self.url = url
        self.html = html
        self.headers = headers
        try:
            self.headers.keys()
        except AttributeError:
            raise ValueError("Headers must be a dictionary-like object")
        self._parse_html()

    def _parse_html(self):
        self.parsed_html = soup = BeautifulSoup(self.html, 'html.parser')
        self.scripts = [script['src'] for script in
                        soup.findAll('script', src=True)]
        self.meta = {
            meta['name'].lower():
                meta['content'] for meta in soup.findAll(
                    'meta', attrs=dict(name=True, content=True))
        }


class PyFinger(object):

    def __init__(self):
        self.latest()
        for name, app in self.apps.items():
            self._prepare_app(app)

    def latest(self):
        obj = json.loads(pkg_resources.resource_string(__name__, "data/finger.json"))
        self.categories = obj['categories']
        self.apps = obj['apps']

    def _prepare_app(self, app):
        for key in ['url', 'html', 'script', 'implies']:
            try:
                value = app[key]
            except KeyError:
                app[key] = []
            else:
                if not isinstance(value, list):
                    app[key] = [value]

        for key in ['headers', 'meta']:
            try:
                value = app[key]
            except KeyError:
                app[key] = {}

        obj = app['meta']
        if not isinstance(obj, dict):
            app['meta'] = {'generator': obj}

        for key in ['headers', 'meta']:
            obj = app[key]
            app[key] = {k.lower(): v for k, v in obj.items()}

        for key in ['url', 'html', 'script']:
            app[key] = [self._prepare_pattern(pattern) for pattern in app[key]]

        for key in ['headers', 'meta']:
            obj = app[key]
            for name, pattern in obj.items():
                obj[name] = self._prepare_pattern(obj[name])

    def _prepare_pattern(self, pattern):

        regex, _, rest = pattern.partition('\\;')
        try:
            return re.compile(regex, re.I)
        except re.error as e:
            warnings.warn(
                "Caught '{error}' compiling regex: {regex}"
                .format(error=e, regex=regex)
            )
            return re.compile(r'(?!x)x')

    def _has_app(self, app, webpage):

        for regex in app['url']:
            if regex.search(webpage.url):
                return True

        for name, regex in app['headers'].items():
            if name in webpage.headers:
                content = webpage.headers[name]
                if regex.search(content):
                    return True

        for regex in app['script']:
            for script in webpage.scripts:
                if regex.search(script):
                    return True

        for name, regex in app['meta'].items():
            if name in webpage.meta:
                content = webpage.meta[name]
                if regex.search(content):
                    return True

        for regex in app['html']:
            if regex.search(webpage.html):
                return True

    def _get_implied_apps(self, detected_apps):

        def __get_implied_apps(apps):
            _implied_apps = set()
            for app in apps:
                try:
                    _implied_apps.update(set(self.apps[app]['implies']))
                except KeyError:
                    pass
            return _implied_apps

        implied_apps = __get_implied_apps(detected_apps)
        all_implied_apps = set()

        while not all_implied_apps.issuperset(implied_apps):
            all_implied_apps.update(implied_apps)
            implied_apps = __get_implied_apps(all_implied_apps)

        return all_implied_apps

    def get_categories(self, app_name):
        cat_nums = self.apps.get(app_name, {}).get("cats", [])

        cat_names = [self.categories.get("%s" % cat_num, "").get("name", "")
                     for cat_num in cat_nums]

        return cat_names

    def analyze(self, webpage):
        detected_apps = set()

        for app_name, app in self.apps.items():
            if self._has_app(app, webpage):
                detected_apps.add(app_name)

        detected_apps |= self._get_implied_apps(detected_apps)

        return detected_apps

    def analyze_with_categories(self, webpage):

        detected_apps = self.analyze(webpage)
        categorised_apps = {}

        for app_name in detected_apps:
            cat_names = self.get_categories(app_name)
            for cat_name in cat_names:
                categorised_apps[cat_name] = app_name#{"categories": cat_names}
        return categorised_apps

    def new_from_url(self, url, header=None, verify=True):
        if not header:
            header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.15 Safari/537.36'}

        response = requests.get(url, headers=header, verify=verify, timeout=2.5)
        return self.new_from_response(response)

    def new_from_response(self, response):
        return self.analyze_with_categories(Req(response.url, html=response.text, headers=response.headers))

    def new_from_html(self, html, header):
        return self.analyze_with_categories(Req("https://www.runoob.com/", html=html, headers=header))


if __name__ == "__main__":
    pyfinger = PyFinger()
    req = requests.get('https://www.runoob.com/')
    print(pyfinger.new_from_url('https://www.runoob.com/'))
    print(pyfinger.new_from_response(req))




