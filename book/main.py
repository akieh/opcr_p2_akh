from utils import soup

book_example = "http://books.toscrape.com/catalogue/scott-pilgrims-precious-little-life-scott-pilgrim-1_987/index.html"


def main():
    print("Récupération de livre")
    a_soup = soup.create_soup(book_example)
    info_book = []
