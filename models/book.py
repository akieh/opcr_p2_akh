from bs4 import BeautifulSoup
from utils import factor_soup


class Book:

    def __init__(self, url, upc, title, price_tax_excl, price_tax_incl, quantity, description,
                 category, rating, url_image):
        self.url = url,
        self.upc = upc,
        self.title = title,
        self.price_tax_excl = price_tax_excl
        self.price_tax_incl = price_tax_incl
        self.quantity = quantity
        self.description = description
        self.category = category
        self.rating = rating
        self.url_image = url_image

    @classmethod
    def from_list(cls, info_book):
        url, upc, title, price_tax_excl, price_tax_incl, quantity, description, category, rating, url_image = info_book
        return cls(url, upc, title, price_tax_excl, price_tax_incl, quantity, description, category, rating, url_image)
