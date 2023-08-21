from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy
import json
app = Flask(__name__)
nlp = spacy.load("fr_core_news_sm")


CORS(app)  # Active CORS pour toutes les routes de l'application

    
# Génération de suggestions basées sur les entités extraites
def generate_recipe_suggestions(cuisine, ingredients):
    suggestions = []

    # Charger les recettes depuis le fichier JSON
    with open('./recettes.json', 'r', encoding='utf-8') as recipes_file:
        recipes = json.load(recipes_file)
        for recipe in recipes:
            if (not cuisine or cuisine.lower() in recipe["cuisine"].lower()) and all(ing.lower() in recipe["ingredients"] for ing in ingredients):
                suggestions.append(recipe["name"])

    return suggestions

# Endpoint pour recevoir les données d'entrée et renvoyer les suggestions
@app.route('/get_suggestions', methods=['POST'])
def get_suggestions():
    data = request.json  # Les données d'entrée de l'utilisateur (cuisine et ingrédients)

    cuisine = data["cuisine"]
    ingredients = data["ingredients"]

    # Utilisation de SpaCy pour analyser les préférences
    preferences_text = f"Je veux une recette {cuisine} avec {', '.join(ingredients)}"
    doc = nlp(preferences_text)

    # Extraction des entités
    cuisine = None
    ingredients = []

    for ent in doc.ents:
        if ent.label_ == "CUISINE":
            cuisine = ent.text
        elif ent.label_ == "INGREDIENT":
            ingredients.append(ent.text)

    suggestions = generate_recipe_suggestions(cuisine, ingredients)

    return jsonify({"suggestions": suggestions})

if __name__ == '__main__':
    app.run()
