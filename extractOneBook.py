import requests
from bs4 import BeautifulSoup
import csv

## objet à manier
url = "http://books.toscrape.com/catalogue/scott-pilgrims-precious-little-life-scott-pilgrim-1_987/index.html"
reponse = requests.get(url)
page = reponse.content
soup = BeautifulSoup(page, "html.parser")
## header pour le excel
en_tete = ["Product Page URL", "UPC", "Title", "Price including tax", "Price excluding tax", "Number available",
           "Product description",
           "Category", "Review_rating", "Image URL"]
## infos d'un livre
info_book = [url]

#récupération du titre du livre

# récupération du tableau des infos du livre
info_tableau = []
product_table = soup.find("table", class_="table table-striped")
product_table_headers = product_table.find_all("th")

for header in product_table_headers:
    if header.text == "UPC" or header.text == "Price (excl. tax)" or header.text == "Price (incl. tax)" or header.text == "Availability":
        info_tableau.append(header.find_next('td').text)

print ("les données du tableau: ",info_tableau)

##récupération de la description du produit dans le tableau
product_description = soup.find(id="product_description")
description_livre = product_description.find("h2").find_next('p').text
print (description_livre)

#récupération titre du livre et son rating
product_main = soup.find (class_="col-sm-6 product_main")
titre_livre = product_main.find("h1").text
print("le titre du livre ouais: ", titre_livre)
rating_livre = product_main.find_all()
##Présentation données du livre
print ("les infos du livre: ", info_book)
