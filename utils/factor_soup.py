from bs4 import BeautifulSoup
import requests

""" Création d'un objet soup qui sera utilisé dans les classes
book.py et category.py
"""


def create_soup(url):
    reponse = requests.get(url)
    if reponse.ok:
        print ("Récupération de l'URL")
        page = reponse.content
        soup = BeautifulSoup(page, "html.parser")
    else:
        print(reponse.raise_for_status())
    return soup
