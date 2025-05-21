# Importation des modules nécessaires
from fastapi import FastAPI, Request
from datetime import datetime
from google.cloud import storage, aiplatform
import os, json
from dotenv import load_dotenv
from google.cloud import aiplatform_v1
import csv
from io import StringIO

# Chargement des variables d'environnement depuis un fichier .env
load_dotenv()

# Initialisation de l'application FastAPI
app = FastAPI()

# Récupération des variables d'environnement
BUCKET_NAME = os.getenv("GCS_BUCKET")              # Nom du bucket GCS
DATA_PATH = os.getenv("DATA_PATH")                 # Chemin vers le fichier CSV dans le bucket
PROJECT_ID = os.getenv("PROJECT_ID")               # ID du projet GCP
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")  # Authentification GCP

# Endpoint GET de test simple
@app.get("/hello")
def hello():
    return {"message": "Bienvenue à l'API !"}

# Endpoint GET pour renvoyer la date et l'heure actuelles
@app.get("/status")
def status():
    return {"datetime": datetime.now().isoformat()}

# Endpoint GET pour lire le fichier CSV depuis le bucket GCS
@app.get("/data")
def get_data():
    client = storage.Client()                      # Création d'un client GCS
    bucket = client.bucket(BUCKET_NAME)            # Accès au bucket
    blob = bucket.blob(DATA_PATH)                  # Accès au fichier
    content = blob.download_as_text()              # Téléchargement du fichier en texte

    # Lecture du CSV et transformation en liste de dictionnaires
    csv_reader = csv.DictReader(StringIO(content))
    data = [row for row in csv_reader]
    return data

# Endpoint POST pour ajouter une ligne dans le fichier CSV du bucket GCS
@app.post("/data")
async def post_data(request: Request):
    new_entry = await request.json()               # Récupération des données JSON envoyées

    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(DATA_PATH)

    # Téléchargement du contenu actuel
    content = blob.download_as_text()
    output = StringIO(content)
    reader = list(csv.DictReader(output))          # Lecture des données existantes

    # Détermination des en-têtes (colonnes)
    fieldnames = reader[0].keys() if reader else new_entry.keys()

    # Écriture du nouveau contenu
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(reader)
    writer.writerow(new_entry)                     # Ajout de la nouvelle ligne

    # Upload du fichier mis à jour dans le bucket
    blob.upload_from_string(output.getvalue(), content_type='text/csv')
    return {"message": "Ligne ajoutée avec succès"}

# Import des outils pour Vertex AI (Gemini)
from vertexai.preview.generative_models import GenerativeModel, ChatSession
import vertexai

# Chargement (à nouveau) des variables d'environnement nécessaires à Vertex AI
load_dotenv()
PROJECT_ID = os.getenv("PROJECT_ID")
REGION = "us-central1"

# Endpoint GET pour obtenir une blague générée par Gemini
@app.get("/joke")
def get_joke():
    try:
        # Initialisation de Vertex AI avec le bon projet et la région
        vertexai.init(project=PROJECT_ID, location=REGION)

        # Chargement du modèle Gemini (version flash 2.0)
        model = GenerativeModel(model_name="gemini-2.0-flash-001")
        chat: ChatSession = model.start_chat()

        # Message d'entrée pour le modèle
        prompt = "Raconte-moi une blague courte et drôle en français."
        response = chat.send_message(prompt)

        # Retour de la réponse générée
        return {"joke": response.text}

    except Exception as e:
        # Gestion des erreurs éventuelles
        return {"error": str(e)}
