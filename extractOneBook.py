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
def createSoup (url):
    reponse = requests.get(url)
    page = reponse.content
    soup = BeautifulSoup(page, "html.parser")
    return soup

def getInfoBook (url):
    print ("*************** GETINFO BOOK ********************")
    soup = createSoup(url)
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

def getUrlCategoryBooks (url):
    print ("\n \n \n *************** GETURLCATEGORYBOOKS ******************** \n \n \n")

    soup = createSoup(url)
    if soup.find(class_="next"):
        page_url = soup.find(class_="next")
        page_urll = page_url.find(href=True)
        print("there is a next\n")
        for ele in enumerate (url):
            print (ele)
        print ("l'URL",url[:68]+page_urll['href'] ,"\n\n\n")
    else:
        print("there is no next pages")

    table_books = soup.find("ol", class_="row")
    url_all_books_category = table_books.find_all(href=True)
    url_all_books = []
    for url in url_all_books_category:
        url_all_books.append(url_site + "catalogue/" + url['href'][9:])

    url_all_books = list(dict.fromkeys(url_all_books))
    """for url_book in enumerate(url_all_books):
        print(url_book)
    print ("Extraction des URL fini")"""

    return url_all_books

#chargement des données dans un fichier


def get_multiple_url_pages (urlcategory):
    print ("\n *************** TEST MULTIPLE URL PAGES ************ \n\n")
    multiplepage_url = [urlcategory]
    soup = createSoup(urlcategory)
    while soup.find(class_="next"):
        next_page_url = soup.find(class_="next").find(href=True)
        new_page_url = urlcategory[:68]+next_page_url['href']
        print ("La nouvelle page:", new_page_url)
        multiplepage_url.append(new_page_url)
        print (urlcategory[:68]+next_page_url['href'])
        soup = createSoup(new_page_url)
    print("\nPrésentation des url\n")
    for url in multiplepage_url:
        print (url)
    print("\n *************** TEST FINI ************ \n\n")


def get_single_page_categorybooks (url):
    soup = createSoup(url)
    table_books = soup.find("ol", class_="row")
    url_all_books_category = table_books.find_all(href=True)
    url_all_books = []
    for url in url_all_books_category:
        url_all_books.append(url_site + "catalogue/" + url['href'][9:])

    url_all_books = list(dict.fromkeys(url_all_books))
    """for url_book in enumerate(url_all_books):
        print(url_book)
    print ("Extraction des URL fini")"""

    return url_all_books

    print ("test")

def loadBooksCSV (info_book):
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
#johnny = getInfoBook(url_book)

get_multiple_url_pages(url_category)
