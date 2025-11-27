import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# --- CONFIGURATION ---
BASE_URL = "http://quotes.toscrape.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def scraper_page():
    print("--- 1. COLLECTE (Requests) ---")
    # On simule un navigateur pour ne pas être bloqué (OPSEC de base)
    reponse = requests.get(BASE_URL, headers=HEADERS)

    if reponse.status_code != 200:
        print(f"Erreur de connexion : {reponse.status_code}")
        return

    print(f"Statut : {reponse.status_code} (OK)")

    print("\n--- 2. EXTRACTION (BeautifulSoup) ---")
    # On transforme le HTML brut en arbre navigable
    soup = BeautifulSoup(reponse.text, 'html.parser')

    # On cherche toutes les boîtes "div" qui ont la classe "quote"
    blocs_citations = soup.find_all('div', class_='quote')
    print(f"Nombre de citations trouvées : {len(blocs_citations)}")

    donnees_extraites = []

    for bloc in blocs_citations:
        # Extraction du texte de la citation
        texte = bloc.find('span', class_='text').text

        # Extraction de l'auteur
        auteur = bloc.find('small', class_='author').text

        # Extraction des tags (liste)
        tags_meta = bloc.find('div', class_='tags').find_all('a', class_='tag')
        tags = [tag.text for tag in tags_meta]

        # On stocke ça proprement dans un dictionnaire
        item = {
            "Citation": texte,
            "Auteur": auteur,
            "Tags": ", ".join(tags)  # On joint les tags par des virgules
        }
        donnees_extraites.append(item)
        print(f"-> Récupéré : {auteur}")

    print("\n--- 3. STOCKAGE (Pandas) ---")
    # On transforme la liste en DataFrame (Tableau Excel-like)
    df = pd.DataFrame(donnees_extraites)

    # Affichage d'un aperçu
    print("Aperçu des données :")
    print(df.head())

    # Export vers CSV (Compatible Excel et Maltego)
    nom_fichier = "resultats_quotes.csv"
    df.to_csv(nom_fichier, index=False, encoding='utf-8-sig')
    print(f"\n[SUCCÈS] Données sauvegardées dans '{nom_fichier}'")


if __name__ == "__main__":
    scraper_page()