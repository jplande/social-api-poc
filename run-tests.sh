#!/bin/bash

# Script d'exécution des tests Newman pour Social API POC
# Usage: ./run-tests.sh

set -e

COLLECTION="postman/social-api.postman_collection.json"
ENVIRONMENT="postman/social-api-poc-local.postman_environment.json"

echo "🧪 Social API POC - Tests automatisés"
echo "======================================"
echo ""

# Vérifier que Newman est installé
if ! command -v newman &> /dev/null; then
    echo "❌ Newman n'est pas installé !"
    echo ""
    echo "Installation :"
    echo "  npm install -g newman"
    echo ""
    echo "OU utiliser npx (sans installation) :"
    echo "  npx newman run $COLLECTION -e $ENVIRONMENT"
    exit 1
fi

# Vérifier que les fichiers existent
if [ ! -f "$COLLECTION" ]; then
    echo "❌ Fichier non trouvé : $COLLECTION"
    exit 1
fi

if [ ! -f "$ENVIRONMENT" ]; then
    echo "❌ Fichier non trouvé : $ENVIRONMENT"
    exit 1
fi

# Vérifier que l'API est accessible
echo "🔍 Vérification de l'API..."
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "❌ L'API ne répond pas sur http://localhost:8000"
    echo ""
    echo "Lancer l'API d'abord :"
    echo "  uvicorn app.main:app --reload"
    exit 1
fi

echo "✅ API accessible"
echo ""

# Exécuter Newman
echo "🚀 Exécution des tests..."
echo ""

newman run "$COLLECTION" \
    -e "$ENVIRONMENT" \
    --color on \
    --delay-request 50

echo ""
echo "✅ Tests terminés !"
