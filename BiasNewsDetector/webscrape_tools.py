from newspaper import Article
from bs4 import BeautifulSoup


def newspaper_scrape(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        title = article.title
        authors = article.authors
        text = article.text
        words = text.split()
        return title, text, len(words), authors
    except Exception as e:
        return f"An error occurred: {e}", 0


def newspaper_scrape2(url):
    try:
        # Download and parse the article
        article = Article(url)
        article.download()
        article.parse()

        # Get the raw HTML and parse it with BeautifulSoup
        soup = BeautifulSoup(article.html, 'html.parser')

        # Find all paragraph tags and get the text content
        paragraphs = soup.find_all('p')
        paragraphs_text = [paragraph.get_text() for paragraph in paragraphs if paragraph.get_text().strip() != '']

        # Join paragraphs with newline characters to maintain spacing
        text_by_paragraphs = '\n\n'.join(paragraphs_text)

        title = article.title
        words = text_by_paragraphs.split()

        return title, text_by_paragraphs, len(words)
    except Exception as e:
        return f"An error occurred: {e}", '', 0
