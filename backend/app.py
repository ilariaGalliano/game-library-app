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

# routing full view of games list
@app.route('/resources/games/all', methods=["GET", "POST"])
def api_all():
    conn = sqlite3.connect(db)
    conn.row_factory = dict_factory
    cur = conn.cursor()

    if request.method == "POST":
        data = request.get_json()
        print(data)
        id = data['id']
        name = data['name']
        genre = data['genre']
        played = data['played']
    # Add into db
        new_game = cur.execute("INSERT INTO games (id,name,genre,played) VALUES(?,?,?,?)", (id,name,genre,played))
        conn.commit()
        print(new_game, "record inserted.")
    
    all_album = cur.execute("SELECT * FROM games;").fetchall()
        
    return jsonify(all_album)


# @app.route('/resources/games/all', methods=["GET", "POST"])
# def api_all():
#     # Check if user is logged in

#     user_id = session.get('user_id')
#     if user_id is None:
#         return jsonify({'error': 'User not logged in'}), 401

     

#     conn = sqlite3.connect(db)
#     conn.row_factory = dict_factory
#     cur = conn.cursor()

#     if request.method == "POST":
#         data = request.get_json()
#         id = data['id']
#         name = data['name']
#         genre = data['genre']
#         played = data['played']
#         user_id = data.get('user_id')  # Retrieve user_id from request data
#         if user_id is None:
#             return jsonify({'error': 'User ID is required for adding a game'}), 400

#         # user_id = request.args.get('user_id')

#         # Insert new game into the database
#         cur.execute("INSERT INTO games (id, name, genre, played, user_id) VALUES (?, ?, ?, ?, ?)",
#                     (id, name, genre, played, user_id))
#         conn.commit()

#         return jsonify({'message': 'Game inserted successfully'}), 201


#     # Fetch all games associated with the logged-in user
#     all_games = cur.execute("SELECT * FROM games WHERE user_id=?", user_id,).fetchall()
        
#     conn.close()

#     return jsonify(all_games)

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

# @app.route('/register', methods=['POST'])
# def register():
#     data = request.json
#     name = data.get('name')
#     email = data.get('email')
#     password = data.get('password')

#     if not name or not email or not password:
#         return jsonify({'error': 'Please provide name, email, and password'}), 400

#     conn = sqlite3.connect(db)
#     c = conn.cursor()
#     c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
#     conn.commit()
#     conn.close()

#     return jsonify({'message': 'Registration successful'}), 201

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.json
#     email = data.get('email')
#     password = data.get('password')

#     if not email or not password:
#         return jsonify({'error': 'Please provide email and password'}), 400

#     conn = sqlite3.connect(db)
#     c = conn.cursor()
#     c.execute("SELECT * FROM users WHERE email=?", (email,))
#     user = c.fetchone()
#     conn.close()

#     if user is None:
#         return jsonify({'error': 'User not found'}), 404

#     # Check if the provided password matches the stored password
#     if password == user[3]:  # password is stored in the fourth column
#         return jsonify({'message': 'Login successful'}), 200
#     else:
#         return jsonify({'error': 'Invalid credentials'}), 401
    
# @app.route('/api/data')
# def view_data():
#     conn = sqlite3.connect(db)  # Replace 'your_database.db' with the path to your SQLite database file
#     conn.row_factory = sqlite3.Row
#     cur = conn.cursor()
#     cur.execute('SELECT * FROM games')  # Replace 'your_table' with the name of your table
#     rows = cur.fetchall()
#     conn.close()

#     # Convert data to a list of dictionaries for JSON serialization
#     data = [dict(row) for row in rows]

#     return jsonify(data)

# run the app
if __name__ == "__main__":
  app.run(debug=True, use_reloader=False)
