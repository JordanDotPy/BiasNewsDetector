import requests
from bs4 import BeautifulSoup


def scrape_text_from_url(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract text from the HTML
            text = soup.get_text(separator=' ', strip=True)

            return text
        else:
            return "Error: Unable to fetch the webpage."
    except Exception as e:
        return f"An error occurred: {e}"
