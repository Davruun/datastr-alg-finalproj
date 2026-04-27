"""
scraper.py
----------
Fetches internal hyperlinks from a starter Wikipedia page.

Uses Wikipedia REST API's summary endpoint to validate titles 
and the standard HTML to extract all internal article links.
"""

from __future__ import annotations
import time
import re
import requests
from bs4 import BeautifulSoup

WIKI_BASE = "https://en.wikipedia.org"

_ARTICLE_RE = re.compile(r"^/wiki/([^:#]+)$")


class WikiScraper:
    """
    Fetches the list of internal Wikipedia article links from a starter page.
    """

    def __init__(self, delay: float = 0.5) -> None:
        self.delay = delay
        self._session = requests.Session()
        self._session.headers.update(
            {"User-Agent": "WikiGraphExplorer/1.0 (Educational Project; github.com/Davruun/datastr-alg-finalproj)"}
        )

    def get_links(self, title: str) -> list[str]:
        """
        Return a list of Wikipedia page titles linked from `title`.
        Only internal article links (/wiki/<Title>) are returned.
        Special-namespace pages exclued.
        title : Wikipedia page title, e.g. "Data science","Deep learning"
        returns: list of linked article titles 
        """
        url = f"{WIKI_BASE}/wiki/{title.replace(' ', '_')}"
        try:
            resp = self._session.get(url, timeout=10)
            resp.raise_for_status()
        except requests.RequestException as exc:
            print(f"[scraper] Could not fetch '{title}': {exc}")
            return []

        soup = BeautifulSoup(resp.text, "lxml")
        content = soup.find("div", id="mw-content-text")
        if content is None:
            return []

        seen: set[str] = set()
        links: list[str] = []
        for tag in content.find_all("a", href=True):
            href: str = tag["href"]
            match = _ARTICLE_RE.match(href)
            if match:
                page_title = match.group(1).replace("_", " ")
                if page_title not in seen:
                    seen.add(page_title)
                    links.append(page_title)

        time.sleep(self.delay)
        return links

    def page_exists(self, title: str) -> bool:
        """Return True if a Wikipedia article with this title exists."""
        api_url = (
            f"{WIKI_BASE}/api/rest_v1/page/summary/{title.replace(' ', '_')}"
        )
        try:
            resp = self._session.get(api_url, timeout=8)
            return resp.status_code == 200
        except requests.RequestException:
            return False
