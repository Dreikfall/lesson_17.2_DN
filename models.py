import data
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


def all_table_add():
    for movie in data.data["movies"]:
        m = Movie(
            id=movie["pk"],
            title=movie["title"],
            description=movie["description"],
            trailer=movie["trailer"],
            year=movie["year"],
            rating=movie["rating"],
            genre_id=movie["genre_id"],
            director_id=movie["director_id"],
        )
        with db.session.begin():
            db.session.add(m)

    for director in data.data["directors"]:
        d = Director(
            id=director["pk"],
            name=director["name"],
        )
        with db.session.begin():
            db.session.add(d)

    for genre in data.data["genres"]:
        d = Genre(
            id=genre["pk"],
            name=genre["name"],
        )
        with db.session.begin():
            db.session.add(d)
