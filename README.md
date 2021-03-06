# Full Stack Casting Agency API

## Project Content
This is the project is the Udacity capstone project. Dealing with a casting agency with RBAC authentication API design.
Cover topics inclue
1. Database design with ```postgres``` and ```sqlalchemy```
2. API design using ```Flask``` framework
3. Test script design
4. Authentication for roles via ```Auth0```
5. Deployment on ```Heroku```

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup

Before flushing the data into the database, we need to create the database named 'casting_agent' via:
```bash
createdb casting_agent
```
You can try to construct a psql file to flush data in to the database.
In this project, I initialize the data by drop_and_create_all function in model.py file.
## Running the server

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py` directs flask to use the `app.py` file to find the application. 


## API Documentation
You can run it locally with flask run just like descibe above.
Or can get the data from deplied heroku app.
To utilize curl and heroku app with authentication, 
```
TOKEN=<bearer token>
```
You can find the token in config.py file.

### Base URL
https://jeffrey-casting-agency.herokuapp.com/


### Actors
GET ```/actors```
- Fetches a list of actors in which contains in the database.
- Request Arguments: None
- Permission: ```get:actors```
- Returns: An object with a single key, actors, that contains an object of id, name, age, gender.
- METHOD URL: ``` curl -X GET -H "Authorization:Bearer ${TOKEN}" "https://jeffrey-casting-agency.herokuapp.com/actors" ```
- Sample: 
```bash
{
  "actors": [
    {
      "Age": 20,
      "Gender": "Male",
      "Id": 2,
      "Name": "Jeffrey"
    }
  ],
  "success": true,
  "total_actors": 1
}

```

POST ```/actors```
- Post method to post new actor to the database
- Arguments: name, gender, age.
- Permission: ```post:actors```
- METHOD URL: ``` curl -X POST -H "Authorization:Bearer ${TOKEN}" -H "Content-Type: application/json" -d '{"name":"Ryan", "age":34, "gender":"Male"}' "https://jeffrey-casting-agency.herokuapp.com/actors"  ```
- Sample:
```bash
{
  "actors": [
    {
      "Age": 34,
      "Gender": "Male",
      "Id": 3,
      "Name": "Ryan"
    }
  ],
  "created": 3,
  "success": true,
  "total_actors": 2
}
```

UPDATE ```/actors/<int:actor_id>```
- Update the current actor information in the database.
- Arguments: actor_id, new name/gender/age. If not specified with any of the content, it will remain the same.
- Permission: ```patch:actors```
- METHOD URL: ```curl -X PATCH -H "Authorization:Bearer ${TOKEN}" -H "Content-Type: application/json" -d '{"age":22}' "https://jeffrey-casting-agency.herokuapp.com/actors/2" ```
- Sample:
```bash
{
  "edit_actor": 2,
  "success": true,
  "total_actors": 2
}
```

DELETE ```/actors/<int:actor_id>```
- Delete actor by providing actor id
- reutrn status of delete and deleted actor id
- METHOD URL: ```  curl -X DELETE -H "Authorization:Bearer ${TOKEN}" "https://jeffrey-casting-agency.herokuapp.com/actors/1" ```
- Sample:
```bash
{
  "deleted": 1,
  "success": true
}
```

### Movies

GET ```/movies```
- Fetches a list of movies that contains in the database
- Return an object that inclues title, release date.
- Permission: ```get:movies```
- METHOD URL: ``` curl -X GET -H "Authorization:Bearer ${TOKEN}" "https://jeffrey-casting-agency.herokuapp.com/movies" ```
- Sample:
```bash
{
  "movies": [
    {
      "Id": 1,
      "Release Date": "Fri, 24 Oct 2014 00:00:00 GMT",
      "Title": "John Wick"
    },
    {
      "Id": 2,
      "Release Date": "Fri, 24 Oct 2014 00:00:00 GMT",
      "Title": "John Wick"
    }
  ],
  "success": true,
  "total_movies": 2
}
```

POST ```/movies```
- Post a new movie to the database.
- Arguments: title, release_date
- Permission: ```post:movies```
- METHOD URL: ``` curl -X POST -H "Authorization:Bearer ${TOKEN}" -H "Content-Type: application/json" -d '{"title":"John Wick 2", "release_date":"2017-2-10"}' "https://jeffrey-casting-agency.herokuapp.com/movies" ```
- Sample:
```bash
{
  "created": 3,
  "movies": [
    {
      "Id": 3,
      "Release Date": "Fri, 10 Feb 2017 00:00:00 GMT",
      "Title": "John Wick 2"
    }
  ],
  "success": true,
  "total_movies": 2
}
```

UPDATE ```/movies/<int:movie_id>```
- Update the movie info in the current database.
- Arguments: Must provide a valid movie id to update. new title, new release date should be provided; otherwise, the info will remain the same.
- METHOD URL: ``` curl -X PATCH -H "Authorization:Bearer ${TOKEN}" -H "Content-Type: application/json" -d '{"title":"John Wick 3", "release_date":"2019-7-10"}' "https://jeffrey-casting-agency.herokuapp.com/movies/1" ```
- Sample:
``` bash
{
  "edit_movie": 1,
  "success": true,
  "total_movies": 2
}
```

DELETE ```/movies/<int:movie_id>```
- Remove movie from database.
- Arguments: movie_id.
- Permission: ```delete:movies```.
- METHOD URL: ``` curl -X DELETE -H "Authorization:Bearer ${TOKEN}" "https://jeffrey-casting-agency.herokuapp.com/movies/2" ```
- Sample:
``` bash
{
  "deleted": 2,
  "success": true
}
```

## Error handling

The error will be return as JSON format as followed:
Not found error (404)
```bash
{
"error": 404,
"message": "not found",
"success": false
}

```
Unprocessable error (422)
```bash
{
"error": 422,
"message": "unprocessable entity",
"success": false
}
```

Authentication error(401)
```bash
{
  'success': False,
  'error': 401,
  'message': 'Authorization header is expected.'
}
```
Permission not found(403)
```bash
{
  'success': False,
  'error': 403,
  'message': 'Permission not found.
}
```

## Authentication setup
1. Create account in Auth0.
2. Create Application in the service.
3. Select Regular Web Application.
4. Create API by clicking API Tab.
5. Enable RBAC in the API.
6. Create new Role.
7. Create and assign permissions.

## Testing
To run the tests, run
```
python test_app.py
```

Sample
```
.........................
----------------------------------------------------------------------
Ran 25 tests in 9.642s

OK
```
PS. The test_app.py file include function that drop database and create a new test database each time it runs. I will flush fresh data to test.

## Authors
Jeffrey Lee is in charged of backend Web Api in (app.py) (auth.py) and (test_app.py) . Also the README in the backend.
Authentication service is provided by third party Auth0
All other files are contributed by Udacity- Full Stack Web Developer Nanodegree.
