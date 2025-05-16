from flask import Blueprint, jsonify
from app.models import db
from sqlalchemy.sql import text
from app.services import get_all_data_from_pandemics, get_all_data_from_continents
from app.ia_model import CovidForecaster

main = Blueprint('main', __name__)

@main.route('/test_db_connection', methods=['GET'])
def test_db_connection():
    try:
        # Tenter une connexion à la base de données
        db.session.execute(text('SELECT 1'))
        return jsonify({"message": "Connection to the database successful!"}), 200
    except Exception as e:
        print(f"Database connection error: {e}") 
        return jsonify({"message": "Connection to the database failed!", "error": str(e)}), 500


@main.route('/get_data/<pandemics>', methods=['GET'])
def get_data_pandemics(pandemics):
    try:
        data = get_all_data_from_pandemics(pandemics)
        if not data:
            return jsonify({"message": f"Aucune donnée trouvée pour la pandémie '{pandemics}'"}), 404
        return jsonify({"data": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/get_data/<continents>', methods=['GET'])
def get_data_continents(continents):
    try:
        data = get_all_data_from_continents(continents)
        return jsonify({"data": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/get_data/<regions>', methods=['GET'])
def get_data_regions(regions):
    try:
        data = get_all_data_from_regions(regions)
        return jsonify({"data": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/get_data/<countries>', methods=['GET'])
def get_data_countries(countries):
    try:
        data = get_all_data_from_countries(countries)
        return jsonify({"data": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/get_data/<total_by_day>', methods=['GET'])
def get_data_total_by_day(total_by_day):
    try:
        data = get_all_data_from_total_by_day(total_by_day)
        return jsonify({"data": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/predict_2023/<region_name>', methods=['GET'])
def predict_2023_region(region_name):
    """Prédire les cas COVID pour 2023 pour une région spécifique"""
    try:
        forecaster = CovidForecaster()
        predictions = forecaster.predict_2023(region_name)
        
        return jsonify({
            "region": region_name,
            "predictions_2023": predictions.to_dict(orient='records')
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@main.route('/train_predict', methods=['POST'])
def train_and_predict():
    """
    Lance le workflow d'entraînement et de prédiction IA.
    """
    try:
        region_name = request.json.get('region_name') if request.is_json else None
        forecaster = CovidForecaster()
        predictions = forecaster.predict_2023(region_name)
        if predictions is not None:
            return jsonify({
                "status": "success",
                "message": "Modèle entraîné et prédictions générées.",
                "nb_predictions": len(predictions),
            }), 200
        else:
            return jsonify({"status": "error", "message": "Aucune prédiction générée."}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500