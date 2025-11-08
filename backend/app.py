from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import mysql.connector

app = Flask(__name__)
CORS(app)

# Database connection
def get_db():
    return mysql.connector.connect(
        host='db',
        user='user',
        password='password',
        database='tictactoe'
    )

@app.route('/')
def home():
    return jsonify({'message': 'Tic Tac Toe backend is running'})

@app.route('/games', methods=['POST'])
def create_game():
    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO games (board, current_player, status) VALUES ('---------', 'X', 'waiting')")
    db.commit()
    game_id = cur.lastrowid
    cur.close()
    db.close()
    return jsonify({'game_id': game_id, 'status': 'waiting'})

@app.route('/games/<int:game_id>', methods=['GET'])
def get_game(game_id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM games WHERE id=%s", (game_id,))
    game = cur.fetchone()
    cur.close()
    db.close()
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    return jsonify(game)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
