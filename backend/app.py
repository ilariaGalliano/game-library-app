from flask import Flask,  redirect, render_template, request, session, url_for, jsonify
from flask_cors import CORS
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["DEBUG"] = True

# update app constantly
app.config.from_object(__name__)

CORS(app, resources={r"/*":{'origins':"*"}})

db = "games.db"

def dict_factory(cursor, row):
    """Convert DB items into dictionary objects.
    
    This function convert items from the db in the form of a dictionary instead than of a list. 
    It ensure a proper jsonification of the items.
    Returns dictionary item
    """
    d = dict()
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
 

@app.route("/")
def helloWorld():
  return "Hello, world!"

# routing error page 404
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>OOPS</h1> <p> Page not found </p>", 404

# routing full view of albums list
@app.route('/api/v1/resources/games/all', methods=["GET"])
def api_all():
    conn = sqlite3.connect(db)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_album = cur.execute("SELECT * FROM games;").fetchall()

    return jsonify(all_album)

# routing api connection to album db
@app.route("/api/v1/resources/games", methods=["GET"])
def api_filter():
    """API items availables at the date
    
    Currently the following parameters have been instantiated: id_key (primary key), artist, album and genre.
    """
    query_parameters = request.args
    
    id_key = query_parameters.get("id")
    name = query_parameters.get("name")
    played = query_parameters.get("played")
    genre = query_parameters.get("genre")
    
    #building our SQL query
    query = "SELECT * FROM games WHERE"
    to_filter = []
    
    if id_key:
        query += ' id=? AND'
        to_filter.append(id_key)
    if name:
        query += ' name=? AND'
        to_filter.append(name)
    if played:
        query += ' played=? AND'
        to_filter.append(played)
    if genre:
        query += ' genre=? AND'
        to_filter.append(genre)
    if not (id_key or name or played or genre):
        return page_not_found(404)
    
    # this is needed to clean the SQL query after the last item is added; 
    # basically it removes the " AND" and add a ";"
    query = query[:-4] + ";"
    
    conn = sqlite3.connect(db)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    
    results = cur.execute(query, to_filter).fetchall()
    
    return jsonify(results)

@app.route("/games", methods=['GET'])
def games():
  return "Games"

@app.route("/login-test", methods=["GET", "POST"])
def login_test():
    """Log user in"""
    query_parameters = request.args
    
    id_key = query_parameters.get("id")
    name = query_parameters.get("name")
    email = query_parameters.get("email")
    password = query_parameters.get("password")
    
    #building our SQL query
    query = "SELECT * FROM users WHERE"
    to_filter = []
    
    if id_key:
        query += ' id=? AND'
        to_filter.append(id_key)
    if name:
        query += ' name=? AND'
        to_filter.append(name)
    if email:
        query += ' email=? AND'
        to_filter.append(email)
    if password:
        query += ' password=? AND'
        to_filter.append(password)
    if not (id_key or name or email or password):
        return page_not_found(404)
    
    # this is needed to clean the SQL query after the last item is added; 
    # basically it removes the " AND" and add a ";"
    query = query[:-4] + ";"
    
    conn = sqlite3.connect(db)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    
    results = cur.execute(query, to_filter).fetchall()
    
    return jsonify(results)

@app.route("/login", methods=["GET", "POST"])
def login():
        conn = sqlite3.connect(db)
        conn.row_factory = dict_factory
        cur = conn.cursor()
        all_users = cur.execute("SELECT * FROM users;").fetchall()

        return jsonify(all_users)

@app.route("/register", methods=["GET", "POST"])
def register():
        data = request.get_json()
        print(data)
        name = data['name']
        email = data['email']
        password = data['password']

        conn = sqlite3.connect(db)
        conn.row_factory = dict_factory
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name,email,password) VALUES(%s, %s, %s, %s)", (name,email,password))

        return jsonify({'Method':'POST', 'message':'New user created successfully'})
   

# run the app
if __name__ == "__main__":
  app.run(debug=True, use_reloader=False)
