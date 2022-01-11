import requests
from bs4 import BeautifulSoup
import csv
import time
import urllib.request

## objet à manier
url_site = "http://books.toscrape.com/"
url_book = "http://books.toscrape.com/catalogue/scott-pilgrims-precious-little-life-scott-pilgrim-1_987/index.html"
url_book3 = "http://books.toscrape.com/catalogue/robin-war_730/index.html"
url_book2 = "http://books.toscrape.com/catalogue/so-cute-it-hurts-vol-6-so-cute-it-hurts-6_734/index.html"
url_category = "http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"
url_catalogue = "http://books.toscrape.com/catalogue/category/books/"

#Création d'un objet soup
def create_soup (url):
    reponse = requests.get(url)
    page = reponse.content
    soup = BeautifulSoup(page, "html.parser")
    return soup

#Récupération des infos d'un livre
def get_info_book (url):
    #print ("\n*************** Récupération des infos du livre en paramètre ********************\n")
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
    #print ("Le Product description : ", product_description, "Son type: ", type(product_description))
    if product_description is None:
        description_livre = "Pas de description disponible"
    else:
        description_livre = product_description.find("h2").find_next('p').text

    #récupération titre du livre et son rating
    product_main = soup.find (class_="col-sm-6 product_main")
    titre_livre = product_main.find("h1").text
    rating_livre = product_main.find(class_="star-rating")
    print ("Type de Rating:", type(rating_livre))
    print ("La taille du rating:", len(rating_livre))
    leratingdict = rating_livre.attrs['class']
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
    print ("Le type de lerating:", type(leratingdict))
    print("Contenu de leratingdict", leratingdict)
    print ("Contenu de rating:",rating)
    print ("Type de rating,",type(rating))

    """ You can specify a string to be used to join the bits of text together:

     soup.get_text("|")
    'I linked to |example.com|'"""

    #récupération catégorie du livre
    categorie_livre = soup.find("li", class_="active").find_previous().text

    #récupération de l'url de l'image
    image_source = soup.find(class_="item active").img['src']
    url_image = url_site + image_source[6:]
    #print ("L'URL de l'image: ", url_image)

    #téléchargement de l'image
    urllib.request.urlretrieve(url_image, "scott.jpg") # CHECKER CA BIEN !!!!!!!!!!!!
    #Présentation données du livre
    info_book.append(url) # URL du livre
    info_book.append(info_tableau[0]) # UPC du livre
    info_book.append(titre_livre) # titre du livre
    info_book.append(info_tableau[1]) # Prix tax excl du livre
    info_book.append(info_tableau[2]) # Prix tax incl du livre
    info_book.append(info_tableau[3]) # quantité dispo du livre
    info_book.append(description_livre) # description du livre

    #print("\n*************** Fin de récupération des infos du livre ********************\n")

    return info_book

##Récupération des URL des livre d'une catégorie
def get_url_category_books (url_liste):
    print ("\n *************** Extraction DES URL DE CHAQUE LIVRES ******************** \n")
    print (f"\n *************** Extraction de l'url {url_liste} ******************** \n")
    url_category_books = []
    multiple_url_pages = []
    soup = create_soup(url_liste)
    name_category = soup.find(class_="page-header action")
    name_category = name_category.find("h1").text
    print ("Nom de la categorie: ",name_category)
    if soup.find(class_="next"):
        multiple_url_pages = get_multiple_url_pages(url_liste)
        #url_pages.append(multiple_url_pages)
        #url_pages = list(dict.fromkeys(url_pages))
        print ("URL des pages: ", multiple_url_pages ,"********\n\n")
        #print ("Affichage url_pages[1][1]",url_pages[1][2])
    print ("Le contenu de multiple_url_pages: ", multiple_url_pages)
    if len(multiple_url_pages) == 0:
        multiple_url_pages.append(url_liste)
    print ("Le contenu de multiple_url_pages: ", multiple_url_pages)
    print("Ca boucle pour récupérer les url de tous les livres ...")
    for url in multiple_url_pages:
        url_category_books.extend(get_single_page_category_books(url))
        """all_url_category_books = get_single_page_category_books(url)
        url_category_books.extend(all_url_category_books)"""
    print ("Boucle terminée !")
    for ele in enumerate(url_category_books):
        print (ele)
    print ("Voici le contenu de all_url_category_books:", url_category_books)
    print ("\n *************** EXTRACTION DES URL DES LIVRES TERMINEE ************ \n")

    return url_category_books, name_category

#Récupération des URL de plusieurs pages d'une catégorie
def get_multiple_url_pages (urlcategory):
    print ("\n *************** RECUPERATION DE MULTIPLE URL PAGES ************ \n")
    multiplepage_url = [urlcategory]
    soup = create_soup(urlcategory)
    url_category_splitted = url_category.split("/")
    while soup.find(class_="next"):
        next_page_url = soup.find(class_="next").find(href=True)
        #new_page_url = urlcategory[:68]+next_page_url['href']
        new_page_url = urlcategory[:51] + url_category_splitted[-2]+ "/" + next_page_url['href']
        multiplepage_url.append(new_page_url)
        soup = create_soup(new_page_url)
    for url in enumerate (multiplepage_url):
        print (url)
    print("\n *************** RECUPERATION DES URL DE PLUSIEURS PAGES TERMINEE ************ \n")
    return multiplepage_url

#Récupération des URL des livres d'une page
def get_single_page_category_books (url):
    print ("\n *************** RECUPERATION URL DES LIVRES ************ \n")
    soup = create_soup(url)
    table_books = soup.find("ol", class_="row")
    url_all_books_category = table_books.find_all(href=True)
    url_all_books = []
    for url in url_all_books_category:
        url_all_books.append(url_site + "catalogue/" + url['href'][9:])
    url_all_books = list(dict.fromkeys(url_all_books))
    print ("Affichage URL des livres: ", url_all_books)
    print ("\n *************** RECUPERATION URL DES LIVRES TERMINEE ************ \n")
    return url_all_books

def get_links_categories (url_site):
    links_categories = []
    soup = create_soup (url_site)
    table_categories = soup.find ("ul", class_="nav nav-list")
    url_categories = table_categories.find_all(href=True)
    url_categories.pop(0)
    for url in url_categories:
        links_categories.append(url_site+ url['href'])
    for url in enumerate (links_categories):
        print (url)
    return links_categories

#Chargement dans un fichier CSV des informations d'un livre
def load_book_csv (info_book):
    print ("\n \n \n *************** Ecriture des infos du livre dans le fichier CSV ******************** \n \n \n")
    with open('resultatbook/book.csv', 'a',encoding="utf-8") as fichier_csv:

        print("Chargement des données du livre dans un fichier en cours ...")
        writer = csv.writer(fichier_csv, delimiter=',')
        writer.writerow(info_book)
        print("Ecriture des données du livre terminée.")

def one_load_book_csv (info_book):
    print ("\n \n \n *************** LOADING BOOKS INFO IN CSV ******************** \n \n \n")
    with open('resultatbook/book.csv', 'w') as fichier_csv:
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
    print ("\n *************** Ecriture de tous livres d'une catégorie ******************** \n")
    fichier_csv = open('resultatbook/' + str(name_category)+'.csv','w', encoding="utf-8")
    ## header pour le excel
    en_tete = ["Product Page URL", "UPC", "Title", "Price including tax", "Price excluding tax", "Number available",
               "Product description",
               ]
    ## "Category", "Review_rating", "Image URL"] à ajouter après Product description
    writer = csv.writer(fichier_csv, delimiter=',')
    writer.writerow(en_tete)
    for book in (list_books):
        print("Chargement des données du livre dans un fichier en cours ...")
        writer = csv.writer(fichier_csv, delimiter=',')
        writer.writerow(book)
        print("Ecriture des données du livre terminée.")

    print ("\n *************** Ecriture de tous livres d'une catégorie terminée ! ******************** \n")

#Récupération des infos de tous les livres d'une catégorie
def get_category_info_books (url_liste):
    print ("\n *************** Extraction des infos de tous les livres d'une catégorie ******************** \n")
    info_category_books = []
    for url in url_liste:
        print("Ca boucle pour récupérer les infos d'un livre...")
        new_book = get_info_book(url)
        info_category_books.append(new_book)
        #one_load_book_csv(new_book)
    print ("\n *************** Extraction des infos de tous les livres d'une catégorie TERMINEE ******************** \n")

    for info in (info_category_books):
        print (info)
    return info_category_books

def etl():
    print ("Démarrage du programme : ETL de tous les livres du site")
    links_categories = get_links_categories(url_site);

    for link in links_categories:
        list_url, name_category = get_url_category_books(link)
        list_books = get_category_info_books(list_url)
        load_multiple_books(list_books, name_category)

    print ("Fin du programme : Tous les livres ont été chargés en CSV !")


#loadBooksCSV(johnny)
#johnny = get_info_book (url_book)

#url_category = get_single_page_category_books(url_category)
#print (url_category)
#get_single_page_category_books(url_category)
print ("Démarrage du programme ...")
start_time = time.time()
print("--- %s seconds ---" % (time.time() - start_time))
get_info_book(url_book)
#etl()

#get_info_book("http://books.toscrape.com/catalogue/alice-in-wonderland-alices-adventures-in-wonderland-1_5/index.html")

"""liste_url, name_category = get_url_category_books("http://books.toscrape.com/catalogue/category/books/classics_6/index.html")
list_books = get_category_info_books(liste_url)"""

"""book = get_info_book(url_book2)
one_load_book_csv(book)"""

#get_links_categories(url_site)

print ("Fin du programme.")
