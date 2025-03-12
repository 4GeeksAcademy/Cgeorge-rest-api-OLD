import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, FavPeople, FavPlanets

# Configuración inicial
app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = db_url.replace("postgres://", "postgresql://") if db_url else "sqlite:////tmp/test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Manejo de errores
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Sitemap de la API
@app.route("/")
def sitemap():
    return generate_sitemap(app)

#  ENDPOINTS: PEOPLE
@app.route("/people", methods=["GET"])
def get_all_people():
    people = People.query.all()
    results = [person.serialize() for person in people]
    return jsonify({"msg": "List of all characters", "people": results}), 200


@app.route("/people/<int:people_id>", methods=["GET"])
def get_person(people_id):
    person = People.query.get_or_404(people_id)
    return jsonify({"msg": "Information of characters", "person": person.serialize()}), 200

#  ENDPOINTS: PLANETS
@app.route("/planets", methods=["GET"])
def get_all_planets():
    planets = Planets.query.all()
    results = [planet.serialize() for planet in planets]
    return jsonify({"msg": "Planet List", "planets": results}), 200


@app.route("/planets/<int:planet_id>", methods=["GET"])
def get_planet(planet_id):
    planet = Planets.query.get_or_404(planet_id)
    return jsonify({"msg": "Planet details", "planet": planet.serialize()}), 200

#  ENDPOINTS: USERS
@app.route("/users", methods=["GET"])
def get_all_users():
    users = User.query.all()
    results = [user.serialize() for user in users]
    return jsonify({"msg": "List of users", "users": results}), 200

#  ENDPOINTS: FAVORITES
@app.route("/users/favorites", methods=["GET"])
def get_user_favorites():
    user_id = 1  
    fav_people = FavPeople.query.filter_by(user_id=user_id).all()
    fav_planets = FavPlanets.query.filter_by(user_id=user_id).all()

    return jsonify({
        "msg": f"Favoritos del usuario {user_id}",
        "people_favorites": [fav.people.serialize() for fav in fav_people],
        "planets_favorites": [fav.planet.serialize() for fav in fav_planets]
    }), 200

@app.route("/favorite/people/<int:people_id>", methods=["POST"])
def add_people_favorite(people_id):
    user_id = 1  
    new_fav = FavPeople(user_id=user_id, people_id=people_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({"msg": "Character added to favorites"}), 201

@app.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def add_planet_favorite(planet_id):
    user_id = 1  
    new_fav = FavPlanets(user_id=user_id, planet_id=planet_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({"msg": "Planet added to favorites"}), 201

@app.route("/favorite/people/<int:people_id>", methods=["DELETE"])
def delete_people_favorite(people_id):
    user_id = 1  
    fav = FavPeople.query.filter_by(user_id=user_id, people_id=people_id).first()
    if not fav:
        return jsonify({"msg": "Not found"}), 404
    db.session.delete(fav)
    db.session.commit()
    return jsonify({"msg": "Favorite removed"}), 200

@app.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
def delete_planet_favorite(planet_id):
    user_id = 1  # Supongo que el ID de usuario es 1 para este ejemplo
    fav = FavPlanets.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not fav:
        return jsonify({"msg": "Not found"}), 404
    db.session.delete(fav)
    db.session.commit()
    return jsonify({"msg": "Favorite removed"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 3000)), debug=False)
