import logging
import sys
from typing import List
import requests
from .models import SearchResult

logging.basicConfig(
    stream=sys.stdout,
    format="%(asctime)s %(levelname)s[%(name)s] %(message)s",
    level=logging.INFO,
)

class GoogleCustomSearch:
    def __init__(self, api_key: str, search_engine_id: str):
        self._api_key = api_key
        self._search_engine_id = search_engine_id

    def search(self, query: str, size: int = 10, substring: str = None) -> List[SearchResult]:
        response_json = self._search_google_impl(
            query=query,
            size=size,
        )

        if response_json is None:
            logging.warning(f"search failed query: {query}")
            return []

        search_items = response_json.get("items", [])
        if not search_items:
            logging.warning(f"nothing found query: {query}")
            return []

        search_results = []

        for item in search_items:
            search_result = SearchResult(title=item["title"], link=item["link"])
            if substring and substring not in search_result.link:
                logging.info(f"skipping search result: {search_result.link} because it does not contain the substring '{substring}'")
                continue

            logging.info(f"adding search result: {search_result.link}")
            search_results.append(search_result)

        return search_results


    def _search_google_impl(
        self, query: str, size: int
    ):
        url_query = self._get_url_query(query, size)
        response = requests.get(url_query, timeout=5)
        if not response.ok:
            logging.warning(f"search failed url: {url_query} status code: {response.status_code} response: {response.text}")
            return None

        return response.json()

    def _get_url_query(self, query: str, size: int) -> str:
        capped_size = max(1, min(size, 10))
        quoted_query = requests.utils.quote(query)
        return f"https://www.googleapis.com/customsearch/v1?fields=items(title,link)&key={self._api_key}&cx={self._search_engine_id}&q={quoted_query}&num={capped_size}"

