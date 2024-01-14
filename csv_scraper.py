import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice
from csv import DictWriter

BASE_URL   = "https://quotes.toscrape.com/"

def scrape_quotes():
    all_quotes = list()
    url        = "/page/1/"
    while url:
        resp = requests.get(f"{BASE_URL}{url}")
        print(f"Now Scraping {BASE_URL}{url} ......")
        
        soup = BeautifulSoup(resp.text, "html.parser")
        quotes = soup.find_all(class_="quote")

        for quote in quotes:
            text   = quote.find(class_="text").get_text()
            author = quote.find(class_="author").get_text()
            bio    = quote.find("a")["href"]
            
            all_quotes.append({
                "text": text,
                "author": author,
                "bio": bio
            })

        next_btn = soup.find(class_="next")
        url = next_btn.find("a")["href"] if next_btn else None
        #sleep(2)

    return all_quotes
   

def write_quotes(quotes):
    # write quotes to a csv file
    with open("quotes.csv", "w", encoding='utf-8') as file:
        headers = ["text", "author", "bio"]
        csv_writer = DictWriter(file, fieldnames=headers)
        csv_writer.writeheader()

        for quote in quotes:
            csv_writer.writerow(quote)


quotes = scrape_quotes()
write_quotes(quotes)