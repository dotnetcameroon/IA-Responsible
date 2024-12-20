# IA Responsable

Cette application utilise Flask pour créer une interface web permettant d'analyser du texte en utilisant les services de sécurité de contenu d'Azure AI.

## Fonctionnalités

- Analyse de texte pour détecter et modérer le contenu potentiellement dangereux.
- Interface web simple pour soumettre du texte à analyser.

## Prérequis

- Python 3.9 ou supérieur

## Installation

1. Clonez le dépôt :
    ```bash
    git clone https://github.com/dotnetcameroon/IA-Responsible.git
    cd IA-Responsible
    ```

2. Créez un environnement virtuel et activez-le :
    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur Windows, utilisez `venv\Scripts\activate`
    ```

3. Installez les dépendances :
    ```bash
    pip install -r requirements.txt
    ```

## Utilisation

Les clés API et le lien de l'endpoint sont déjà inclus dans le projet, vous n'avez donc pas besoin de les configurer.

1. Lancez l'application Flask :
    ```bash
    python app.py
    ```

2. Ouvrez votre navigateur et accédez à l'adresse suivante :
    ```
    http://localhost:5000
    ```

## Déploiement

Pour déployer cette application, vous pouvez utiliser des services comme Heroku, Azure App Service, ou tout autre service de conteneurisation.

## Accès au site

Vous pouvez accéder à l'application déployée à l'adresse suivante :
http://127.0.0.1:5000/

## Contribuer

Les contributions sont les bienvenues ! Veuillez soumettre une pull request ou ouvrir une issue pour discuter des changements que vous souhaitez apporter.

