# 📬 Collections Postman

Ce dossier contient les collections Postman pour tester l'API.

## Fichiers

- `social-api.postman_collection.json` - Collection complète avec 22 tests
- `social-api-poc-local.postman_environment.json` - Variables d'environnement

## Utilisation rapide

### Avec Postman
1. Importer les 2 fichiers dans Postman
2. Sélectionner l'environnement "Social API POC - Local"
3. Lancer l'API : `uvicorn app.main:app --reload`
4. Exécuter la collection

### Avec Newman (CLI)
```bash
# Installation
npm install -g newman

# Exécution
newman run social-api.postman_collection.json \
  -e social-api-poc-local.postman_environment.json
```

Voir le fichier `POSTMAN_TESTS.md` à la racine pour plus de détails.
