# 📦 Package Complet - Tests Postman/Newman

## 📁 Fichiers créés

### 🎯 Fichiers essentiels (obligatoires)

1. **`social-api.postman_collection.json`**
   - Collection Postman complète
   - 22 requêtes avec tests automatisés
   - Tests d'authentification, posts, likes, pagination
   - À placer dans : `postman/social-api.postman_collection.json`

2. **`social-api-poc-local.postman_environment.json`**
   - Variables d'environnement Postman
   - Gestion automatique des tokens et IDs
   - À placer dans : `postman/social-api-poc-local.postman_environment.json`

### 📖 Documentation

3. **`QUICK_START_TESTS.md`** ⭐ COMMENCER PAR ICI
   - Guide rapide de démarrage (5 min)
   - Installation et utilisation simple
   - Checklist avant évaluation
   - À placer dans : `QUICK_START_TESTS.md` (racine du projet)

4. **`POSTMAN_TESTS.md`**
   - Documentation complète et détaillée
   - Tous les tests expliqués
   - Options avancées Newman
   - Intégration CI/CD
   - À placer dans : `POSTMAN_TESTS.md` (racine du projet)

5. **`postman-README.md`**
   - README pour le dossier postman
   - À placer dans : `postman/README.md`

### 🚀 Scripts d'automatisation

6. **`run-tests.sh`**
   - Script Bash pour lancer les tests facilement
   - Vérifications automatiques (API, fichiers)
   - À placer dans : `run-tests.sh` (racine du projet)
   - Rendre exécutable : `chmod +x run-tests.sh`

### 🎁 Bonus - CI/CD

7. **`api-tests.yml`**
   - Workflow GitHub Actions
   - Tests automatiques à chaque push/PR
   - Génération de rapport HTML
   - À placer dans : `.github/workflows/api-tests.yml`

8. **`docker-compose.test.yml`**
   - Configuration Docker pour les tests
   - Exécution isolée avec healthcheck
   - Option rapport HTML
   - À placer dans : `docker-compose.test.yml` (racine du projet)

## 🗂️ Structure finale du projet

```
social-api-poc/
├── .github/
│   └── workflows/
│       └── api-tests.yml           # ← Bonus CI/CD
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models/
│   ├── repositories/
│   ├── routers/
│   ├── schemas/
│   ├── middlewares/
│   └── utils/
├── postman/                         # ← NOUVEAU
│   ├── README.md                    # ← Doc du dossier
│   ├── social-api.postman_collection.json        # ← Collection
│   └── social-api-poc-local.postman_environment.json  # ← Env
├── venv/
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── docker-compose.test.yml         # ← Bonus Docker tests
├── requirements.txt
├── README.md
├── POSTMAN_TESTS.md                # ← Doc complète
├── QUICK_START_TESTS.md            # ← Guide rapide ⭐
└── run-tests.sh                    # ← Script auto
```

## 📝 Installation rapide

### Étape 1 : Organiser les fichiers

```bash
cd /mnt/d/M2/web_service/microservices/social-api-poc

# Créer le dossier postman
mkdir -p postman

# Déplacer les fichiers téléchargés
mv social-api.postman_collection.json postman/
mv social-api-poc-local.postman_environment.json postman/
mv postman-README.md postman/README.md

mv QUICK_START_TESTS.md .
mv POSTMAN_TESTS.md .
mv run-tests.sh .
chmod +x run-tests.sh

# Bonus CI/CD
mkdir -p .github/workflows
mv api-tests.yml .github/workflows/

# Bonus Docker
mv docker-compose.test.yml .
```

### Étape 2 : Installer Newman (optionnel)

```bash
npm install -g newman newman-reporter-htmlextra
```

### Étape 3 : Tester !

```bash
# Terminal 1 : Lancer l'API
source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 2 : Exécuter les tests
./run-tests.sh
```

## 🎯 Pour l'évaluation

### Démonstration minimale

1. **Montrer l'API qui tourne**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Exécuter les tests**
   - Option A : Postman (interface graphique)
   - Option B : Newman (ligne de commande)
   ```bash
   ./run-tests.sh
   ```

3. **Montrer les résultats**
   - ✅ 22/22 tests passent
   - ✅ 85+ assertions validées
   - ✅ Temps d'exécution ~2-3 secondes

### Démonstration complète (avec bonus)

4. **Rapport HTML**
   ```bash
   newman run postman/social-api.postman_collection.json \
     -e postman/social-api-poc-local.postman_environment.json \
     -r htmlextra \
     --reporter-htmlextra-export newman-report.html
   
   # Ouvrir le rapport dans le navigateur
   ```

5. **Tests Docker**
   ```bash
   docker-compose -f docker-compose.test.yml up --abort-on-container-exit
   ```

6. **CI/CD GitHub Actions**
   - Montrer le fichier `.github/workflows/api-tests.yml`
   - (Si repo GitHub) montrer les Actions qui s'exécutent

## ✅ Ce qui est testé

### Authentification (7 tests)
- ✅ Inscription de 2 utilisateurs
- ✅ Connexion et JWT
- ✅ Validation des tokens
- ✅ Cas d'erreur (email dupliqué, mauvais password)

### Posts (8 tests)
- ✅ Création de posts
- ✅ Liste avec pagination cursor-based
- ✅ Tri chronologique inversé
- ✅ Pas de doublons entre pages
- ✅ Protection par authentification

### Likes (7 tests)
- ✅ Toggle like/unlike
- ✅ Compteur correct
- ✅ Champ `is_liked_by_me` personnalisé
- ✅ Gestion d'erreurs

### Total : 85+ assertions automatisées ! 🎉

## 🆘 Support

### Problème d'installation
Voir `QUICK_START_TESTS.md` section "Problèmes courants"

### Questions sur les tests
Voir `POSTMAN_TESTS.md` section "Détail des tests"

### Configuration CI/CD
Voir `POSTMAN_TESTS.md` section "Intégration CI/CD"

## 📚 Ressources

- [Documentation Postman](https://learning.postman.com/)
- [Documentation Newman](https://www.npmjs.com/package/newman)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)

---

## 🚀 Prêt pour l'évaluation !

**Tous les fichiers sont prêts à être utilisés.**

**Ordre recommandé :**
1. 📖 Lire `QUICK_START_TESTS.md` (5 min)
2. 🗂️ Organiser les fichiers (2 min)
3. 🧪 Tester avec Postman ou Newman (2 min)
4. 🎁 (Bonus) Configurer CI/CD et Docker

**Temps total : ~10 minutes**

✅ **22 tests automatisés**  
✅ **85+ assertions**  
✅ **Documentation complète**  
✅ **Scripts d'automatisation**  
✅ **CI/CD ready**

🎓 **Bon courage pour ton POC !**
