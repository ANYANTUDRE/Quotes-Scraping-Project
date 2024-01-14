import requests
from bs4 import BeautifulSoup
from random import choice
from csv import DictReader


BASE_URL   = "https://quotes.toscrape.com/"

def read_quotes(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        csv_reader = DictReader(f)
        quotes = list(csv_reader)
        return quotes


def start_game(quotes):
    quote = choice(quotes)
    remaining_guesses = 4
    guess = ""
    print("Here's a quote: ")
    print(quote["text"])
    print(quote["author"])

    while guess.lower() != quote["author"].lower() and remaining_guesses > 0:
        guess = input(f"Who said this quote? \n Guesses remaining: {remaining_guesses} \n")
        remaining_guesses -= 1

        if guess.lower() == quote["author"].lower():
            print("YOU GOT IT RIGHT BRUHHH !!!")
            
        elif remaining_guesses == 3:
            res  = requests.get(f"{BASE_URL}{quote['bio']}")
            soup = BeautifulSoup(res.text, "html.parser")
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
            print(f"Sorry you ran out of guesses.\n The answer was {quote['author']}")

    again = " "
    while again.lower() not in ('y', 'yes', 'n', 'no'):
        again = input("Would you like to play again (yes/no)?")

    if again.lower() in ('y', 'yes'):
        print("Ok you play again!")
        return start_game(quotes)
    else:
        print("Ok, goodbye!")


quotes = read_quotes("quotes.csv")
start_game(quotes)