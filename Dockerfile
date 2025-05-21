# Utilisation d'une image Python légère
FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier uniquement requirements.txt dans un premier temps (meilleure gestion du cache)
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste des fichiers du projet
COPY . .

# Évite le buffering dans les logs (utile pour Cloud Run/logging)
ENV PYTHONUNBUFFERED=1

# Définir le port d’écoute (utile pour GCP Cloud Run)
ENV PORT=8080

# Lancer l'application avec Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
