import json
import logging
import os
from datetime import datetime

import serpapi
from dotenv import load_dotenv

from src.db.db import DB

load_dotenv()


class GoogleSearch:
    def __init__(self) -> None:
        self.serpapi_client = serpapi.Client(api_key=os.environ.get('SERPAPI_API_KEY'))
        self.db = DB()

    def search(self, query: str) -> dict:
        options: dict = dict(
            engine='google',
            q=query,
            location='New York, New York, United States',
            gl='us',
            hl='en',
            safe='off',
            num=100,
        )
        try:
            return self.serpapi_client.search(options)
        except Exception as e:
            logging.exception(e)
            raise e

    def save_results(self, source: str, searchterm: str, searchdate: datetime, results: dict) -> int:
        try:
            self.db.connect()
            data = dict(
                source=source,
                searchterm=searchterm,
                searchdate=searchdate,
                results=json.dumps(results)
            )
            return self.db.insert_data('searches', data)
        except Exception as e:
            logging.exception(e)
            raise e


if __name__ == "__main__":
    gs = GoogleSearch()
    term = "new york economic development organization"
    results = gs.search(term)
    gs.save_results("google", term, datetime.now(), results["organic_results"])
