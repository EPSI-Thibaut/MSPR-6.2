# Documentation du modèle d'IA - CovidForecaster

## 1. Introduction

Ce document décrit le workflow et l’architecture du modèle IA utilisé pour prédire l’évolution de la pandémie COVID en 2023.

---

## 2. Lancement du workflow

Pour lancer le workflow du modèle IA qui va générer les prédictions des données de COVID en 2023, exécutez :

```bash
python3 workflow.py
```

---

## 3. Architecture du modèle

Le modèle utilise un ensemble (ensemble model) basé sur la classe `CovidForecaster` qui implémente les étapes suivantes :

### 3.1 Récupération des données

- Connexion à la base MariaDB pour extraire les données historiques COVID.

### 3.2 Prétraitement des données

- Nettoyage des valeurs extrêmes.
- Création de caractéristiques temporelles (jour de la semaine, mois, etc.).
- Génération de variables décalées (lag features) pour capturer les tendances.
- Calcul de moyennes mobiles.

### 3.3 Entraînement

- Utilisation d’un modèle `RandomForestRegressor`.
- Optimisation des hyperparamètres via `RandomizedSearchCV`.
- Division train/test temporelle pour respecter la chronologie des données.

### 3.4 Prédiction

- Génération de prédictions jour par jour.
- Extrapolation si nécessaire pour couvrir toute l’année 2023.
- Calcul des décès et récupérations basé sur les taux historiques.

### 3.5 Visualisation et sauvegarde

- Génération de graphiques comparant données réelles et prédictions.
- Sauvegarde des modèles entraînés pour réutilisation.
- Stockage des prédictions dans la base de données.

---

## 4. Caractéristiques utilisées

Le modèle utilise des caractéristiques avancées pour améliorer les prédictions :

- **Variables temporelles** : jour de semaine, mois, saison, weekends.
- **Indicateurs décalés** : cas, décès et récupérations avec différents délais.
- **Moyennes mobiles** : sur 7, 14 et 30 jours pour lisser les tendances.
- **Taux calculés** : taux de croissance, taux de mortalité, taux de récupération.

---

## 5. Gestion des erreurs

Le modèle intègre plusieurs mécanismes de gestion d’erreurs :

- Détection et correction des valeurs infinies ou NaN.
- Retry automatique avec sous-ensemble de données en cas d’erreur.
- Mode "test" pour déploiement et vérification rapides.

---

## 6. Utilisation du modèle

### 6.1 Lancement du workflow complet

Pour générer des prédictions pour 2023, la commande précédente va :

- Récupérer les données COVID depuis la base de données.
- Prétraiter les données.
- Entraîner le modèle.
- Générer des prédictions pour 2023.
- Sauvegarder les prédictions dans la base de données.
- Générer des graphiques de visualisation.

### 6.2 Prédictions par région

Pour générer des prédictions pour une région spécifique, utilisez l’option correspondante dans le script.

### 6.3 Visualisation des résultats

Les graphiques sont automatiquement générés dans le dossier `static/` :

- `covid_predictions.png` : comparaison entre cas réels, prédits et prévisions futures.

---

## 7. Maintenance et améliorations possibles

### Performances

- Ajuster les paramètres d’entraînement pour améliorer les temps de traitement.
- Utiliser `use_bulk_insert=True` dans `save_predictions_to_db` pour des insertions plus rapides.

### Précision du modèle

- Ajouter d’autres sources de données (vaccinations, mesures gouvernementales).
- Essayer des architectures de modèles alternatives (LSTM, XGBoost).
- Intégrer des données démographiques par région.

### Visualisation

- Développer un tableau de bord interactif pour explorer les prédictions.
- Ajouter des intervalles de confiance aux prédictions.

---

## 8. Résolution des problèmes courants

### Erreur "cannot convert float NaN to integer"

- Vérifiez que les données source ne contiennent pas de valeurs NaN.
- Le modèle inclut désormais une protection contre les NaN.

### Problèmes de connexion à la base de données

- Vérifiez les paramètres dans le fichier `.env`.
- Assurez-vous que la base de données est accessible.

### Erreurs d’entraînement du modèle

- Utiliser l’option `test_mode=True` pour un entraînement plus simple.
- Réduire la taille des données avec `df.tail(1000)` pour les tests.

---

## 9. Définition de la classe et des méthodes

### `__init__()`
Initialise le modèle de prévision COVID avec les composants essentiels : scalers pour la normalisation des données, connexion à la base de données et définition des caractéristiques de base pour l’apprentissage.

### `fetch_data(region_id=None)`
Récupère les données COVID depuis la base de données. Filtre par région si un identifiant est fourni. Retourne un DataFrame contenant les cas, décès, guérisons et informations géographiques.

### `clean_extreme_values(df)`
Nettoie les valeurs aberrantes ou infinies dans les données. Remplace les valeurs extrêmes par des seuils raisonnables (99e percentile) et les valeurs manquantes par la médiane de chaque colonne.

### `preprocess_data(df)`
Prépare les données brutes pour l’apprentissage automatique. Crée des caractéristiques temporelles (jour de semaine, mois, saison), calcule des taux (croissance, mortalité), génère des variables décalées et des moyennes mobiles pour capturer les tendances.

### `prepare_train_test(df, test_size=0.2)`
Divise chronologiquement les données en ensembles d’entraînement et de test. Normalise les données et vérifie leur intégrité. Conserve l’ordre temporel des données pour respecter la nature séquentielle des séries temporelles.

### `train(X_train, y_train)`
Entraîne un modèle RandomForest avec optimisation des hyperparamètres via RandomizedSearchCV. Recherche la meilleure configuration parmi différentes combinaisons de paramètres (nombre d’arbres, profondeur, etc.).

### `evaluate(X_test, y_test)`
Évalue les performances du modèle sur les données de test en calculant des métriques standard : MSE, RMSE, MAE et R². Affiche les résultats et retourne les prédictions pour comparaison.

### `predict_future(df, days=30)`
Génère des prédictions jour par jour pour une période future spécifiée. Utilise une approche itérative où chaque prédiction devient une entrée pour les prédictions suivantes, simulant ainsi la progression temporelle des cas COVID.

### `extrapolate_to_2023(df)`
Étend les données historiques jusqu’à fin 2023 en utilisant un modèle de croissance contrôlé. Calcule les nouveaux cas, décès et guérisons en fonction des tendances récentes, avec des limites pour éviter les valeurs irréalistes.

### `predict_2023_safe(region_name=None, retry_with_subset=True)`
Version robuste de `predict_2023` avec mécanisme de repli automatique. En cas d’erreur (valeurs infinies), réessaie avec un sous-ensemble réduit de données pour garantir la génération de prédictions.

### `save_model(path='model')`
Sauvegarde le modèle entraîné, les scalers et la liste des caractéristiques dans un dossier spécifié. Permet de réutiliser ultérieurement le modèle sans réentraînement.

### `load_model(path='model')`
Charge un modèle préalablement entraîné depuis un dossier spécifié. Restaure le modèle, les scalers et la liste des caractéristiques pour continuer les prédictions.

### `plot_predictions(y_test, y_pred, test_dates, future_df=None)`
Génère et sauvegarde un graphique comparant les cas réels, les prédictions sur les données de test et les prédictions futures. Permet de visualiser la performance du modèle et ses projections.

### `predict_2023(region_name=None)`
Fonction principale pour générer des prédictions COVID pour l’année 2023. Récupère les données, les prétraite, entraîne le modèle, évalue sa performance et génère les prédictions pour toute l’année. Sauvegarde les résultats dans la base de données et génère des visualisations.
