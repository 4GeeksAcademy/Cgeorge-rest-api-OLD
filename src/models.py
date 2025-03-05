from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}>"

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }


class People(db.Model):
    __tablename__ = "people"
    
    people_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    hair_color = db.Column(db.String(50), nullable=False)
    eye_color = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<People {self.name}>"

    def serialize(self):
        return {
            "people_id": self.people_id,
            "name": self.name,
            "height": self.height,
            "weight": self.weight,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color
        }


class Planets(db.Model):
    __tablename__ = "planets"

    planet_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    climate = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Planets {self.name}>"

    def serialize(self):
        return {
            "planet_id": self.planet_id,
            "name": self.name,
            "diameter": self.diameter,
            "climate": self.climate
        }


class FavPeople(db.Model):
    __tablename__ = "favpeople"
    
    favpeople_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey("people.people_id"), nullable=False)

    user = db.relationship("User", backref="favpeople")
    people = db.relationship("People", backref="favorited_by")

    def __repr__(self):
        return f"<FavPeople user_id={self.user_id}, people_id={self.people_id}>"

    def serialize(self):
        return {
            "favpeople_id": self.favpeople_id,
            "user_id": self.user_id,
            "people_id": self.people_id
        }


class FavPlanets(db.Model):
    __tablename__ = "favplanets"
    
    favplanets_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.planet_id"), nullable=False)

    user = db.relationship("User", backref="favplanets")
    planet = db.relationship("Planets", backref="favorited_by")

    def __repr__(self):
        return f"<FavPlanets user_id={self.user_id}, planet_id={self.planet_id}>"

    def serialize(self):
        return {
            "favplanets_id": self.favplanets_id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }
