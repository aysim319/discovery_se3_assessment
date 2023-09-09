import json
from pathlib import Path
import unittest
from unittest import mock

from src.utils.fetch_data import get_picture_of_day, get_wiki_pages, get_wiki_extlinks


TEST_PROJECT_DIR = Path(__file__).resolve().parent


class MyTestCase(unittest.TestCase):
    date = "2023-04-01"
    with open(f"{TEST_PROJECT_DIR}/data/{date}-apod.json") as f:
        test_apod_data = json.load(f)
    with open(f"{TEST_PROJECT_DIR}/data/{date}-apod-wiki-results.json") as f:
        test_wiki_data = json.load(f)
    with open(f"{TEST_PROJECT_DIR}/data/{date}-wiki-extlinks.json") as f:
        test_wiki_ext_data = json.load(f)

    @mock.patch("requests.get")
    def test_APOD(self, mock_requests):
        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.return_value = self.test_apod_data
        response = get_picture_of_day(date=self.date)
        mock_requests.assert_called_once()
        self.assertEqual(response.json(), self.test_apod_data)

    @mock.patch("requests.get")
    def test_wiki_hits(self, mock_requests):
        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.return_value = self.test_wiki_data
        response = get_wiki_pages(data=self.test_apod_data)
        mock_requests.assert_called_once()
        self.assertEqual(response.json(), self.test_wiki_data)

    @mock.patch("requests.get")
    def test_wiki_ext_links(self, mock_requests):
        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.return_value = self.test_wiki_ext_data
        title = (
            self.test_wiki_data.get("query", dict()).get("search", [])[0].get("title")
        )
        response = get_wiki_extlinks(title=title)
        mock_requests.assert_called_once()
        self.assertEqual(response.json(), self.test_wiki_ext_data)

    @mock.patch("requests.get")
    def test_get_cleaned_wiki_data(self, mock_requests):
        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.return_value = self.test_wiki_ext_data
        title = (
            self.test_wiki_data.get("query", dict()).get("search", [])[0].get("title")
        )
        response = get_wiki_extlinks(title=title)
        mock_requests.assert_called_once()
        self.assertEqual(response.json(), self.test_wiki_ext_data)


if __name__ == "__main__":
    unittest.main()
