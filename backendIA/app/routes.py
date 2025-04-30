from flask import Blueprint, jsonify
from app.models import db
from sqlalchemy.sql import text

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