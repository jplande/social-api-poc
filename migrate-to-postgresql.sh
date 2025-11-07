#!/bin/bash

# Script de migration automatique vers PostgreSQL
# Usage: ./migrate-to-postgresql.sh

set -e

echo "🗄️ Migration vers PostgreSQL - Social API POC"
echo "=============================================="
echo ""

# Vérifier qu'on est dans le bon dossier
if [ ! -f "app/main.py" ]; then
    echo "❌ Erreur: Ce script doit être exécuté depuis la racine du projet social-api-poc"
    echo "   cd /path/to/social-api-poc"
    echo "   ./migrate-to-postgresql.sh"
    exit 1
fi

echo "📦 Backup des fichiers actuels..."
mkdir -p backup-$(date +%Y%m%d-%H%M%S)
cp -r app backup-$(date +%Y%m%d-%H%M%S)/
cp requirements.txt backup-$(date +%Y%m%d-%H%M%S)/ 2>/dev/null || true
cp docker-compose.yml backup-$(date +%Y%m%d-%H%M%S)/ 2>/dev/null || true
echo "✅ Backup créé dans backup-$(date +%Y%m%d-%H%M%S)/"
echo ""

echo "📝 Instructions:"
echo ""
echo "1. Téléchargez tous les fichiers depuis les artifacts Claude"
echo "2. Placez-les dans ce dossier"
echo "3. Exécutez les commandes suivantes:"
echo ""
echo "   # Remplacer les fichiers principaux"
echo "   cp requirements.txt ."
echo "   cp docker-compose.yml ."
echo "   cp .env.example ."
echo "   cp .env.example .env  # Créer le fichier .env"
echo ""
echo "   # Remplacer les fichiers de l'app"
echo "   cp config.py app/"
echo "   cp database.py app/"
echo "   cp main.py app/"
echo ""
echo "   # Créer les nouveaux modèles"
echo "   cp db_models.py app/models/"
echo ""
echo "   # Remplacer les repositories"
echo "   cp user_repository.py app/repositories/"
echo "   cp post_repository.py app/repositories/"
echo ""
echo "   # Remplacer les routers"
echo "   cp auth.py app/routers/"
echo "   cp posts.py app/routers/"
echo ""
echo "   # Remplacer le middleware"
echo "   cp auth_middleware.py app/middlewares/"
echo ""
echo "   # Remplacer le workflow GitHub Actions"
echo "   cp api-tests.yml .github/workflows/"
echo ""
echo "4. Installer les nouvelles dépendances:"
echo "   pip install -r requirements.txt"
echo ""
echo "5. Lancer avec Docker:"
echo "   docker-compose up --build"
echo ""
echo "6. OU lancer en local (après avoir installé PostgreSQL):"
echo "   uvicorn app.main:app --reload"
echo ""
echo "📖 Pour plus de détails, consultez MIGRATION_POSTGRESQL.md"
echo ""
echo "✅ Prêt à migrer!"
