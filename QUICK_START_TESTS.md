# 🚀 Guide Rapide - Tests Postman/Newman

## ⚡ Installation rapide (5 minutes)

### 1. Télécharger les fichiers

Tu devrais avoir :
- ✅ `social-api.postman_collection.json`
- ✅ `social-api-poc-local.postman_environment.json`
- ✅ `run-tests.sh` (optionnel)
- ✅ `POSTMAN_TESTS.md` (documentation complète)

### 2. Placer les fichiers dans ton projet

```bash
cd /mnt/d/M2/web_service/microservices/social-api-poc

# Créer un dossier postman
mkdir -p postman

# Déplacer les fichiers
mv social-api.postman_collection.json postman/
mv social-api-poc-local.postman_environment.json postman/
mv run-tests.sh .
mv POSTMAN_TESTS.md .

# Rendre le script exécutable
chmod +x run-tests.sh
```

## 🎯 Option 1 : Test rapide avec Postman (Interface)

### Installation Postman
1. Télécharger : https://www.postman.com/downloads/
2. Installer et ouvrir Postman

### Import et test
1. **Import** → Sélectionner `postman/social-api.postman_collection.json`
2. **Import** → Sélectionner `postman/social-api-poc-local.postman_environment.json`
3. En haut à droite : sélectionner **"Social API POC - Local"**
4. Lancer ton API :
   ```bash
   cd /mnt/d/M2/web_service/microservices/social-api-poc
   source venv/bin/activate
   uvicorn app.main:app --reload
   ```
5. Dans Postman : Clic droit sur la collection → **Run collection**
6. Cliquer **Run Social API POC** → Tous les tests s'exécutent !

**Résultat attendu :** ✅ 22/22 tests passent

## 🤖 Option 2 : Test automatisé avec Newman (CLI)

### Installation Newman

```bash
# Option A : Installation globale (recommandé)
npm install -g newman

# Option B : Sans installation (avec npx)
# Remplacer 'newman' par 'npx newman' dans les commandes
```

### Exécution des tests

```bash
# Terminal 1 : Lancer l'API
cd /mnt/d/M2/web_service/microservices/social-api-poc
source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 2 : Exécuter les tests
cd /mnt/d/M2/web_service/microservices/social-api-poc

# Méthode 1 : Script automatique
./run-tests.sh

# Méthode 2 : Newman direct
newman run postman/social-api.postman_collection.json \
  -e postman/social-api-poc-local.postman_environment.json
```

### Résultat attendu

```
┌─────────────────────────┬────────────────────┬───────────────────┐
│                         │           executed │            failed │
├─────────────────────────┼────────────────────┼───────────────────┤
│              iterations │                  1 │                 0 │
├─────────────────────────┼────────────────────┼───────────────────┤
│                requests │                 22 │                 0 │
├─────────────────────────┼────────────────────┼───────────────────┤
│            test-scripts │                 44 │                 0 │
├─────────────────────────┼────────────────────┼───────────────────┤
│              assertions │                 85 │                 0 │
├─────────────────────────┴────────────────────┴───────────────────┤
│ total run duration: ~2.5s                                        │
└──────────────────────────────────────────────────────────────────┘

✅ Tous les tests passent !
```

## 📊 Bonus : Rapport HTML

```bash
# Installer le reporter HTML
npm install -g newman-reporter-htmlextra

# Générer le rapport
newman run postman/social-api.postman_collection.json \
  -e postman/social-api-poc-local.postman_environment.json \
  -r htmlextra \
  --reporter-htmlextra-export newman-report.html

# Ouvrir le rapport
xdg-open newman-report.html   # Linux
open newman-report.html        # macOS
start newman-report.html       # Windows
```

## 🐳 Bonus : Test avec Docker

```bash
# Créer un fichier docker-compose.test.yml
cat > docker-compose.test.yml << 'EOF'
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SECRET_KEY=${SECRET_KEY}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 5s
      timeout: 3s
      retries: 5

  newman:
    image: postman/newman:alpine
    depends_on:
      api:
        condition: service_healthy
    volumes:
      - ./postman:/etc/newman
    command: >
      run /etc/newman/social-api.postman_collection.json
      -e /etc/newman/social-api-poc-local.postman_environment.json
      --env-var "base_url=http://api:8000"
EOF

# Lancer les tests avec Docker
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

## 🔧 Intégration CI/CD (GitHub Actions)

```bash
# Créer le dossier
mkdir -p .github/workflows

# Copier le workflow
cp api-tests.yml .github/workflows/

# Commit et push
git add .github/workflows/api-tests.yml
git commit -m "Add GitHub Actions workflow for API tests"
git push
```

Les tests s'exécuteront automatiquement à chaque push/PR ! 🎉

## 📋 Checklist avant l'évaluation

- [ ] API démarre sans erreur : `uvicorn app.main:app --reload`
- [ ] Health check OK : `curl http://localhost:8000/health`
- [ ] Collection Postman importée et fonctionne
- [ ] Newman installé : `newman --version`
- [ ] Tous les tests Newman passent : `./run-tests.sh`
- [ ] (Bonus) Rapport HTML généré
- [ ] (Bonus) CI/CD configuré

## ❓ Problèmes courants

### Newman : command not found
```bash
npm install -g newman
# OU utiliser npx
npx newman run postman/social-api.postman_collection.json ...
```

### API ne répond pas
```bash
# Vérifier que l'API tourne
curl http://localhost:8000/health

# Si pas de réponse :
cd /mnt/d/M2/web_service/microservices/social-api-poc
source venv/bin/activate
uvicorn app.main:app --reload
```

### Tests échouent
```bash
# Redémarrer l'API (réinitialise les données en mémoire)
# CTRL+C dans le terminal de l'API
uvicorn app.main:app --reload

# Relancer les tests
./run-tests.sh
```

## 📚 Documentation complète

Voir `POSTMAN_TESTS.md` pour :
- Détail de tous les tests
- Options avancées Newman
- Configuration CI/CD complète
- Ajout de nouveaux tests

## ✅ Tu es prêt !

**Commandes essentielles à retenir :**

```bash
# Terminal 1 : API
uvicorn app.main:app --reload

# Terminal 2 : Tests
./run-tests.sh
```

**Démonstration pour l'évaluation :**
1. Lancer l'API
2. Montrer Postman ou exécuter `./run-tests.sh`
3. Montrer les 22 tests qui passent ✅
4. (Bonus) Montrer le rapport HTML et/ou GitHub Actions

🚀 **Bonne chance pour ton évaluation !**
