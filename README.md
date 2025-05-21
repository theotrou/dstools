lien du Cloud run : https://dstools-api-32184514091.europe-west1.run.app/

CHUNG Theodore : theotrou (chef de groupe)
PITIOT Paul : ppppaulp


# Mini API Cloud - dstools-api (FastAPI + GCP)

Ce projet est une mini API Python (FastAPI) déployée sur Google Cloud Run, avec stockage de données dans Google Cloud Storage (GCS) et génération de blagues via Vertex AI.

---

## Fonctionnalités

- `GET /hello` : message de bienvenue
- `GET /status` : heure/serveur actuelle
- `GET /data` : lit un fichier CSV depuis GCS
- `POST /data` : ajoute une ligne dans ce CSV dans GCS
- `GET /joke` : retourne une blague générée par l’IA (Gemini via Vertex AI, ou simulée)

---

## Technologies utilisées

- Python 3.11 + FastAPI
- Docker
- Google Cloud Storage (GCS)
- Vertex AI / Gemini (ou fallback local)
- Google Cloud Run
- GitHub

---

## Lancement en local

### 1. Cloner le projet

```bash
git clone https://github.com/theotrou/dstools-api.git
cd dstools-api
