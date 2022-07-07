from utils import factor_soup
from models import category

books_to_scrap_url = "http://books.toscrape.com/"


def get_links_categories(url_site):
    soup = factor_soup.create_soup(url_site)
    url_categories = soup.find("ul", class_="nav nav-list").find_all(href=True)
    url_categories.pop(0)
    categories = []
    for url in url_categories:
        """Ici, je dois créer des objets "category" en boucle
        qui prendront l'URL de la catégorie et son nom.
        """
        objet = category.Category(url_site+"catalogue" + url['href'][9:], url.text.strip())
        categories.append(objet)
    return categories


categories = get_links_categories(books_to_scrap_url)

for el in category.Category.list_category:
    print(vars(el))

