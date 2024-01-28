import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class OpenAICompletions:
    def __init__(self) -> None:
        self.openai_client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

    def find_page_info(self, html_text: str) -> dict:
        """
        Find the page info from the HTML text
        :param html_text: The page content
        :return: A dictionary containing the properties and values found
        """
        # Chat Completion API from OpenAI
        # TODO: Add retry on failure/empty response
        # TODO: Configure no hallucinations
        completion = self.openai_client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[{"role": "system", "content": """You are an expert at scraping and parsing raw HTML into JSON. 
            You are given the following HTML. 
            Please extract the following details from the page. 
            If you can't find the info, return an empty String.
            If you can find more than one person, return them in a list (array).
            """},
            {"role": "user", "content": html_text},
            {"role": "system", "content": "Parse the following data into JSON:"},
            {"role": "system", "content": "Contact Name: {{contact_name}}"},
            {"role": "system", "content": "Contact Title: {{contact_title}}"},
            {"role": "system", "content": "Work Phone: {{work_phone}}"},
            {"role": "system", "content": "Cell Phone: {{cell_phone}}"},
            {"role": "system", "content": "Contact Email: {{contact_email}}"},
            {"role": "system", "content": "Company Email: {{company_email}}"},
            {"role": "system", "content": "Full Address: {{full_address}}"},
            {"role": "system", "content": "Street: {{street}}"},
            {"role": "system", "content": "City: {{city}}"},
            {"role": "system", "content": "State: {{state}}"},
            {"role": "system", "content": "Postal code: {{postal_code}}"},
            {"role": "system", "content": "POBox: {{po_box}}"},
            {"role": "system", "content": "Country: {{country}}"},
            {"role": "system", "content": "Location: {{location}}"},
            {"role": "system", "content": "Hours of operation: {{hours_of_operation}}"},
            {"role": "system", "content": "Office Hours: {{office_hours}}"},
            {"role": "system", "content": "Contact Us Link: {{contact_us_link}}"},
            {"role": "system", "content": "About Us Link: {{about_us_link}}"},
            {"role": "system", "content": "People Link: {{people_link}}"},
            ],
            response_format={"type": "json_object"},
            tools=[{
                "type": "function",
                "function": {
                    "name": "parse_data",
                    "description": "Parse raw HTML data nicely",
                    "parameters": {
                        'type': 'object',
                        'properties': {
                            'data': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'contact_name': {
                                            'type': 'string'
                                        },
                                        'contact_title': {
                                            'type': 'string'
                                        },
                                        'work_phone': {
                                            'type': 'string'
                                        },
                                        'cell_phone': {
                                            'type': 'string'
                                        },
                                        'contact_email': {
                                            'type': 'string'
                                        },
                                        'company_email': {
                                            'type': 'string'
                                        },
                                        'full_address': {
                                            'type': 'string'
                                        },
                                        'street': {
                                            'type': 'string'
                                        },
                                        'city': {
                                            'type': 'string'
                                        },
                                        'state': {
                                            'type': 'string'
                                        },
                                        'postal_code': {
                                            'type': 'string'
                                        },
                                        'po_box': {
                                            'type': 'string'
                                        },
                                        'country': {
                                            'type': 'string'
                                        },
                                        'location': {
                                            'type': 'string'
                                        },
                                        'hours_of_operation': {
                                            'type': 'string'
                                        },
                                        'office_hours': {
                                            'type': 'string'
                                        },
                                        'contact_us_link': {
                                            'type': 'string'
                                        },
                                        'about_us_link': {
                                            'type': 'string'
                                        },
                                        'people_link': {
                                            'type': 'string'
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }],
            tool_choice={"type": "function", "function": {"name": "parse_data"}})

        # Calling the data results
        argument_str = completion.choices[0].message.tool_calls[0].function.arguments
        argument_dict = json.loads(argument_str)
        return argument_dict['data']
