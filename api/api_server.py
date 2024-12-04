from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

@app.route('/get_user', methods=['GET'])
def get_user():
    user_id = request.args.get('user_id')  # Pass user ID as a query parameter
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({
            'user_id': user[0],
            'username': user[1],
            'coin_balance': user[2]
        })
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
