# Social API POC

API REST pour réseau social - POC 3 jours

## 🚀 Lancement rapide

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
```bash
docker-compose up
```

**API** : http://localhost:8000  
**Documentation** : http://localhost:8000/docs

## 📡 Endpoints

- `POST /api/auth/register` - Inscription
- `POST /api/auth/login` - Connexion (retourne JWT)
- `GET /api/posts` - Liste des posts avec pagination (auth requise)
- `POST /api/posts` - Créer un post (auth requise)
- `POST /api/posts/{id}/like` - Toggle like (auth requise)

## 🧪 Tests
```bash
# Postman/Newman
newman run postman/social-api.postman_collection.json

# Pytest
pytest
```
