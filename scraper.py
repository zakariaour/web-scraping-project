import requests
from bs4 import BeautifulSoup
import csv


def scrape_amazon(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Erreur : impossible d'accéder à la page (Code {response.status_code})")
        return

    soup = BeautifulSoup(response.content, "html.parser")
    products = []
    for product in soup.select(".s-main-slot .s-result-item"):
        title = product.select_one("h2 a span")
        price = product.select_one(".a-price span.a-offscreen")
        if title and price:
            products.append({"title": title.text.strip(), "price": price.text.strip()})

    with open("products.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["title", "price"])
        writer.writeheader()
        writer.writerows(products)

    print("Scraping terminé. Les résultats sont dans products.csv")


if __name__ == "__main__":
    amazon_url = "https://www.amazon.fr/s?k=clavier+gaming"
    scrape_amazon(amazon_url)
