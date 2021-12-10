import requests
from bs4 import BeautifulSoup

url = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
url_base = 'http://books.toscrape.com/'


def recuperation_informations_page_livre(url_page_livre):

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
            str(url_base) + str(block_image).split('"')[5].split('../../')[1]
        )

        # Avis ('review_rating')
        block_avis = soup.find('div', class_='col-sm-6 product_main')
        review_rating_string = str(block_avis.find_all('p')[2]).split('"')[1].split(' ')[1]
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

        return(data)

    else:
        return str("Message d'erreur : réponse à la requête négative. Revoir url.")


print(recuperation_informations_page_livre(url))
