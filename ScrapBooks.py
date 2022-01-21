import os
import sys

import requests
import csv
import time
import urllib.request
import string

from bs4 import BeautifulSoup

## objet à manier
url_site = "http://books.toscrape.com/"
#url_book = "http://books.toscrape.com/catalogue/we-are-robin-vol-1-the-vigilante-business-we-are-robin-1_778/index.html"
url_catalogue = "http://books.toscrape.com/catalogue/category/books/"

#Création d'un objet soup
def create_soup (url):
    #print ("Creation du soup pour cet url",url)
    reponse = requests.get(url)
    if reponse.ok:
        page = reponse.content
        soup = BeautifulSoup(page, "html.parser")
    else:
        print (reponse.raise_for_status())
    return soup

#create_soup(url_site)

#Récupération des infos d'un livre
def get_info_book (url):
    soup = create_soup(url)
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

    #récupération de la description du produit dans le tableau
    product_description = soup.find(id="product_description")
    if product_description is None:
        description_livre = "Pas de description disponible"
    else:
        description_livre = product_description.find("h2").find_next('p').text

    #récupération titre du livre et son rating
    product_main = soup.find (class_="col-sm-6 product_main")
    titre_livre = product_main.find("h1").text
    rating_class = product_main.find(class_="star-rating")
    leratingdict = rating_class.attrs['class']
    rating = leratingdict[-1]
    if rating == "Five":
        rating = "5/5"
    elif rating == "Four":
        rating = "4/5"
    elif rating == "Three":
        rating = "3/5"
    elif rating == "Two":
        rating = "2/5"
    else:
        rating == "1/5"

    #récupération catégorie du livre
    categorie_livre = soup.find("li", class_="active").find_previous().text
    #récupération de l'url de l'image
    image_source = soup.find(class_="item active").img['src']
    url_image = url_site + image_source[6:]

    #Ajout des données du livre dans la liste finale
    info_book.append(url) # URL du livre
    info_book.append(info_tableau[0]) # UPC du livre
    info_book.append(titre_livre) # titre du livre
    info_book.append(info_tableau[1]) # Prix tax excl du livre
    info_book.append(info_tableau[2]) # Prix tax incl du livre
    info_book.append(info_tableau[3]) # quantité dispo du livre
    info_book.append(description_livre) # description du livre
    info_book.append(categorie_livre) #categorie du livre
    info_book.append(rating) #notation du livre
    info_book.append(url_image) # url de l'image de couverture du livre

    #enregistrement de l'image du livre en JPG dans un dossier spécifique
    image_file_name = titlebook_to_filename(titre_livre)
    image_book = requests.get(url_image)
    with open(r'imagesbooks/'+str(image_file_name)+".jpg",'wb') as f:
        f.write(image_book.content)

    print ("Extraction du livre ",titre_livre," terminée !")
    return info_book

##Récupération des URL des livre d'une catégorie
def get_url_category_books (url_liste):
    print ("\n *************** Extraction DES URL DE CHAQUE LIVRES DE LA CATEGORIE ******************** \n")
    #print (f"\n *************** Extraction de l'url {url_liste} ******************** \n")
    url_category_books = []
    multiple_url_pages = []
    soup = create_soup(url_liste)
    name_category = soup.find(class_="page-header action")
    name_category = name_category.find("h1").text
    print ("Nom de la categorie: ",name_category)
    if soup.find(class_="next"):
        multiple_url_pages = get_multiple_url_pages(url_liste)
    if len(multiple_url_pages) == 0:
        multiple_url_pages.append(url_liste)
    print("Ca boucle pour récupérer les url de tous les livres ...")
    for url in multiple_url_pages:
        url_category_books.extend(get_single_page_category_books(url))
    print ("Boucle terminée !")
    #print ("Voici le contenu de all_url_category_books:", url_category_books)
    #print ("\n *************** EXTRACTION DES URL DES LIVRES TERMINEE ************ \n")

    return url_category_books, name_category

#Récupération des URL de plusieurs pages d'une catégorie
def get_multiple_url_pages (urlcategory):
    #print ("\n *************** RECUPERATION DE MULTIPLE URL PAGES ************ \n")
    multiplepage_url = [urlcategory]
    soup = create_soup(urlcategory)
    url_category_splitted = urlcategory.split("/")
    while soup.find(class_="next"):
        next_page_url = soup.find(class_="next").find(href=True)
        #new_page_url = urlcategory[:68]+next_page_url['href']
        new_page_url = urlcategory[:51] + url_category_splitted[-2]+ "/" + next_page_url['href']
        multiplepage_url.append(new_page_url)
        soup = create_soup(new_page_url)
    #print("\n *************** RECUPERATION DES URL DE PLUSIEURS PAGES TERMINEE ************ \n")
    return multiplepage_url

#Récupération des URL des livres d'une page
def get_single_page_category_books (url):
    #print ("\n *************** RECUPERATION URL DES LIVRES ************ \n")
    soup = create_soup(url)
    table_books = soup.find("ol", class_="row")
    url_all_books_category = table_books.find_all(href=True)
    url_all_books = []
    for url in url_all_books_category:
        url_all_books.append(url_site + "catalogue/" + url['href'][9:])
    url_all_books = list(dict.fromkeys(url_all_books))
    #print ("Affichage URL des livres: ", url_all_books)
    #print ("\n *************** RECUPERATION URL DES LIVRES TERMINEE ************ \n")
    return url_all_books

def get_links_categories (url_site):
    links_categories = []
    soup = create_soup (url_site)
    table_categories = soup.find ("ul", class_="nav nav-list")
    url_categories = table_categories.find_all(href=True)
    url_categories.pop(0)
    for url in url_categories:
        links_categories.append(url_site+ url['href'])
    return links_categories

#Chargement dans un fichier CSV des informations d'un livre
def load_book_csv (info_book):
    print ("\n \n \n *************** Ecriture des infos du livre dans le fichier CSV ******************** \n \n \n")
    with open('csvbooks/book.csv', 'a',encoding="utf-8") as fichier_csv:

        print("Chargement des données du livre dans un fichier en cours ...")
        writer = csv.writer(fichier_csv, delimiter=',')
        writer.writerow(info_book)
        print("Ecriture des données du livre terminée.")

def one_load_book_csv (info_book):
    print ("\n \n \n *************** LOADING BOOKS INFO IN CSV ******************** \n \n \n")
    with open('csvbooks/book.csv', 'w') as fichier_csv:
        ## header pour le excel
        en_tete = ["Product Page URL", "UPC", "Title", "Price including tax", "Price excluding tax", "Number available",
                   "Product description",
                   ]
        ## "Category", "Review_rating", "Image URL"] à ajouter après Product description
        writer = csv.writer(fichier_csv, delimiter=',')
        writer.writerow(en_tete)
        print("Chargement des données du livre dans un fichier en cours ...")
        writer.writerow(info_book)
        print("Terminé.")

def load_multiple_books (list_books, name_category):
    print (f"\n *************** Ecriture des livres de la catégorie {name_category} en CSV ******************** \n")
    fichier_csv = open('csvbooks/' + str(name_category)+'.csv','w', encoding="utf-8")
    ## header pour le excel
    en_tete = ["Product Page URL", "UPC", "Title", "Price including tax", "Price excluding tax", "Number available",
               "Product description","Category", "Review_rating", "Image URL"]
    writer = csv.writer(fichier_csv, delimiter=',')
    writer.writerow(en_tete)
    for book in (list_books):
        writer = csv.writer(fichier_csv, delimiter=',')
        writer.writerow(book)

    print (f"\n *************** Ecriture de tous livres de la catégorie {name_category} terminée ! ******************** \n")

#Récupération des infos de tous les livres d'une catégorie
def get_category_info_books (url_liste):
    print ("\n *************** Extraction des infos de tous les livres de la catégorie en cours ... ******************** \n")
    info_category_books = []
    for url in url_liste:
        new_book = get_info_book(url)
        info_category_books.append(new_book)
    print ("\n *************** Extraction des infos de tous les livres de la catégorie TERMINEE ******************** \n")
    return info_category_books

#Creation des repertoires pour les images et les CSV
def createDirectories ():
    print ("Creation des dossiers 'imagesbooks' et 'csvbooks'")
    if not os.path.exists("imagesbooks"):
        os.mkdir("imagesbooks")
        print ("Le repetoire 'imagesbooks' a été créé.")
    else:
        print ("Le reportoire 'imagesbooks' existe déjà.")
    if not os.path.exists("csvbooks"):
        os.mkdir("csvbooks")
        print("Le repetoire 'csvbooks' a été créé.")
    else:
        print("Le reportoire 'csvbooks' existe déjà.")

#Changement du nom du livre pour qu'il soit valide dans le téléchargement de l'image
def titlebook_to_filename(titlebook):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in titlebook if c in valid_chars)
    filename = filename.replace(' ','_')
    return filename


def main():
    print ("Démarrage du programme : ETL de tous les livres du site")
    createDirectories()
    links_categories = get_links_categories(url_site)

    for link in links_categories:
        list_url, name_category = get_url_category_books(link)
        list_books = get_category_info_books(list_url)
        load_multiple_books(list_books, name_category)

    print ("Fin du programme : Tous les livres ont été chargés en CSV !")


print ("Démarrage du programme ...")
start_time = time.time()
print("--- %s seconds ---" % (time.time() - start_time))

main()
print ("Fin du programme.")
