from newspaper import Article


def newspaper_scrape(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        title = article.title
        text = article.text
        words = text.split()
        return title, text, len(words)
    except Exception as e:
        return f"An error occurred: {e}", 0
