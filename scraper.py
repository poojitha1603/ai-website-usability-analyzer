import requests
from bs4 import BeautifulSoup

def extract_website_data(url):
    if not url.startswith("http"):
        url = "https://" + url

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ")
    cleaned_text = " ".join(text.split())

    return html, cleaned_text
