import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class OpenAICompletions:
    def __init__(self) -> None:
        self.openai_client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

    def find_contacts(self, html_text: str) -> dict:
        # Chat Completion API from OpenAI
        completion = self.openai_client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[{"role": "system", "content": """You are an expert at scraping and parsing raw HTML into JSON. 
            You are given the following HTML. 
            Please extract the following details from the page. 
            If you can't find the info, return an empty String.
            """},
                      {"role": "user", "content": html_text},
                      {"role": "system", "content": "Parse the following data into JSON:"},
                      {"role": "system", "content": "Contact Name: {{contact_name}}"},
                      {"role": "system", "content": "Contact Title: {{contact_title}}"},
                      {"role": "system", "content": "Contact Phone: {{contact_phone}}"},
                      {"role": "system", "content": "Contact Email: {{contact_email}}"},
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
                                        'contact_phone': {
                                            'type': 'string'
                                        },
                                        'contact_email': {
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
