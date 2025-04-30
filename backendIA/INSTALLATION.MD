Cette application FLASK PYthon est conçue pour créer un modèle de prédiction IA sur les données COVID en 2023 et 2024, cette application récupère les données de la base de données mariaDB générée par l'api SpringBoot qui gère de son côté l'extraction, nettoyage et transformation des données covid et sars.

### Étapes d'initialisation

1. **Créer un environnement virtuel** :
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate
   ```

2. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurer la base de données** (si nécessaire) :
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

4. **Lancer l'application Flask** :
   ```bash
   python run.py
   ```

### Exemple de commande pour prédictions
Si votre modèle de prédiction est déjà intégré dans l'application Flask, vous pouvez tester une prédiction en utilisant `curl` ou un outil comme Postman. Exemple avec `curl` :
```bash
curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d '{"input_data": [1.0, 2.0, 3.0]}'
```

Assurez-vous que votre route `/predict` est bien définie dans routes.py.