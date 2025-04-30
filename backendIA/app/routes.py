from flask import Blueprint, jsonify
from app.models import db
from sqlalchemy.sql import text
from app.services import get_all_data_from_pandemics, get_all_data_from_continents

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