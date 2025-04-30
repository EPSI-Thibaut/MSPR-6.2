from app.models import db
from sqlalchemy.sql import text

def get_all_data_from_pandemics(pandemics):
    query = f"SELECT * FROM {pandemics}"
    result = db.session.execute(text(query))
    # Convertir chaque ligne en dictionnaire
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]

def get_all_data_from_continents(continents):
    query = f"SELECT * FROM {continents}"
    result = db.session.execute(text(query))
    # Convertir chaque ligne en dictionnaire
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]

def get_all_data_from_countries(regions):
    query = f"SELECT * FROM {regions}"
    result = db.session.execute(text(query))
    # Convertir chaque ligne en dictionnaire
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]

def get_all_data_from_countries(countries):
    query = f"SELECT * FROM {countries}"
    result = db.session.execute(text(query))
    # Convertir chaque ligne en dictionnaire
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]

def get_all_data_from_total_by_day(total_by_day):
    query = f"SELECT * FROM {total_by_day}"
    result = db.session.execute(text(query))
    # Convertir chaque ligne en dictionnaire
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]