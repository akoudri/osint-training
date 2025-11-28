#!/usr/bin/env python3
"""
Maltego Transform Server
Serveur Flask pour héberger les transforms localement
"""

from maltego_trx.server import app, application
from transforms.transform_config import registry

# Enregistrer les transforms
registry.register_to_server(app)

if __name__ == "__main__":
    # Démarrer le serveur en mode debug
    print("=" * 60)
    print("Maltego Transform Server - OSINT Training")
    print("=" * 60)
    print(f"Serveur démarré sur http://localhost:8080")
    print(f"Transforms disponibles: {len(registry.transforms)}")
    for transform in registry.transforms:
        print(f"  - {transform}")
    print("=" * 60)
    print("Pour configurer Maltego:")
    print("1. Ouvrir Maltego → Transforms → Transform Hub")
    print("2. New Local Transform Server")
    print("3. URL: http://localhost:8080")
    print("=" * 60)

    app.run(host="0.0.0.0", port=8080, debug=True)
