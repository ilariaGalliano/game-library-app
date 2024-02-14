from flask import Flask,  redirect, render_template, request, session, url_for, jsonify
from flask_cors import CORS
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
import datetime
import os

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = os.urandom(24)



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

# routing api connection to album db
@app.route("/resources/games", methods=["GET", "POST"])
def api_filter():
    token = session.get('token')

    query_parameters = request.args
    
    id_key = query_parameters.get("id")
    name = query_parameters.get("name")
    genre = query_parameters.get("genre")
    played = query_parameters.get("played")
    user_id = query_parameters.get("user_id")
    
    # Building our SQL query
    query = "SELECT * FROM games WHERE 1=1"  # Start with a base query to ensure all conditions are added correctly
    to_filter = []
    
    if id_key:
        query += ' AND id=?'
        to_filter.append(id_key)
    if name:
        query += ' AND name=?'
        to_filter.append(name)
    if played:
        query += ' AND played=?'
        to_filter.append(played)
    if genre:
        query += ' AND genre=?'
        to_filter.append(genre)
    if user_id:
        query += ' AND user_id=?'
        to_filter.append(user_id)
    
    conn = sqlite3.connect(db)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    
    results = cur.execute(query, to_filter).fetchall()

    if request.method == "POST":
        data = request.get_json()
        
        id = data['id']
        name = data['name']
        genre = data['genre']
        played = data['played']
        user_id = data['user_id']

        # Insert new game into the database
        cur.execute("INSERT INTO games (id, name, genre, played, user_id) VALUES (?, ?, ?, ?, ?)",
                    (id, name, genre, played, user_id))
        conn.commit()

        return jsonify({'message': 'Game inserted successfully'}), 201
    
    conn.close()  # Close the connection after fetching results
    
    return jsonify(results)


@app.route('/resources/games/all', methods=["GET", "POST"])
def api_all():
    # Check if user is logged in
    token = session.get('token')
    if not token:
        return jsonify({'error': 'User not logged in'}), 401

    # Decode the token to get the user_id
    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'])
        user_id = decoded_token.get('user_id')
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token is expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401


    conn = sqlite3.connect(db)
    conn.row_factory = dict_factory
    cur = conn.cursor()

    if request.method == "POST":
        data = request.get_json()
        
        id = data['id']
        name = data['name']
        genre = data['genre']
        played = data['played']

        # Insert new game into the database
        cur.execute("INSERT INTO games (id, name, genre, played, user_id) VALUES (?, ?, ?, ?, ?)",
                    (id, name, genre, played, user_id))
        conn.commit()

        return jsonify({'message': 'Game inserted successfully'}), 201


    # Fetch all games associated with the logged-in user
    all_games = cur.execute("SELECT * FROM games WHERE user_id=?",(user_id,)).fetchall()
        
    conn.close()

    return jsonify(all_games)

@app.route("/resources/edit_game/<int:id>", methods=["PUT"])
def put(id):
    data = request.get_json()
    print(data)
    name = data['name']
    genre = data['genre']
    played = data['played']

    conn = sqlite3.connect(db)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute("UPDATE games SET name=?, genre=?, played=? WHERE id=?", (name, genre, played, id))
    conn.commit()
    return jsonify({'Method': 'PUT', 'message': 'Game updated successfully'})


@app.route("/resources/delete_game/<int:id>", methods=["DELETE"])
def delete_game(id):
        conn = sqlite3.connect(db)
        conn.row_factory = dict_factory
        cur = conn.cursor()
        cur.execute("DELETE FROM games WHERE id=?", (id,))
        conn.commit()
        return jsonify({'Method':'DELETE', 'message':'Game deleted'}) 

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({'error': 'Please provide name, email, and password'}), 400

    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Registration successful'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Please provide email and password'}), 400

    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT id, email FROM users WHERE email=? AND password=?", (email, password))
    user = c.fetchone()
    conn.close()

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    # Check if the provided password matches the stored password
    if user:  # password == user[3] password is stored in the fourth column
       user_id, email=user 
       token = jwt.encode({'user_id': user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
       return jsonify({'message': 'Login successful', 'token': token }), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401
    
@app.route('/api/data')
def view_data():
    conn = sqlite3.connect(db)  
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')  
    rows = cur.fetchall()
    conn.close()

    # Convert data to a list of dictionaries for JSON serialization
    data = [dict(row) for row in rows]

    return jsonify(data)

# run the app
if __name__ == "__main__":
  app.run(debug=True, use_reloader=False)
