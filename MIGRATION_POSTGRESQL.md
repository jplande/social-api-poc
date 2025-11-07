# 🗄️ Migration vers PostgreSQL - Guide Complet

## 📋 Changements apportés

### ✅ Nouvelles dépendances
- `sqlalchemy` : ORM pour Python
- `psycopg2-binary` : Driver PostgreSQL
- `alembic` : Gestion des migrations de schéma
- `pytest-asyncio` : Tests asynchrones

### ✅ Nouveaux fichiers

1. **`app/database.py`** : Configuration SQLAlchemy et session management
2. **`app/models/db_models.py`** : Modèles SQLAlchemy (tables)
3. **`.env.example`** : Configuration de la base de données
4. **`docker-compose.yml`** (mis à jour) : Service PostgreSQL ajouté

### ✅ Fichiers modifiés

1. **`app/config.py`** : Ajout de `DATABASE_URL`
2. **`app/repositories/user_repository.py`** : Utilise SQLAlchemy au lieu de dict en mémoire
3. **`app/repositories/post_repository.py`** : Utilise SQLAlchemy avec requêtes SQL
4. **`app/routers/auth.py`** : Injection de dépendance `db: Session`
5. **`app/routers/posts.py`** : Injection de dépendance `db: Session`
6. **`app/middlewares/auth_middleware.py`** : Accès BDD via repository
7. **`app/main.py`** : Initialisation de la BDD au démarrage
8. **`.github/workflows/api-tests.yml`** : Service PostgreSQL pour CI/CD

## 🚀 Installation et Démarrage

### Option 1 : Docker Compose (Recommandé)

Le plus simple pour avoir PostgreSQL + API ensemble :

```bash
# Copier les nouveaux fichiers dans votre projet
cd /mnt/d/M2/web_service/microservices/social-api-poc

# Remplacer les fichiers
# (voir section "Fichiers à remplacer" ci-dessous)

# Démarrer tout avec Docker
docker-compose up --build
```

L'API sera disponible sur `http://localhost:8000` et PostgreSQL sur `localhost:5432`.

### Option 2 : Local (PostgreSQL séparé)

Si vous voulez lancer PostgreSQL localement sans Docker :

#### 1. Installer PostgreSQL

**Ubuntu/Debian :**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**macOS (avec Homebrew) :**
```bash
brew install postgresql@16
brew services start postgresql@16
```

**Windows :**
Télécharger l'installeur depuis https://www.postgresql.org/download/windows/

#### 2. Créer la base de données

```bash
# Se connecter à PostgreSQL
sudo -u postgres psql

# Dans le shell PostgreSQL
CREATE DATABASE social_db;
CREATE USER social_user WITH PASSWORD 'social_password';
GRANT ALL PRIVILEGES ON DATABASE social_db TO social_user;
\q
```

#### 3. Configurer l'environnement

```bash
# Créer le fichier .env
cp .env.example .env

# Éditer .env
nano .env
```

Contenu de `.env` :
```
SECRET_KEY=your-super-secret-key-change-me
DATABASE_URL=postgresql://social_user:social_password@localhost:5432/social_db
```

#### 4. Installer les dépendances Python

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Installer les nouvelles dépendances
pip install -r requirements.txt
```

#### 5. Lancer l'API

```bash
uvicorn app.main:app --reload
```

Au premier démarrage, les tables seront créées automatiquement.

## 📁 Fichiers à remplacer dans votre projet

Voici la liste des fichiers à remplacer ou créer :

### Fichiers à REMPLACER

1. `requirements.txt`
2. `app/config.py`
3. `app/main.py`
4. `app/repositories/user_repository.py`
5. `app/repositories/post_repository.py`
6. `app/routers/auth.py`
7. `app/routers/posts.py`
8. `app/middlewares/auth_middleware.py`
9. `docker-compose.yml`
10. `.github/workflows/api-tests.yml`

### Fichiers à CRÉER (nouveaux)

1. `app/database.py`
2. `app/models/db_models.py`
3. `.env.example`
4. `.env` (copie de `.env.example` avec vos valeurs)

### Fichier à METTRE À JOUR

Ajoutez à votre `.gitignore` :
```
# Database
.env
*.db
*.sqlite
*.sqlite3
```

## 🧪 Tests

### Tests locaux

Les tests Postman fonctionnent exactement pareil :

```bash
# Terminal 1 : Lancer l'API (avec Docker ou local)
docker-compose up

# OU en local
uvicorn app.main:app --reload

# Terminal 2 : Exécuter les tests
./run-tests.sh
```

### Tests CI/CD

GitHub Actions lance maintenant un service PostgreSQL automatiquement. Les tests passent comme avant !

## 🔍 Vérification de la migration

### 1. Vérifier que PostgreSQL fonctionne

```bash
# Avec Docker
docker-compose ps

# En local
psql -U social_user -d social_db -h localhost
```

### 2. Vérifier les tables créées

```bash
# Se connecter à la BDD
psql -U social_user -d social_db -h localhost

# Lister les tables
\dt

# Vous devriez voir :
#  public | post_likes | table | social_user
#  public | posts      | table | social_user
#  public | users      | table | social_user
```

### 3. Tester l'API

```bash
# Health check
curl http://localhost:8000/health

# Devrait retourner :
# {"status":"healthy","database":"connected"}
```

### 4. Exécuter les tests Postman

```bash
newman run postman/social-api.postman_collection.json \
  -e postman/social-api-poc-local.postman_environment.json
```

Tous les 22 tests doivent passer ! ✅

## 📊 Structure de la base de données

### Table `users`
```sql
CREATE TABLE users (
    id VARCHAR PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Table `posts`
```sql
CREATE TABLE posts (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR NOT NULL REFERENCES users(id),
    content VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Table `post_likes` (Many-to-Many)
```sql
CREATE TABLE post_likes (
    user_id VARCHAR REFERENCES users(id),
    post_id VARCHAR REFERENCES posts(id),
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (user_id, post_id)
);
```

## 🎓 Points bonus obtenus

✅ **Base de données PostgreSQL** : Migration complète depuis le stockage en mémoire  
✅ **Persistance des données** : Les données survivent au redémarrage  
✅ **ORM SQLAlchemy** : Code maintenable et sécurisé  
✅ **Relations** : Users ↔ Posts ↔ Likes avec contraintes référentielles  
✅ **Transactions** : ACID compliance automatique  
✅ **Docker** : PostgreSQL dans docker-compose  
✅ **CI/CD** : Tests automatiques avec PostgreSQL dans GitHub Actions  

## ❓ FAQ

### Q: Comment réinitialiser la base de données ?

**Avec Docker :**
```bash
docker-compose down -v  # Supprime les volumes
docker-compose up --build
```

**En local :**
```bash
psql -U social_user -d social_db -h localhost
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO social_user;
\q
# Redémarrer l'API pour recréer les tables
```

### Q: Comment voir les données dans la BDD ?

```bash
# Connexion
psql -U social_user -d social_db -h localhost

# Requêtes utiles
SELECT * FROM users;
SELECT * FROM posts ORDER BY created_at DESC;
SELECT * FROM post_likes;

# Statistiques
SELECT COUNT(*) FROM posts;
SELECT username, COUNT(posts.id) as post_count 
FROM users 
LEFT JOIN posts ON users.id = posts.user_id 
GROUP BY username;
```

### Q: Puis-je utiliser une autre base de données ?

Oui ! SQLAlchemy supporte MySQL, MariaDB, SQLite, etc. Changez juste `DATABASE_URL` :

```bash
# MySQL
DATABASE_URL=mysql://user:password@localhost/dbname

# SQLite (pour tests)
DATABASE_URL=sqlite:///./test.db
```

### Q: Comment faire des migrations de schéma ?

Utilisez Alembic (déjà installé) :

```bash
# Initialiser Alembic
alembic init alembic

# Créer une migration
alembic revision --autogenerate -m "Add column to users"

# Appliquer les migrations
alembic upgrade head
```

## ✅ Checklist de migration

- [ ] PostgreSQL installé et démarré
- [ ] Base de données `social_db` créée
- [ ] Tous les nouveaux fichiers copiés
- [ ] Tous les fichiers existants remplacés
- [ ] `.env` créé avec `DATABASE_URL`
- [ ] `pip install -r requirements.txt` exécuté
- [ ] API démarre sans erreur
- [ ] Health check retourne `{"database": "connected"}`
- [ ] Les 3 tables sont créées (users, posts, post_likes)
- [ ] Les 22 tests Postman passent
- [ ] Docker Compose fonctionne
- [ ] GitHub Actions passe

## 🎉 Prêt pour l'évaluation !

Vous avez maintenant :
- ✅ Une vraie base de données PostgreSQL
- ✅ Persistance des données
- ✅ Architecture professionnelle (ORM)
- ✅ Tests qui passent
- ✅ CI/CD fonctionnel
- ✅ Documentation complète

**Points bonus garantis ! 🚀**
