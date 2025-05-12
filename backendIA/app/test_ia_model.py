import pandas as pd
import numpy as np
from app.ia_model import CovidForecaster

def test_minimal():
    """Test minimal du modèle sans optimisation d'hyperparamètres"""
    print("Test minimal du modèle de prédiction COVID")
    
    # Initialiser le modèle
    forecaster = CovidForecaster()
    
    # Récupérer un échantillon de données limité (100 dernières entrées)
    df = forecaster.fetch_data()
    if df.empty:
        print("Erreur: Aucune donnée récupérée")
        return
    
    df = df.sort_values('date').tail(100)
    print(f"Échantillon réduit: {len(df)} entrées")
    
    # Prétraitement
    df = forecaster.preprocess_data(df)
    
    # Train/test split
    X_train, X_test, y_train, y_test, test_dates = forecaster.prepare_train_test(df, test_size=0.2)
    
    
    from sklearn.ensemble import RandomForestRegressor
    model = RandomForestRegressor(n_estimators=10, max_depth=5, random_state=42)
    
    # Entraînement rapide
    print("Entraînement du modèle (version rapide)...")
    model.fit(X_train, y_train)
    forecaster.model = model
    
    # Évaluation
    y_pred = forecaster.evaluate(X_test, y_test)
    
    # Prédiction
    predictions = forecaster.predict_future(df, days=30)
    print(predictions.head())
    
    return "Test terminé avec succès"

if __name__ == "__main__":
    test_minimal()