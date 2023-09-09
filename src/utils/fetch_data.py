from dotenv import load_dotenv
import os
import requests
from requests import HTTPError, Response
from typing import List

load_dotenv()
APOD_API = os.environ.get("APOD_API")
WIKI_API = os.environ.get("WIKI_API")


def get_picture_of_day(date: str) -> Response:
    try:
        response = requests.get(f"{APOD_API}&date={date}&thumbs=true")
        return response
    except HTTPError:
        return Response()


def get_wiki_pages(data) -> Response:
    title = data.get("title")
    params = {"action": "query", "format": "json", "list": "search", "srsearch": title}
    try:
        return requests.get(WIKI_API, params=params)
    except HTTPError:
        return Response()


def get_wiki_extlinks(title: str) -> Response:
    params = {"action": "query", "format": "json", "titles": title, "prop": "extlinks"}
    try:
        return requests.get(WIKI_API, params=params)
    except HTTPError:
        return Response()


def get_cleaned_wiki_data(data: Response, associated_page_limit=1) -> List[str]:
    '''
    given response from NASA APOD data, makes calls to the wiki api
    and parses the response to return additional information
    :param data: Response:
    :param associated_page_limit: int: number of associated wiki pages to grab external URLS
    :return: List[str] list of external URL about the APOD image
    '''
    response = get_wiki_pages(data)
    pageid_title_lst = [
        (str(entry.get("pageid")), entry.get("title"))
        for entry in response.json().get("query", {}).get("search")
    ]
    links = []
    try:
        for ii in range(associated_page_limit):
            pageid, title = pageid_title_lst[ii]
            response = get_wiki_extlinks(title)
            if response.status_code == 200:
                parsed_list = (
                    response.json()
                    .get("query", dict())
                    .get("pages", dict())
                    .get(pageid, dict())
                    .get("extlinks")
                )
                links.extend([entry.get("*") for entry in parsed_list])
        return links
    except:
        return []
