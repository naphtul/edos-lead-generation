import json
import logging

from schema.types import Company, LeadPerson
from src.db.db import DB
from src.openai.completions import OpenAICompletions
from src.serpapi.search import GoogleSearch
from src.utils.utils import strip_html_using_regex, fetch_page


class Scraper:
    def __init__(self) -> None:
        self.db = DB()
        self.db.connect()
        self.gs = GoogleSearch()
        self.gpt = OpenAICompletions()

    def get_search_results_from_google(self, term: str) -> tuple:
        logging.info(f"Searching Google for {term}")
        # TODO: Ask ChatGPT (programmatically) to generate a search queries based on my goal
        # Commented out to avoid hitting the free API limit
        # results = gs.search(term)
        # search_id = gs.save_results("google", term, datetime.now(), results["organic_results"])
        # return results["organic_results"], search_id
        results = self.db.query_data("searches", condition=f"source = 'google' AND searchterm = '{term}'")
        return json.loads(results[0][4]), results[0][0]

    def scrape(self, url: str) -> dict:
        logging.info(f"Scraping {url}")
        if not url:
            return {}
        page = fetch_page(url)
        html_text = strip_html_using_regex(page)
        data = self.gpt.find_contacts(html_text)
        return data

    def follow_up(self, result: dict, data: dict) -> dict:
        logging.info(f"Following up with {result['link']} additional pages")
        results = dict(contact_us_link=dict(), about_us_link=dict(), people_link=dict())
        for page_type in results.keys():
            if page_type not in data[0]:
                continue
            page_link = result["link"] + data[0][page_type] if data[0][page_type].startswith('/') else data[0][page_type]
            results[page_type] = self.scrape(page_link)
        return results

    def prepare_and_insert_data(self, data: dict, search_result: dict, search_id: int) -> list:
        logging.info(f"Preparing data for {search_result['title']}")
        company = Company(
            name=search_result["title"],
            website=search_result["link"],
            description=search_result["snippet"],
            relevancyscore=search_result["position"],
            searchid=search_id,
            segmentid=1
        )
        # TODO: Avoid duplicate companies
        company_id = self.db.insert_data("companies", company.__dict__)
        lead_persons = []
        for page in data.keys():
            for person in data[page]:
                lead_persons.append(LeadPerson(
                    # TODO: Map the fields properly
                    name=person["contact_name"] if person["contact_name"] else None,
                    email=person["contact_email"] if person["contact_email"] else None,  # TODO: Email is protected. Research how to get it.
                    cellphone=person["contact_phone"] if person["contact_phone"] else None,
                    companyid=company_id,
                    locationid=1,  # TODO: Handle location
                    workphone=person["contact_phone"] if person["contact_phone"] else None,
                    title=person["contact_title"] if person["contact_title"] else None,
                    placersalesperson=1,
                ))
        for lead_person in lead_persons:
            self.db.insert_data("leadpersons", lead_person.__dict__)
        return lead_persons

    def crawl_and_scrape(self, term: str) -> None:
        results, search_id = self.get_search_results_from_google(term)

        for result in results:
            homepage_data = self.scrape(result['link'])
            additional_data = self.follow_up(result, homepage_data)
            data = dict(homepage_data=homepage_data, **additional_data)
            prepared_data = self.prepare_and_insert_data(data, result, search_id)


if __name__ == "__main__":
    scraper = Scraper()
    term = "new york economic development organization"
    scraper.crawl_and_scrape(term)
