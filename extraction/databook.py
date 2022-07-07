from utils import factor_soup
from models.book import Book

book_example = "http://books.toscrape.com/catalogue/scott-pilgrims-precious-little-life-scott-pilgrim-1_987/index.html"
url_site = "http://books.toscrape.com/"


def rating_book(product_main):
    #récupération du dictionnaire d'élément HTML qui compose les éléments du rating
    rating_dict = product_main.find(class_="star-rating").attrs['class']
    rating = rating_dict[-1]
    if rating == "Five":
        rating = "5/5"
    elif rating == "Four":
        rating = "4/5"
    elif rating == "Three":
        rating = "3/5"
    elif rating == "Two":
        rating = "2/5"
    else:
        rating = "1/5"
    return rating


def info_tableau_book(product_table):
    info_tableau = []
    product_table_headers = product_table.find_all("th")
    for header in product_table_headers:
        if header.text == "UPC" \
                or header.text == "Price (excl. tax)" \
                or header.text == "Price (incl. tax)" \
                or header.text == "Availability":
            info_tableau.append(header.find_next('td').text)
    return info_tableau


def extract_book(url_book):
    soup = factor_soup.create_soup(url_book)
    info_book = [url_book]
    product_table = soup.find("table", class_="table table-striped")
    info_book.extend(info_tableau_book(product_table))
    info_book.insert(2, soup.find(class_="col-sm-6 product_main").find("h1").text)
    product_main = soup.find(class_="col-sm-6 product_main")
    product_description = soup.find(id="product_description")
    if product_description is None:
        info_book.append("Pas de description disponible")
    else:
        info_book.append(product_description.find("h2").find_next('p').text)
    #category
    info_book.append(soup.find("li", class_="active").find_previous().text)
    info_book.append(rating_book(product_main))
    image_source = soup.find(class_="item active").img['src']
    info_book.append(url_site + image_source[6:])
    book = Book.from_list(info_book)
    return book


extract_book(book_example)
