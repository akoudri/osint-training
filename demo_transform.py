#!/usr/bin/env python3
"""
Script de démonstration pour tester la transform Twitter
Affiche le résultat XML de manière lisible
"""

import sys
import subprocess

def test_transform(alias):
    """Test la transform avec un alias donné"""
    print(f"\n{'='*60}")
    print(f"Test de la transform avec: '{alias}'")
    print('='*60)

    # Exécuter le script
    result = subprocess.run(
        ['python', 'transforms/twitter_transform.py', alias],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("✅ Exécution réussie\n")
        print("Sortie XML (pour Maltego):")
        print("-" * 60)
        # Afficher le XML avec indentation basique
        xml_lines = result.stdout.strip().split('\n')
        for line in xml_lines:
            # Indentation simple pour lisibilité
            if '<MaltegoMessage>' in line or '</MaltegoMessage>' in line:
                print(line)
            elif '<MaltegoTransformResponseMessage>' in line or '</MaltegoTransformResponseMessage>' in line:
                print('  ' + line)
            elif '<Entities>' in line or '</Entities>' in line:
                print('    ' + line)
            elif '<Entity' in line or '</Entity>' in line:
                print('      ' + line)
            elif '<Value>' in line or '<Weight>' in line:
                print('        ' + line)
            else:
                print('          ' + line if line.strip() else '')
    else:
        print(f"❌ Erreur (code {result.returncode})\n")
        if result.stderr:
            print("Erreur:")
            print(result.stderr)

    if result.stdout:
        # Extraire et afficher les informations clés
        if 'twitter.alias' in result.stdout:
            print("\n✅ Propriété 'twitter.alias' trouvée")
        if 'twitter.handle' in result.stdout:
            print("✅ Propriété 'twitter.handle' trouvée")
        if 'https://x.com/' in result.stdout:
            print("✅ URL Twitter/X générée")
        if 'URLs OSINT additionnelles' in result.stdout:
            print("✅ Notes OSINT ajoutées")

    return result.returncode == 0


if __name__ == "__main__":
    # Liste de tests
    test_cases = [
        "elonmusk",
        "@snowden",
        "  @test_user  ",
        "invalid-user!",
    ]

    if len(sys.argv) > 1:
        # Si un alias est fourni en argument, tester seulement celui-ci
        test_cases = sys.argv[1:]

    print("\n" + "="*60)
    print("DÉMONSTRATION MALTEGO TWITTER TRANSFORM")
    print("="*60)

    success_count = 0
    for alias in test_cases:
        if test_transform(alias):
            success_count += 1

    print("\n" + "="*60)
    print(f"RÉSUMÉ: {success_count}/{len(test_cases)} tests réussis")
    print("="*60 + "\n")
