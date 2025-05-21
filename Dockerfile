# Utilise une image Python 3.11 allégée comme base
FROM python:3.11-slim

# Définit le répertoire de travail à l'intérieur du conteneur
WORKDIR /app

# Copie le fichier des dépendances dans le conteneur
COPY requirements.txt .

# Installe les dépendances Python sans garder le cache (image plus légère)
RUN pip install --no-cache-dir -r requirements.txt

# Copie tout le contenu du dossier local dans le conteneur
COPY . .

# Assure que les logs Python s'affichent directement dans la console (pas de buffering)
ENV PYTHONUNBUFFERED=1

# Commande par défaut exécutée au démarrage du conteneur : lance l'API FastAPI avec Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
