from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Continent(db.Model):
    id_continents = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

class Country(db.Model):
    id_countries = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    id_continents = db.Column(db.Integer, db.ForeignKey('continent.id_continents'), nullable=False)

class Region(db.Model):
    id_regions = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    id_continents = db.Column(db.Integer, db.ForeignKey('continent.id_continents'), nullable=False)

class Pandemic(db.Model):
    id_pandemics = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

class TotalByDay(db.Model):
    id_pandemics = db.Column(db.Integer, db.ForeignKey('pandemic.id_pandemics'), primary_key=True)
    id_regions = db.Column(db.Integer, db.ForeignKey('region.id_regions'), primary_key=True)
    case_count = db.Column(db.Integer, nullable=False)
    death = db.Column(db.Integer, nullable=False)
    recovered = db.Column(db.Integer, nullable=False)
    date_by_day = db.Column(db.Date, primary_key=True)