import requests
from bs4 import BeautifulSoup
import csv


## objet à manier
url_site = "http://books.toscrape.com/"
url_book = "http://books.toscrape.com/catalogue/scott-pilgrims-precious-little-life-scott-pilgrim-1_987/index.html"
url_category = "http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"
"""reponse = requests.get(url_book)
page = reponse.content
soup = BeautifulSoup(page, "html.parser")
"""
def create_soup (url):
    reponse = requests.get(url)
    page = reponse.content
    soup = BeautifulSoup(page, "html.parser")
    return soup

def get_info_book (url):
    print ("*************** GETINFO BOOK ********************")
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
    description_livre = product_description.find("h2").find_next('p').text

    #récupération titre du livre et son rating
    product_main = soup.find (class_="col-sm-6 product_main")
    titre_livre = product_main.find("h1").text
    rating_livre = product_main.find(class_="star-rating")
    print ("!!!!!!!!!!!" ,rating_livre)

    #print ("le rating livre bis: ", rating_livre)

    #récupération catégorie du livre
    categorie_livre = ""
    bandeau_livre = soup.find("ul", class_="breadcrumb")
    """for ele in bandeau_livre:
        if '<li> <a href="../category/books/sequential-art_5/index.html">Sequential Art</a> </li>' in ele:
            print ("OUI IL Y A ")
        else:
            print ("nan y'a pas")
        print (ele)
    print("LA CATEGORIE DU LIVRE ",categorie_livre)
    """


    #récupération de l'url de l'image
    image_source = soup.find(class_="item active").img['src']
    url_image = url_site + image_source[6:]
    #print ("L'URL de l'image: ", url_image)

    #Présentation données du livre
    info_book.append(url_book) # URL du livre
    info_book.append(info_tableau[0]) # UPC du livre
    info_book.append(titre_livre) # titre du livre
    info_book.append(info_tableau[1]) # Prix tax excl du livre
    info_book.append(info_tableau[2]) # Prix tax incl du livre
    info_book.append(info_tableau[3]) # quantité dispo du livre
    info_book.append(description_livre) # description du livre

    print("Les infos du livre dans la fonction: ", info_book)

    return info_book

##Récupération des URL des livre d'une catégorie
def get_url_category_books (url_liste):
    print ("\n *************** Extraction DES URL DE CHAQUE LIVRES ******************** \n")
    print (f"\n *************** Extraction de l'url {url_liste} ******************** \n")
    url_pages = [url_liste]
    url_category_books = []
    multiple_url_pages = []
    all_url_category_books = []
    soup = create_soup(url_liste)
    if soup.find(class_="next"):
        multiple_url_pages = get_multiple_url_pages(url_liste)
        #url_pages.append(multiple_url_pages)
        #url_pages = list(dict.fromkeys(url_pages))
        print ("URL des pages: ", multiple_url_pages ,"********\n\n")
        #print ("Affichage url_pages[1][1]",url_pages[1][2])
    for url in multiple_url_pages:
        print ("Ca boucle ...")
        all_url_category_books = get_single_page_category_books(url)
        url_category_books.extend(all_url_category_books)
    for ele in enumerate(url_category_books):
        print (ele)
    #print ("Voici le contenu de all_url_category_books:", url_category_books)
    print ("\n *************** EXTRACTION DES URL DES LIVRES TERMINEE ************ \n")

    return url_category_books

def get_multiple_url_pages (urlcategory):
    print ("\n *************** RECUPERATION DE MULTIPLE URL PAGES ************ \n")
    multiplepage_url = [urlcategory]
    soup = create_soup(urlcategory)
    while soup.find(class_="next"):
        next_page_url = soup.find(class_="next").find(href=True)
        new_page_url = urlcategory[:68]+next_page_url['href']
        multiplepage_url.append(new_page_url)
        soup = create_soup(new_page_url)
    for url in enumerate (multiplepage_url):
        print (url)
    print("\n *************** RECUPERATION DES URL DE PLUSIEURS PAGES TERMINEE ************ \n")
    return multiplepage_url

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

def load_books_csv (info_book):
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

#loadBooksCSV(johnny)
#johnny = get_info_book (url_book)

#url_category = get_single_page_category_books(url_category)
#print (url_category)
#get_single_page_category_books(url_category)
get_url_category_books(url_category)
#get_multiple_url_pages(url_category)