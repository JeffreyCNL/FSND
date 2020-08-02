import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Actor, Movie, setup_db, drop_and_create_all
from auth import requires_auth, AuthError
import sys

DATA_PER_PAGE = 10
def myPrint(obj):
  print(obj, file=sys.stderr)

def paginate_data(request, data):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * DATA_PER_PAGE
  end = start + DATA_PER_PAGE
  formatted  = [obj.format() for obj in data]
  current = formatted[start:end]
  return current

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  # drop_and_create_all()
  CORS(app, resources={r"/api/*": {"origins": "*"}})

  # Use the after_request decorator to set Access-Control-Allow
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response


  # Actors
  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_actors(payload):
    try:
      actors = Actor.query.order_by(Actor.id).all()
      if len(actors) == 0:
        abort(404)
      current_actors = paginate_data(request, actors)
      if len(current_actors) == 0:
        abort(404)
      return jsonify({
        'success': True,
        'actors': current_actors,
        'total_actors':len(actors)
      })
    except:
      abort(404)

  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(payload, actor_id):
    try:
      actor = Actor.query.get(actor_id)
      if actor is None:
        abort(404)
      actor.delete()
      return jsonify({
        'success': True,
        'deleted': actor_id
      })
    except:
      abort(422)

  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def create_actor(payload):
    body = request.get_json()
    if body is None:
      abort(422)
    new_name = body.get('name', None)
    new_age = body.get('age', None)
    new_gender = body.get('gender', None)

    if ((new_name == '') or (new_age == '') or (new_gender == '')):
      abort(422)
    try:
      actor = Actor(name=new_name, age=new_age, gender=new_gender)
      actor.insert()
      selection = Actor.query.filter(Actor.id == actor.id).order_by(Actor.id).all()
      current_actors = paginate_data(request, selection)
      return jsonify({
        'success': True,
        'created': actor.id,
        'actors': current_actors,
        'total_actors': len(Actor.query.all())
      })
    except:
      abort(422)

  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def edit_actor(payload, actor_id):
    body = request.get_json()
    if body is None:
      abort(422)    
    edit_actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if edit_actor is None:
      abort(404)
    try:
      # if there's no new input, remain the same
      new_name = body.get('name', edit_actor.name)
      new_age = body.get('age', edit_actor.age)
      new_gender = body.get('gender', edit_actor.gender)
      # set the updated value
      edit_actor.name = new_name
      edit_actor.age = new_age
      edit_actor.gender = new_gender
      edit_actor.update()
      return jsonify({
        'success': True,
        'edit_actor': actor_id,
        'total_actors': len(Actor.query.all())
      })
    except:
      abort(404)

  # Movies
  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def get_movies(payload):
    try:
      movies = Movie.query.order_by(Movie.id).all()
      if len(movies) == 0:
        abort(404)
      current_movies = paginate_data(request, movies)
      if len(current_movies) == 0:
        abort(404)
      return jsonify({
        'success': True,
        'movies': current_movies,
        'total_movies': len(movies)
      })
    except:
      abort(404)
 
  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(payload,movie_id):
    try:
      movie = Movie.query.get(movie_id)
      if movie is None:
        abort(404)
      movie.delete()
      return jsonify({
        'success': True,
        'deleted': movie_id
      })
    except:
      abort(422)

  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def create_movie(payload):
    body = request.get_json()
    if body is None:
      abort(422)
    new_title = body.get('title', None)
    new_release_date = body.get('release_date', None)

    if ((new_title == '') or (new_release_date == '')):
      abort(422)
    try:
      movie = Movie(title=new_title, release_date=new_release_date)

      movie.insert()
      selection = Movie.query.filter(Movie.id == movie.id).order_by(Movie.id).all()
      current_movies = paginate_data(request, selection)
      return jsonify({
        'success': True,
        'created': movie.id,
        'movies': current_movies,
        'total_movies': len(Movie.query.all())
      })
    except:
      abort(422)

  
  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def edit_movie(payload,movie_id):
    body = request.get_json()
    if body is None:
      abort(422)
    
    edit_movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if edit_movie is None:
      abort(422)
    try:
      new_title = body.get('title', edit_movie.title)
      new_release_date = body.get('release_date', edit_movie.release_date)

      edit_movie.title = new_title
      edit_movie.release_date = new_release_date
      edit_movie.update()
      return jsonify({
        'success': True,
        'edit_movie': movie_id,
        'total_movies': len(Movie.query.all())
      })
    except:
      abort(422)

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'not found'
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'unprocessable entity'
    }), 422

  @app.errorhandler(AuthError)
  def authentication_failure(AuthError):
    return jsonify({
      'success': False,
      'error': AuthError.status_code,
      'message': AuthError.error['description']
    }), AuthError.status_code

  return app

app = create_app()

if __name__ == '__main__':
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=8080, debug=True)

