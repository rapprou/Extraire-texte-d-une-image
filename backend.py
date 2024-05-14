# "python3 backend.py" toujours demarrer le port du backend ensuite le port Flask

import re
from flask import Flask, request, jsonify
from flask_cors import CORS
import pytesseract
from PIL import Image
import io

# Initialisation de l'application Flask
app = Flask(__name__)
CORS(app)  # Permet les requêtes cross-origin

# Configuration de Tesseract si nécessaire
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


@app.route('/extract-text', methods=['POST'])
def extract_text():
    try:
        # Récupérer le fichier image à partir de la requête
        image_file = request.files.get('image')
        if not image_file:
            return jsonify({'error': 'Aucun fichier image fourni.'}), 400

        # Charger l'image
        image = Image.open(io.BytesIO(image_file.read()))

        # Extraire le texte avec Tesseract
        text = pytesseract.image_to_string(image, lang='fra')

        # Nettoyer le texte
        cleaned_text = clean_text(text)

        # Retourner le texte extrait sous forme de JSON
        return jsonify({'text': text})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Gérer les accents et symbole


def clean_text(text):
    # Remplacer les accents et supprimer les symboles spéciaux
    text = re.sub(r'[àáâãäå]', 'a', text)
    text = re.sub(r'[èéêë]', 'e', text)
    text = re.sub(r'[ìíîï]', 'i', text)
    text = re.sub(r'[òóôõö]', 'o', text)
    text = re.sub(r'[ùúûü]', 'u', text)
    text = re.sub(r'[ç]', 'c', text)
    # Conserver uniquement les caractères alphanumériques et quelques ponctuations
    text = re.sub(r'[^a-zA-Z0-9\s.,;?!]', '', text)
    return text


# Tester ma route

@app.route('/')
def index():
    return "Tester ma route API backend"


# Lancer l'application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
