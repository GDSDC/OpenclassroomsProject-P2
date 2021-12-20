from typing import Any, Dict, List
from time import time

import requests
from bs4 import BeautifulSoup
import csv
import os

repertoire_de_travail = str(os.path.dirname(os.path.realpath(__file__)))
books_home_url = 'https://books.toscrape.com/catalogue/category/books_1/index.html'


def timing_decorator(func):
    def timing_function(*args):
        start = time() # Initialisation Timer
        return func(*args) # Exécution fonction
        end = time() # Finalisation Timer
        print(f'Temps écoulé pour {func.__name__}: {end - start} secondes') # Print temps écoulé pour l'éxécution de la fonction
    return timing_function


def recuperation_informations_page_livre(url_page_livre: str) -> Dict[str, str]:
    '''Fonction permettant d'extraire les informations d'un livre dans une liste en sortie à partir de son url.'''

    # Initialisation requête + data
    response = requests.get(url_page_livre)

    data = {
        'product_page_url': '',
        'universal_product_code': '',
        'title': '',
        'price_including_tax': '',
        'price_excluding_tax': '',
        'number_available': '',
        'product_description': '',
        'category': '',
        'review_rating': '',
        'image_url': '',
    }

    # Récupération des informations
    if response.ok:
        # URL de la page produit ('product_page_url')
        data['product_page_url'] = str(url_page_livre)

        # HTML PARSER
        soup = BeautifulSoup(response.text, 'html.parser')

        # Titre du livre ('title')
        block_titre = soup.find_all('div', class_='col-sm-6 product_main')
        data['title'] = str(block_titre[0].find('h1').text)

        # Traitement du block 'Product Information'
        block_information_produit = soup.find('table', class_='table table-striped')
        block_information_produit_lignes = block_information_produit.find_all('tr')
        # Recherche dans le block 'Product Information'
        for ligne in block_information_produit_lignes:
            # UPC ('universal_product_code')
            if ligne.find('th').text == 'UPC':
                data['universal_product_code'] = str(ligne.find('td').text)
            # Price (incl. tax) ('price_including_tax')
            elif ligne.find('th').text == 'Price (incl. tax)':
                data['price_including_tax'] = str(ligne.find('td').text[1:])
            # Price (excl. tax) ('price_excluding_tax')
            elif ligne.find('th').text == 'Price (excl. tax)':
                data['price_excluding_tax'] = str(ligne.find('td').text[1:])
            # Availability ('price_excluding_tax')
            elif ligne.find('th').text == 'Availability':
                data['number_available'] = str(
                    ligne.find('td').text.split('(')[1].split(' ')[0]
                )

        # Description Produit ('product_description')
        blocks_texte = soup.find_all('p')
        data['product_description'] = str(blocks_texte[3].text)

        # Catégorie ('category')
        block_categories = soup.find('ul', class_='breadcrumb')
        data['category'] = str(block_categories.find_all('li')[2].find('a').text)

        # URL de l'image ('image_url')
        block_image = soup.find('div', class_='item active')
        data['image_url'] = str(
            'http://books.toscrape.com/'
            + str(block_image).split('"')[5].split('../../')[1]
        )

        # Récupération image de couverture
        telechargement_image_livre(data['image_url'], data['universal_product_code'])


        # Avis ('review_rating')
        block_avis = soup.find('div', class_='col-sm-6 product_main')
        review_rating_string = (
            str(block_avis.find_all('p')[2]).split('"')[1].split(' ')[1]
        )
        review_rating = ''
        if review_rating_string == 'One':
            review_rating = 1
        elif review_rating_string == 'Two':
            review_rating = 2
        elif review_rating_string == 'Three':
            review_rating = 3
        elif review_rating_string == 'Four':
            review_rating = 4
        elif review_rating_string == 'Five':
            review_rating = 5
        data['review_rating'] = str(review_rating)

        return data


def telechargement_image_livre(image_url_value: str, upc_value: str):
    '''Fonction permettant de télécharger l'image de couverture du livre correspondant à l'url du livre en entrée.
    Toutes les images de couvertures seront placées dans le dossier '/Donnees_Resultat/Couvertures' présant dans le dossier de travail.
    Toutes les images de couvertures seront nommées par la valeur de l'UPC.'''


    # Création Dossier 'Couvertures' si nécessaire dans le dossier 'Donnees_Resultat'
    if os.path.exists(repertoire_de_travail + '/Donnees_Resultat' + '/Couvertures') == False:
        os.makedirs(repertoire_de_travail + '/Donnees_Resultat' + '/Couvertures')

    # Enregistrement de l'image de couverture
    r = requests.get(image_url_value, allow_redirects=True)
    image_path = repertoire_de_travail + '/Donnees_Resultat' + '/Couvertures' + '/' + upc_value + '.jpeg'
    open(image_path, 'wb').write(r.content)


def ecriture_csv(categorie_livre: str, liste_donnees_par_livre: List[Dict[str, str]]):
    '''Fonction pour créer le fichier CSV pour une catégorie donnée.
    Le fichier portera le nom de la catégorie entrée en argument.'''

    headers_csv = [
        'product_page_url',
        'universal_product_code',
        'title',
        'price_including_tax',
        'price_excluding_tax',
        'number_available',
        'product_description',
        'category',
        'review_rating',
        'image_url',
    ]

    # Création Dossier 'Donnees_Resultat' si nécessaire dans le répertoire de travail
    if os.path.exists(repertoire_de_travail + '/Donnees_Resultat') == False:
        os.makedirs(repertoire_de_travail + '/Donnees_Resultat')

    # Création du CSV portant le nom de la catégorie et écriture des entêtes
    nom_du_csv = repertoire_de_travail + '/Donnees_Resultat/' + str(categorie_livre) + '.csv'
    print(f'Ecriture du csv {nom_du_csv}')

    with open(nom_du_csv, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers_csv)
        writer.writeheader()
        writer.writerows(liste_donnees_par_livre)

    print(f'{len(liste_donnees_par_livre)} livres écrits pour la catégorie {categorie_livre}.')


def extraire_liste_livres(categorie_livre_url :str) -> List[str]:
    '''Fonction permettant d'obternir en sortie une liste contenant l'url de chacun des livres présents dans la catégorie.
    Cette fonction est récursive pour tenir compte de la pagination.'''

    # Initialisation requête
    response = requests.get(categorie_livre_url)

    # Récupération des informations
    if response.ok:

        # HTML PARSER
        soup = BeautifulSoup(response.text, 'html.parser')

        # Recherche des url de livres
        blocks_livres = soup.find_all(
            'li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3'
        )
        donnees_liste_livre = []
        for livre in blocks_livres:
            donnees_liste_livre.append(
                str(
                    'http://books.toscrape.com/catalogue/'
                    + str(livre).split('"')[7].split('../../../')[1]
                )
            )

        # Detection page 'Next' et itération
        block_url_page_suivante = soup.find_all('li', class_='next')
        if block_url_page_suivante != []:
            url_livre_base = ''
            url_livre_base_liste = categorie_livre_url.split('/')[:-1]
            for element in url_livre_base_liste:
                url_livre_base += str(element) + '/'
            donnees_liste_livre += extraire_liste_livres(
                url_livre_base + str(block_url_page_suivante[0]).split('"')[3]
            )

        return donnees_liste_livre

def ecriture_categorie(categorie_livre_url :str):
    '''Function permettant d'extraire toutes les informations de tous les livres d'un même catégorie.
    Toutes ces informations seront écrites sur un même fichier CSV portant le nom de la categorie'''

    # Extraire liste des url de livres
    liste_livre = extraire_liste_livres(categorie_livre_url)

    # Inititalisation CSV par catégorie
    categorie: str = recuperation_informations_page_livre(liste_livre[0])['category']

    # Itération sur tous les livres dans la catégorie
    donnees_par_livre = []
    for livre in liste_livre:
        donnees_par_livre.append(recuperation_informations_page_livre(livre))

    ecriture_csv(categorie, donnees_par_livre)

def extraire_list_categorie_url_extraction(contenu_html: str) -> List[str]:
    # HTML PARSER
    soup = BeautifulSoup(contenu_html, 'html.parser')
    liste_categorie = []

    # Block Liste de categorie
    block_categories = soup.find('ul', class_='nav nav-list')
    block_categories_lignes = block_categories.find_all('a')

    # Itération sur chaque categorie
    for categorie in range(1, len(block_categories_lignes)):
        liste_categorie.append(
            str(
                'https://books.toscrape.com/catalogue/category/'
                + str(block_categories_lignes[categorie])
                .split('"')[1]
                .split('../')[1]
            )
        )
    return liste_categorie

def extraire_liste_categorie_url() -> List[str]:
    '''Function permettant d'extraire dans une liste l'ensemble des categories disponibles sous forme d'url.'''

    # Initialisation requête + liste_categorie
    response = requests.get(books_home_url)
    # Récupération des informations
    if response.ok:
        categories = extraire_list_categorie_url_extraction(response.text)
        return categories

def extraire_tout():
    '''Fonction permettant d'extraire les informations de tous les produits parmis toutes les catégories du site'''

    # Extraction de la liste des catégories
    print(f"Début de l'extraction des catégories")
    liste_categorie = extraire_liste_categorie_url()
    print(f"{len(liste_categorie)} catégories extraites")
    print('------ Traitement par catégorie ------')

    # Extraction des informations de tous les livres pour chaque catégorie
    for categorie_url in liste_categorie[:2]:
        print(f"Traitement de la catégorie {categorie_url}")
        ecriture_categorie(categorie_url)
        print('------------')


if __name__ == '__main__':
    extraire_tout()

