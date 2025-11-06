# 🧪 Tests Postman/Newman - Social API POC

## 📦 Fichiers de test

- `social-api.postman_collection.json` : Collection complète avec 22 tests automatisés
- `social-api-poc-local.postman_environment.json` : Variables d'environnement

## 🎯 Ce qui est testé

### ✅ Authentification
- ✅ Inscription de 2 utilisateurs (Alice & Bob)
- ✅ Connexion et génération JWT
- ✅ Validation des tokens
- ✅ Gestion des erreurs (email dupliqué, mauvais mot de passe)

### ✅ Posts
- ✅ Création de posts avec authentification
- ✅ Récupération avec pagination cursor-based
- ✅ Tri par date (plus récent en premier)
- ✅ Vérification : pas de doublons entre pages
- ✅ Protection : accès refusé sans authentification

### ✅ Likes
- ✅ Like/Unlike (toggle) sur un post
- ✅ Compteur de likes correct
- ✅ Champ `is_liked_by_me` personnalisé par utilisateur
- ✅ Gestion des erreurs (post inexistant)

### ✅ Sécurité
- ✅ Tous les endpoints protégés nécessitent JWT
- ✅ Pas de fuite de mot de passe dans les réponses
- ✅ Validation des données (structure, types, longueurs)

## 🚀 Utilisation

### 1️⃣ Avec Postman (Interface graphique)

#### Importer la collection
1. Ouvrir Postman
2. **Import** → Sélectionner `social-api.postman_collection.json`
3. **Import** → Sélectionner `social-api-poc-local.postman_environment.json`
4. Sélectionner l'environnement **"Social API POC - Local"** en haut à droite

#### Lancer l'API
```bash
cd /mnt/d/M2/web_service/microservices/social-api-poc
source venv/bin/activate
uvicorn app.main:app --reload
```

#### Exécuter les tests
- **Option 1** : Exécuter toute la collection
  - Clic droit sur la collection → **Run collection**
  - Vérifier que l'environnement est sélectionné
  - Cliquer sur **Run Social API POC**

- **Option 2** : Exécuter un test individuel
  - Ouvrir une requête
  - Cliquer sur **Send**
  - Vérifier l'onglet **Test Results**

### 2️⃣ Avec Newman (Ligne de commande)

#### Installation de Newman
```bash
# Installer Newman globalement
npm install -g newman

# OU avec npx (sans installation)
npx newman --version
```

#### Exécuter tous les tests
```bash
# S'assurer que l'API tourne d'abord !
# Puis dans un autre terminal :

newman run social-api.postman_collection.json \
  -e social-api-poc-local.postman_environment.json
```

#### Avec rapport HTML
```bash
# Installer le reporter HTML
npm install -g newman-reporter-htmlextra

# Générer un rapport détaillé
newman run social-api.postman_collection.json \
  -e social-api-poc-local.postman_environment.json \
  -r htmlextra \
  --reporter-htmlextra-export ./newman-report.html
```

#### Options utiles
```bash
# Mode verbeux (afficher toutes les requêtes)
newman run social-api.postman_collection.json -e social-api-poc-local.postman_environment.json --verbose

# Arrêter au premier échec
newman run social-api.postman_collection.json -e social-api-poc-local.postman_environment.json --bail

# Délai entre les requêtes (en ms)
newman run social-api.postman_collection.json -e social-api-poc-local.postman_environment.json --delay-request 100
```

## 📊 Résultat attendu

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
│      prerequest-scripts │                 22 │                 0 │
├─────────────────────────┼────────────────────┼───────────────────┤
│              assertions │                 85 │                 0 │
├─────────────────────────┴────────────────────┴───────────────────┤
│ total run duration: 2.5s                                         │
├──────────────────────────────────────────────────────────────────┤
│ total data received: 5.2kB (approx)                              │
├──────────────────────────────────────────────────────────────────┤
│ average response time: 25ms [min: 5ms, max: 120ms, s.d.: 28ms]  │
└──────────────────────────────────────────────────────────────────┘
```

## 🔍 Détail des tests

### Ordre d'exécution
Les tests doivent être exécutés **dans l'ordre** car ils sont enchaînés :

1. **Health Check** → Vérifier que l'API est en ligne
2. **Register User 1 & 2** → Créer Alice et Bob
3. **Login** → Obtenir les tokens JWT
4. **Create Posts** → Créer 3-4 posts
5. **Get Posts** → Tester la pagination
6. **Like/Unlike** → Tester le système de likes
7. **Pagination avancée** → Vérifier l'absence de doublons

### Tests de régression
Les tests vérifient aussi les cas d'erreur :
- ❌ Email déjà enregistré
- ❌ Mauvais mot de passe
- ❌ Accès sans token
- ❌ Like sur post inexistant

## 🔧 Intégration CI/CD (Bonus)

### GitHub Actions

Créer `.github/workflows/api-tests.yml` :

```yaml
name: API Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Start API
      run: |
        uvicorn app.main:app --host 0.0.0.0 --port 8000 &
        sleep 5
    
    - name: Install Newman
      run: npm install -g newman
    
    - name: Run Newman tests
      run: |
        newman run social-api.postman_collection.json \
          -e social-api-poc-local.postman_environment.json
```

### GitLab CI

Créer `.gitlab-ci.yml` :

```yaml
stages:
  - test

api-tests:
  stage: test
  image: python:3.11-slim
  services:
    - name: postman/newman:alpine
  before_script:
    - pip install -r requirements.txt
    - apt-get update && apt-get install -y nodejs npm
    - npm install -g newman
  script:
    - uvicorn app.main:app --host 0.0.0.0 --port 8000 &
    - sleep 5
    - newman run social-api.postman_collection.json -e social-api-poc-local.postman_environment.json
```

## 📝 Variables d'environnement

Les variables suivantes sont automatiquement gérées par les tests :

| Variable | Description | Exemple |
|----------|-------------|---------|
| `base_url` | URL de l'API | `http://localhost:8000` |
| `user1_token` | JWT d'Alice | `eyJhbGciOi...` |
| `user2_token` | JWT de Bob | `eyJhbGciOi...` |
| `post1_id` | ID du premier post | `uuid-v4` |
| `next_cursor` | Cursor de pagination | `2024-11-06T...` |

## 🐛 Dépannage

### Erreur : Connection refused
```
L'API n'est pas lancée !
→ Vérifier : uvicorn app.main:app --reload
```

### Erreur : All tests failed
```
L'API ne répond pas ou mauvaise URL
→ Vérifier : http://localhost:8000/health
```

### Erreur : newman: command not found
```bash
npm install -g newman
# OU
npx newman run ...
```

## ✅ Checklist avant évaluation

- [ ] L'API démarre sans erreur
- [ ] Health check répond `200 OK`
- [ ] Tous les tests Postman passent au vert
- [ ] Newman s'exécute avec 0 failures
- [ ] Rapport HTML généré (bonus)
- [ ] CI/CD configuré (bonus)

## 🎓 Pour aller plus loin

### Ajouter un nouveau test
```javascript
pm.test("Mon test personnalisé", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.propriete).to.eql("valeur_attendue");
});
```

### Tester la performance
```bash
newman run social-api.postman_collection.json \
  -n 10 \  # 10 itérations
  --delay-request 100
```

## 📚 Documentation

- [Postman Learning Center](https://learning.postman.com/)
- [Newman Documentation](https://learning.postman.com/docs/running-collections/using-newman-cli/command-line-integration-with-newman/)
- [Postman Test Scripts](https://learning.postman.com/docs/writing-scripts/test-scripts/)

---

**Prêt pour l'évaluation ! 🚀**
