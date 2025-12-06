#image python
FROM python:3.13-slim

# worklfow folder
WORKDIR /app

# copier dépendances
COPY requirements.txt .

# installer dépendances
# --no-cache-dir permet réduit taille de l'image
RUN pip install --no-cache-dir -r requirements.txt

#copier tout le code
COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:create_app()"]