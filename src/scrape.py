import json
import logging

from schema.types import Company, LeadPerson, Location
from src.db.db import DB
from src.clients.completions import OpenAICompletions
from src.clients.search import GoogleSearch
from src.utils.utils import strip_html_using_regex, fetch_page


logging.basicConfig(level=logging.INFO)

class Scraper:
    def __init__(self) -> None:
        self.db = DB()
        self.db.connect()
        self.gs = GoogleSearch()
        self.gpt = OpenAICompletions()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.db.connection.closed:
            self.db.close_connection()

    def get_search_results_from_google(self, term: str) -> tuple:
        """
        Get the search results from Google using SerpAPI
        :param term: The search term to use
        :return: A tuple containing the search results and the search ID
        """
        logging.info(f"Searching Google for {term}")
        # TODO: Ask ChatGPT (programmatically) to generate a search queries based on my goal
        # Commented out to avoid hitting the free API limit
        # results = gs.search(term)
        # search_id = gs.save_results("google", term, datetime.now(), results["organic_results"])
        # return results["organic_results"], search_id
        results = self.db.query_data("searches", condition=f"source = 'google' AND searchterm = '{term}'")
        return json.loads(results[0][4]), results[0][0]

    def scrape(self, url: str) -> dict:
        """
        Scrape the data from the website using OpenAI's Chat Completions API with GPT-4
        :param url: The URL to scrape
        :return: The data scraped from the website
        """
        logging.info(f"Scraping {url}")
        if not url:
            return {}
        page = fetch_page(url)
        html_text = strip_html_using_regex(page)
        data = self.gpt.find_page_info(html_text)
        return data

    def follow_up(self, result: dict, data: dict) -> dict:
        """
        Follow up with the links on the homepage to find additional pages
        :param result: The search result from Google
        :param data: The data scraped from the homepage
        :return: The data scraped from the additional pages
        """
        logging.info(f"Following up with {result['link']} additional pages")
        results = dict(contact_us_link=dict(), about_us_link=dict(), people_link=dict())
        for page_type in results.keys():
            if not data or page_type not in data[0]:
                continue
            page_link = result["link"].strip("/") + data[0][page_type] if data[0][page_type].startswith("/") else data[0][page_type]
            results[page_type] = self.scrape(page_link)
        return results

    def prepare_and_insert_data(self, data: dict, search_result: dict, search_id: int) -> None:
        """
        Prepare the data and insert it into the database
        :param data: The found properties from the website on the various pages
        :param search_result: The search result from Google
        :param search_id: The search result ID from the database (based on the rank in the search results)
        """
        logging.info(f"Preparing data for {search_result['title']}")
        # Handle companies
        found_company = self.db.query_data("companies", condition=f"website = '{search_result["link"]}'")
        new_company = Company(
            name=search_result["title"],
            website=search_result["link"],
            description=search_result["snippet"],
            relevancyscore=search_result["position"],
            searchid=search_id,
            segmentid=1
        )
        company_id = found_company[0][0] if found_company else self.db.insert_data("companies", new_company.__dict__)

        # Handle locations
        locations = []
        for page in data.values():
            for found in page:
                locations.append(Location(
                    address=found["street"] if "street" in found and found["street"] else found["full_address"] if "full_address" in found and found["full_address"] else None,
                    city=found["city"] if "city" in found and found["city"] else None,
                    state=found["state"] if "state" in found and found["state"] else None,
                    postalcode=found["postal_code"] if "postal_code" in found and found["postal_code"] else None,
                    pobox=found["po_box"] if "po_box" in found and found["po_box"] else None,
                    country=found["country"] if "country" in found and found["country"] else None,
                    hours=found["hours_of_operation"] if "hours_of_operation" in found and found["hours_of_operation"] else found["office_hours"] if "office_hours" in found and found["office_hours"] else None,
                    companyid=company_id,
                ))
        location_id = 1
        for location in locations:  # TODO: Handle duplicate locations
            if location.address:
                location_id = self.db.insert_data("locations", location.__dict__)

        # Handle lead persons
        lead_persons = []
        for page in data.values():
            for found in page:
                lead_persons.append(LeadPerson(
                    name=found["contact_name"] if "contact_name" in found and found["contact_name"] else None,
                    title=found["contact_title"] if "contact_title" in found and found["contact_title"] else None,
                    workphone=found["work_phone"] if "work_phone" in found and found["work_phone"] else None,
                    cellphone=found["cell_phone"] if "cell_phone" in found and found["cell_phone"] else None,
                    # TODO: Email is protected. Research how to get it.
                    email=found["contact_email"] if "contact_email" in found and found["contact_email"] else found["company_email"] if "company_email" in found and found["company_email"] else None,
                    companyid=company_id,
                    locationid=location_id,
                    placersalesperson=1,
                ))
        for lead_person in lead_persons:
            if lead_person.name:
                self.db.insert_data("leads", lead_person.__dict__)

    def crawl_and_scrape(self, term: str) -> None:
        """
        Crawl Google search results and scrape the data from the websites using OpenAI's Chat Completions API with GPT-4
        :param term: The search term to use
        """
        # TODO: Research if using LangChain yields better results
        # TODO: Cache the GPT results in a vector database
        results, search_id = self.get_search_results_from_google(term)

        for result in results:
            homepage_data = self.scrape(result['link'])
            additional_data = self.follow_up(result, homepage_data)
            data = dict(homepage_data=homepage_data, **additional_data)
            self.prepare_and_insert_data(data, result, search_id)


if __name__ == "__main__":
    with Scraper() as scraper:
        goal = "new york economic development organization"
        scraper.crawl_and_scrape(goal)
