from http import HTTPStatus

import requests
from bs4 import BeautifulSoup


def parse_content_for_given_url(base_url: str) -> str:
    related_urls = get_urls(base_url)
    if related_urls:
        whole_content = ""
        for url in related_urls:
            content = scrape_content(url)
            if content:
                whole_content += content + "\n"

        return whole_content


def scrape_content(url: str) -> str | None:
    response = requests.get(url)
    if response.status_code == HTTPStatus.OK:
        soup = BeautifulSoup(response.content, "html.parser")
        paragraphs = soup.find_all("p")
        content = "\n".join(paragraph.get_text() for paragraph in paragraphs)
        return content
    return


def get_urls(base_url: str) -> set[str]:
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "html.parser")
    urls = {base_url}

    for a_tag in soup.find_all("a"):
        url = a_tag.get("href")
        if url and url.startswith(base_url):
            urls.add(url)

    return urls
