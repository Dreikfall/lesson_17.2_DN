from flask import Flask, request
from flask_restx import Api, Resource
from models import db, Movie, Genre, Director, all_table_add
from schema import movie_schema, movies_schema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 2, 'sort_keys': False}
app.config['JSON_SORT_KEYS'] = False

db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()
    all_table_add()

api = Api(app)
movies_ns = api.namespace("movies")


@movies_ns.route("")
class MoviesView(Resource):
    def get(self):
        """
        Для получения всего списка фильмов отправляется запрос типа
        http://127.0.0.1:5000/movies

        Для получения списка фильмов по id режиссера отправляется запрос типа
        http://127.0.0.1:5000/movies?director_id=2

        Для получения списка фильмов по id жанров отправляется запрос типа
        http://127.0.0.1:5000/movies?genre_id=4

        Для получения списка фильмов по id режиссера и id жанров отправляется запрос типа
        http://127.0.0.1:5000/movies?director_id=2&genre_id=17
        """
        movies_query = db.session.query(Movie.id, Movie.title, Movie.description, Movie.trailer,
                                        Movie.year, Movie.rating, Genre.name.label('genre'),
                                        Director.name.label('director')).join(Genre).join(Director)

        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')

        if director_id:
            movies_query = movies_query.filter(Movie.director_id == director_id)

        if genre_id:
            movies_query = movies_query.filter(Movie.genre_id == genre_id)

        movies_all = movies_query.all()
        return movies_schema.dump(movies_all), 200

    def post(self):

        """
        Для добавления модели фильмов отправляется запрос типа
        http://127.0.0.1:5000/movies типа
        {"title": "a", "description": "b", "trailer": "c", "year": 2000, "rating": 4.5, "genre_id": 1, "director_id": 1}
        """

        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
        return "", 201


@movies_ns.route("/<int:mid>")
class MovieView(Resource):
    def get(self, mid):
        """
        Возвращает подробную информацию о фильме по его id.
        Отправляется запрос типа http://127.0.0.1:5000/movies/1
        """
        try:
            movie_id = db.session.query(Movie.id, Movie.title, Movie.description, Movie.trailer,
                                        Movie.year, Movie.rating, Genre.name.label('genre'),
                                        Director.name.label('director')).join(Genre).join(Director).filter(
                Movie.id == mid).one()
            return movie_schema.dump(movie_id)
        except Exception as e:
            return str(e), 404

    def put(self, mid):
        """
        Изменение полей модели как частичной так и полной.
        Отправляется запрос типа http://127.0.0.1:5000/movies/1
        """
        data = movie_schema.load(request.json)
        db.session.query(Movie).filter(Movie.id == mid).update(data)
        db.session.commit()
        return "", 204

    def delete(self, mid):
        """
        Удаление объекта.
        Отправляется запрос типа http://127.0.0.1:5000/movies/1
        """
        db.session.query(Movie).filter(Movie.id == mid).delete()
        db.session.commit()
        return "", 204


if __name__ == '__main__':
    app.run(debug=True)
