import os
from flask import Flask, request, render_template
from dotenv import load_dotenv
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import TextCategory
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions

# Initialisation de l'application Flask
app = Flask (__name__)

# Chargement des variables d'environnement pour sécuriser les clés d'API
load_dotenv()
key = os.getenv("API")
endpoint = os.getenv("ENDPOINT")

# Initialisation du client Azure Content Safety avec les informations d'authentification
client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

@app.route('/',methods=['GET','POST'])
def index():
    """
    Route principale de l'application qui gère les méthodes GET et POST.
    - GET: Affiche le formulaire vide
    - POST: Traite le texte soumis et renvoie l'analyse de contenu
    
    Returns:
        Template HTML avec les résultats de l'analyse si disponibles
    """
    if request.method == 'POST':
        # Récupération du texte depuis le formulaire
        text_content = request.form['text_content']
        # Analyse du texte via l'API Azure Content Safety
        result = analyze_text(text_content)
        # Retourne le template avec les résultats et le texte original
        return render_template('index.html',result=result,text_content=text_content)
    # Affichage initial du formulaire vide
    return render_template ('index.html')

def analyze_text(text_content):
    """
    Analyse le texte fourni pour détecter du contenu potentiellement inapproprié
    en utilisant l'API Azure Content Safety.
    
    Args:
        text_content (str): Le texte à analyser
        
    Returns:
        dict: Dictionnaire contenant les scores de sévérité pour différentes catégories
              et une conclusion basée sur les seuils de sévérité
    """
    # Préparation de la requête pour l'API Azure Content Safety
    request = AnalyzeTextOptions(text=text_content)
    
    try:
        # Appel de l'API pour analyser le texte
        response = client.analyze_text(request)
    except HttpResponseError as e:
        # Gestion des erreurs de l'API
        return {"error": f"Analyze text failed. Error code: {e.error.code}, Error message: {e.error.message}"}

    # Extraction des scores de sévérité pour chaque catégorie de contenu inapproprié
    results = {
        "Hate severity": next((item.severity for item in response.categories_analysis if item.category == TextCategory.HATE), 0),
        "SelfHarm severity": next((item.severity for item in response.categories_analysis if item.category == TextCategory.SELF_HARM), 0),
        "Sexual severity": next((item.severity for item in response.categories_analysis if item.category == TextCategory.SEXUAL), 0),
        "Violence severity": next((item.severity for item in response.categories_analysis if item.category == TextCategory.VIOLENCE), 0)
    }

    # Création d'une conclusion basée sur les seuils de sévérité (≥ 4 est considéré comme élevé)
    conclusion = []
    for category, severity in results.items():
        if severity >= 4:
            conclusion.append(f"{category} severity")

    # Ajout de la conclusion aux résultats
    results["Conclusion"] = ", ".join(conclusion) if conclusion else "No high severity content detected."
    
    return results


if __name__ == "__main__":
    # Démarrage de l'application en mode debug pour le développement
    app.run(debug=True)