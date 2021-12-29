import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

## objet à manier
url_site = "http://books.toscrape.com/"
url_book = "http://books.toscrape.com/catalogue/scott-pilgrims-precious-little-life-scott-pilgrim-1_987/index.html"
reponse = requests.get(url_book)
page = reponse.content
soup = BeautifulSoup(page, "html.parser")
## header pour le excel
en_tete = ["Product Page URL", "UPC", "Title", "Price including tax", "Price excluding tax", "Number available",
           "Product description",
           ]
## "Category", "Review_rating", "Image URL"] à ajouter après Product description
info_book = []

# récupération du tableau des infos du livre
info_tableau = []
product_table = soup.find("table", class_="table table-striped")
product_table_headers = product_table.find_all("th")

for header in product_table_headers:
    if header.text == "UPC" \
    or header.text == "Price (excl. tax)" \
    or header.text == "Price (incl. tax)" \
    or header.text == "Availability":
        info_tableau.append(header.find_next('td').text)


##récupération de la description du produit dans le tableau
product_description = soup.find(id="product_description")
description_livre = product_description.find("h2").find_next('p').text

#récupération titre du livre et son rating
product_main = soup.find (class_="col-sm-6 product_main")
titre_livre = product_main.find("h1").text
##print("le titre du livre ouais: ", titre_livre)
rating_livre = product_main.find_all()

#récupération catégorie du livre
bandeau_livre = soup.find("ul", class_="breadcrumb").findAllNext

#récupération de l'url de l'image
image_source = soup.find(class_="item active").img['src']
url_image = url_site + image_source[6:]
print (image_source)
print ("L'URL de l'image: ", url_image)

#Présentation données du livre
info_book.append(url_book) # URL du livre
info_book.append(info_tableau[0]) # UPC du livre
info_book.append(titre_livre) # titre du livre
info_book.append(info_tableau[1]) # Prix tax excl du livre
info_book.append(info_tableau[2]) # Prix tax incl du livre
info_book.append(info_tableau[3]) # quantité dispo du livre
info_book.append(description_livre) # description du livre

print ("les infos du livre: ", info_book)

#chargement des données dans un fichier
book = pd.DataFrame([info_book], columns=en_tete)
print ("Chargement des données du livre dans un fichier en cours ...")
book.to_csv('resultatbook/book.csv', index=False, encoding='utf-8')
print ("Terminé.")

