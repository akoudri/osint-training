#!/usr/bin/env python3
"""
Maltego Transform: Twitter/X Alias to Profile URL
Converts a Twitter/X username/alias to profile URL with validation and metadata
"""

import sys
import re
from maltego_trx.maltego import MaltegoTransform, MaltegoMsg

def validate_twitter_alias(alias):
    """
    Valide le format d'un alias Twitter/X

    Args:
        alias (str): L'alias à valider

    Returns:
        tuple: (is_valid, cleaned_alias, error_message)
    """
    if not alias:
        return False, "", "L'alias ne peut pas être vide"

    # Nettoyer l'alias (retirer @ si présent, espaces, etc.)
    cleaned = alias.strip().lstrip('@')

    # Validation selon les règles Twitter:
    # - 1 à 15 caractères
    # - Lettres, chiffres, underscore uniquement
    # - Ne peut pas être "mentions" ou "settings" (réservés)
    if not cleaned:
        return False, "", "L'alias ne contient que des caractères invalides"

    if len(cleaned) > 15:
        return False, cleaned, f"L'alias est trop long ({len(cleaned)} > 15 caractères)"

    if not re.match(r'^[A-Za-z0-9_]+$', cleaned):
        return False, cleaned, "L'alias contient des caractères invalides (seuls a-z, 0-9, _ sont autorisés)"

    # Noms réservés par Twitter
    reserved_names = ['mentions', 'settings', 'home', 'notifications', 'messages']
    if cleaned.lower() in reserved_names:
        return False, cleaned, f"'{cleaned}' est un nom réservé par Twitter/X"

    return True, cleaned, ""

def main():
    """Point d'entrée principal de la transform"""

    # 1. Initialisation de l'objet de réponse Maltego
    response = MaltegoTransform()

    try:
        # 2. Récupération de l'argument (L'input de l'entité)
        if len(sys.argv) < 2:
            response.addUIMessage(
                "Erreur: Aucun argument reçu. Utilisez: python twitter_transform.py <alias>",
                messageType="FatalError"
            )
            print(response.returnOutput())
            sys.exit(1)

        input_alias = sys.argv[1]

        # 3. Validation de l'alias
        is_valid, cleaned_alias, error_msg = validate_twitter_alias(input_alias)

        if not is_valid:
            response.addUIMessage(
                f"Alias invalide: {error_msg}",
                messageType="PartialError"
            )
            # On retourne quand même un résultat mais avec un warning
            if cleaned_alias:
                response.addUIMessage(
                    f"Tentative avec l'alias nettoyé: {cleaned_alias}",
                    messageType="Inform"
                )
            else:
                print(response.returnOutput())
                sys.exit(1)
        else:
            # Message de succès
            if input_alias != cleaned_alias:
                response.addUIMessage(
                    f"Alias nettoyé: '{input_alias}' → '{cleaned_alias}'",
                    messageType="Inform"
                )

        # 4. Construction de l'URL du profil
        twitter_url = f"https://x.com/{cleaned_alias}"

        # 5. Création de l'Entité de Sortie (maltego.URL)
        entity = response.addEntity("maltego.URL", twitter_url)

        # 6. Ajout de propriétés enrichies pour Maltego
        entity.addProperty("url", "URL", "strict", twitter_url)
        entity.addProperty("short-title", "Title", "loose", f"Profil X de @{cleaned_alias}")
        entity.addProperty("title", "Full Title", "loose", f"Twitter/X Profile: @{cleaned_alias}")

        # Propriétés additionnelles pour contexte OSINT
        entity.addProperty("twitter.alias", "Twitter Alias", "strict", cleaned_alias)
        entity.addProperty("twitter.handle", "Twitter Handle", "strict", f"@{cleaned_alias}")

        # URLs alternatives utiles pour OSINT
        entity.setLinkLabel(f"@{cleaned_alias}")
        entity.setLinkColor("0x0000FF")  # Bleu pour Twitter
        entity.setBookmark(0)  # Bookmark pour référence rapide

        # Notes pour l'analyste
        entity.setNote(
            f"Profil Twitter/X: @{cleaned_alias}\n"
            f"URL: {twitter_url}\n\n"
            f"URLs OSINT additionnelles:\n"
            f"- Recherche tweets: https://x.com/search?q=from:{cleaned_alias}\n"
            f"- Avec réponses: https://x.com/search?q=from:{cleaned_alias}+filter:replies\n"
            f"- Média: https://x.com/{cleaned_alias}/media\n"
            f"- Likes: https://x.com/{cleaned_alias}/likes"
        )

        # 7. Envoi du résultat à Maltego (STDOUT)
        print(response.returnOutput())

    except Exception as e:
        # Gestion d'erreur globale
        response.addUIMessage(
            f"Erreur inattendue: {str(e)}",
            messageType="FatalError"
        )
        print(response.returnOutput())
        sys.exit(1)

if __name__ == "__main__":
    main()