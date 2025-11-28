# Social API POC

API REST pour réseau social - POC 3 jours

## Lancement rapide

### Local (dev)
```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Lancer
uvicorn app.main:app --reload
```

### Docker

#### API seule
```bash
docker-compose up
```

#### API + Gravitee APIM
```bash
docker-compose -f docker-compose-unified.yml up -d
```

## URLs des services

### API FastAPI
- **API** : http://localhost:8000  
- **Documentation** : http://localhost:8000/docs

### Gravitee APIM
- **Gateway** : http://localhost:8082
- **Management API** : http://localhost:8083
- **Management UI** : http://localhost:8084
- **Portal UI** : http://localhost:8085

## Endpoints API

### Authentification
- `POST /api/auth/register` - Inscription
- `POST /api/auth/login` - Connexion (retourne JWT)

### Posts
- `GET /api/posts` - Liste des posts avec pagination (auth requise)
- `POST /api/posts` - Créer un post (auth requise)
- `POST /api/posts/{id}/like` - Toggle like (auth requise)

### Health
- `GET /health` - Health check
- `GET /` - Informations de l'API

## Tests
```bash
# Postman/Newman
newman run postman/social-api.postman_collection.json

# JSON-SERVER
npx json-server db.json -p 3000
```

## Configuration

Créer un fichier `.env` à la racine du projet :

```env
# Gravitee APIM
MONGODB_VERSION=6.0.8
ELASTIC_VERSION=8.8.1
APIM_VERSION=4

# FastAPI
SECRET_KEY=dev-secret-key-change-in-production
```

## Architecture

- **FastAPI** : Framework Python pour l'API REST
- **JWT** : Authentification par tokens
- **Gravitee APIM** : Gateway et gestion des APIs
- **MongoDB** : Base de données pour Gravitee
- **Elasticsearch** : Analytics pour Gravitee