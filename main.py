from fastapi import FastAPI, Request
from datetime import datetime
from google.cloud import storage, aiplatform
import os, json
from dotenv import load_dotenv
from google.cloud import aiplatform_v1

load_dotenv()

app = FastAPI()

BUCKET_NAME = os.getenv("GCS_BUCKET")
DATA_PATH = os.getenv("DATA_PATH")
PROJECT_ID = os.getenv("PROJECT_ID")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

@app.get("/hello")
def hello():
    return {"message": "Bienvenue à l'API !"}

@app.get("/status")
def status():
    return {"datetime": datetime.now().isoformat()}

import csv
from io import StringIO

@app.get("/data")
def get_data():
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(DATA_PATH)
    content = blob.download_as_text()

    csv_reader = csv.DictReader(StringIO(content))
    data = [row for row in csv_reader]
    return data


@app.post("/data")
async def post_data(request: Request):
    new_entry = await request.json()

    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(DATA_PATH)

    content = blob.download_as_text()
    output = StringIO(content)
    reader = list(csv.DictReader(output))
    fieldnames = reader[0].keys() if reader else new_entry.keys()

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(reader)
    writer.writerow(new_entry)

    blob.upload_from_string(output.getvalue(), content_type='text/csv')
    return {"message": "Ligne ajoutée avec succès"}





from vertexai.preview.generative_models import GenerativeModel, ChatSession
import vertexai
import os
from dotenv import load_dotenv

load_dotenv()
PROJECT_ID = os.getenv("PROJECT_ID")
REGION = "us-central1"

@app.get("/joke")
def get_joke():
    try:       
        vertexai.init(project=PROJECT_ID, location=REGION)
        
        model = GenerativeModel(model_name="gemini-2.0-flash-001") 
  
        chat: ChatSession = model.start_chat()

        prompt = "Raconte-moi une blague courte et drôle en français."

        response = chat.send_message(prompt)

        return {"joke": response.text}

    except Exception as e:
        return {"error": str(e)}



