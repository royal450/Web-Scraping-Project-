import trafilatura
import requests
from bs4 import BeautifulSoup
import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def scrape(self, url: str, selector: str) -> List[Dict[str, str]]:
        """
        Scrapes content from a webpage using requests and BeautifulSoup.

        Args:
            url: The URL to scrape
            selector: CSS selector for targeting specific elements

        Returns:
            List of dictionaries containing text and HTML content
        """
        try:
            logger.info(f"Attempting to scrape URL: {url}")

            # Download webpage
            response = self.session.get(url, timeout=30)
            response.raise_for_status()  # Raise exception for bad status codes

            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find elements matching the selector
            elements = soup.select(selector)

            if not elements:
                logger.warning(f"No elements found matching selector: {selector}")
                return []

            # Extract data from elements
            data = []
            for element in elements:
                data.append({
                    'text': element.get_text(strip=True),
                    'html': str(element)
                })

            logger.info(f"Successfully scraped {len(data)} elements from {url}")
            return data

        except requests.RequestException as e:
            logger.error(f"Error downloading webpage: {str(e)}")
            raise Exception(f"Error downloading webpage: {str(e)}")
        except Exception as e:
            logger.error(f"Error during scraping: {str(e)}")
            raise Exception(f"Error during scraping: {str(e)}")