import re

import requests
from bs4 import BeautifulSoup, ResultSet


def strip_html_to_text(html_text: str) -> str:
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup.get_text()


def get_all_links_from_html(html_text: str) -> ResultSet:
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup.find_all('a')


def strip_html_using_regex(html_text: str) -> str:
    # Remove everything between <head> and </head>
    html_text = re.sub(r'<head.*?>.*?</head>', '', html_text, flags=re.DOTALL)
    # Remove all occurrences of content between <script> and </script>
    html_text = re.sub(r'<script.*?>.*?</script>', '', html_text, flags=re.DOTALL)
    # Remove all occurrences of content between <style> and </style>
    html_text = re.sub(r'<style.*?>.*?</style>', '', html_text, flags=re.DOTALL)
    return html_text


def fetch_page(url: str) -> str:
    return requests.get(url).text
