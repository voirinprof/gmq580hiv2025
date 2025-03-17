from flask import Flask, render_template
from sqlalchemy import create_engine, text
import os

app = Flask(__name__, template_folder='/app/templates')

# Récupération des variables d'environnement pour la base de données
DATABASE_URL = os.environ.get('DATABASE_URL', f'postgresql://test_user:test_db@test_host/test_db')

@app.route('/')
def home():
    # Connexion à la base de données
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        # Récupération des points géographiques
        result = conn.execute(text("SELECT name, ST_X(geom) as longitude, ST_Y(geom) as latitude FROM points;"))
        points = [dict(row) for row in result.mappings()]  # Convertir les résultats en dictionnaire
    
    # Rendre le template HTML avec les données
    return render_template('index.html', points=points)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
