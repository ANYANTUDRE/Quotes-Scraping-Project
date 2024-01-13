import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice

BASE_URL   = "https://quotes.toscrape.com/"


def scrape_quotes():
    all_quotes = list()
    url        = "/page/1/"
    while url:
        resp = requests.get(f"{BASE_URL}{url}")
        print(f"Now Scraping {BASE_URL}{url} ......")
        #print(resp.text)
        soup = BeautifulSoup(resp.text, "html.parser")
        quotes = soup.find_all(class_="quote")
        #print(quotes)

        for quote in quotes:
            text   = quote.find(class_="text").get_text()
            author = quote.find(class_="author").get_text()
            bio    = quote.find("a")["href"]
            #print(bio)
            all_quotes.append({
                "text": text,
                "author": author,
                "bio": bio
            })

        next_btn = soup.find(class_="next")
        url = next_btn.find("a")["href"] if next_btn else None
        #sleep(2)

    return all_quotes
    
def start_game(quotes):
    quote = choice(quotes)
    remaining_guesses = 4
    guess = ""
    print("Here's a quote: ")
    print(quote["text"])
    print(quote["author"])

    while guess.lower() != quote["author"].lower() and remaining_guesses > 0:
        guess = input(f"Who said this quote? Guesses remaining: {remaining_guesses} \n")
        remaining_guesses -= 1

        if guess.lower() == quote["author"].lower():
            print("YOU GOT IT RIGHT BRUHHH !!!")
            
        elif remaining_guesses == 3:
            res  = requests.get(f"{BASE_URL}{quote['bio']}")
            soup = BeautifulSoup(res.text, "html.parser")
            #print(soup.body)
            birth_date = soup.find(class_="author-born-date").get_text()
            birth_location = soup.find(class_="author-born-location").get_text()
            print(f"Here's a hint for you : The author was born on {birth_date} {birth_location}")

        elif remaining_guesses == 2:
            first_initial = quote['author'][0]
            print(f"Here's a hint : The author's first name starts with: {first_initial}")
        
        elif remaining_guesses == 1:
            last_inital = quote['author'].split(" ")[1][0]
            print(f"Here's a hint : The author's last name starts with: {last_inital}")
        else: 
            print(f"Sorry you ran out of guesses. The answer was {quote['author']}")

    again = " "
    while again.lower() not in ('y', 'yes', 'n', 'no'):
        again = input("Would you like to play again (yes/no)?")

    if again.lower() in ('y', 'yes'):
        print("Ok you play again!")
        return start_game(quotes)
    else:
        print("Ok, goodbye!")

quotes = scrape_quotes()
start_game(quotes)