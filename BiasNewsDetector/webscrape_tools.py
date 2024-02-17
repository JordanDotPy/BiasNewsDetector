import requests
from bs4 import BeautifulSoup
from newspaper import Article


def beautifulsoup_scrape(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract text from the HTML
            text = soup.get_text(separator=' ', strip=True)

            # find how many words are in the text
            words = text.split()

            return text, len(words)
        else:
            return "Error: Unable to fetch the webpage."
    except Exception as e:
        return f"An error occurred: {e}"


def newspaper_scrape(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        text = article.text
        words = text.split()
        return text, len(words)
    except Exception as e:
        return f"An error occurred: {e}", 0

