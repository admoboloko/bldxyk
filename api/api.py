from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/api/add_user', methods=['POST'])
def add_user():
    data = request.get_json()

    user_id = data.get('user_id')
    username = data.get('username')
    coin_balance = data.get('coin_balance', 0)

    if not user_id or not username:
        return jsonify({'error': 'Invalid data provided'}), 400

    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()

    # Check if the user already exists
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        return jsonify({'message': 'User already exists'}), 200

    # Insert the new user
    cursor.execute('INSERT INTO users (user_id, username, coin_balance) VALUES (?, ?, ?)',
                   (user_id, username, coin_balance))
    conn.commit()
    conn.close()

    return jsonify({'message': 'User added successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)
