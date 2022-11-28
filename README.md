<h3 align="center">
    <img alt="Logo" title="#logo" width="236px" src="/assets/1600779540759_Online bookstore-01.png">
    <br>
</h3>

# OpenClassrooms Projet P2

- [Objectif](#obj)
- [Compétences](#competences)
- [Technologies](#techs)
- [Requirements](#reqs)
- [Architecture](#architecture)
- [Configuration locale](#localconfig)

<a id="obj"></a>

## Objectif

Books Online est une importante librairie en ligne spécialisée dans les livres d'occasion.
À l'origine, Books Online essayait de suivre manuellement les prix des livres d'occasion sur les sites web de ses
concurrents, mais cela représentait trop de travail : il y a trop de livres et trop de librairies en ligne !
L'objectif de ce projet est d'automatiser cette tâche laborieuse via un programme (un scraper) développé en Python,
capable d'extraire les informations tarifaires d'autres librairies en ligne.

<a id="competences"></a>

## Compétences acquises

- Gérer les données à l'aide du processus ETL
- Utiliser le contrôle de version avec Git et GitHub
- Appliquer les bases de la programmation en Python

<a id="techs"></a>

## Technologies Utilisées

- [Python3](https://www.python.org/)
- [Web Scrapping](https://fr.wikipedia.org/wiki/Web_scraping)

<a id="reqs"></a>

## Requirements

- beautifulsoup4
- certifi
- charset-normalizer
- idna
- requests
- soupsieve
- urllib3

<a id="architecture"></a>

## Architecture et répertoires

```
Project
├── scrapper.py : script principal
├── requirements.txt
│
├── donnees_resultat : répertoire contenant les résultats après lancement du script

```

<a id="localconfig"></a>

## Configuration locale

## Installation

### 1. Récupération du projet sur votre machine locale

Clonez le repository sur votre machine.

```bash
git clone https://github.com/GDSDC/OpenclassroomsProject-P2.git
```

Accédez au répertoire cloné.
```bash
cd OpenclassroomsProject-P2
```

### 2. Création d'un environnement virtuel

Créez l'environnement virtuel env.

```bash
python3 -m venv env
```

### 3. Activation et installation de votre environnement virtuel

Activez votre environnement virtuel env nouvellement créé.

```bash
source env/bin/activate
```

Installez les paquets présents dans la liste requirements.txt

```bash
pip install -r requirements.txt
```

## Utilisation

Lancer simplement le script python scraper.py présent à la source du dossier de travail.

```bash
python scraper.py
```

## Résultat

Une fois le script exécuté, le résultat se trouve dans le dossier `donnees_resultat/`.
Vous y trouverez les fichiers CSV correspondant aux informations de tous les livres de chaque catégorie de livre
présente sur le site https://books.toscrape.com/index.html. 


