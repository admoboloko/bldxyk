import telebot
import sqlite3

# Initialize the bot with your token
TOKEN = '7667533446:AAEW0BafwTz6HHuhTBUrjdISoqFmkk9Bi4s'  # Replace this with your bot's token
bot = telebot.TeleBot(TOKEN)

# Create SQLite database connection
conn = sqlite3.connect('bot_database.db', check_same_thread=False)
cursor = conn.cursor()

# Create a table for users if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    coin_balance INTEGER DEFAULT 0
)
''')
conn.commit()

# Handle /start command
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username

    # Check if the user is already in the database
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if not user:
        # Add user to database if not already there
        cursor.execute('INSERT INTO users (user_id, username) VALUES (?, ?)', (user_id, username))
        conn.commit()
        bot.reply_to(message, f"Welcome to the app, {username}! You've been registered.")
    else:
        bot.reply_to(message, f"Welcome back, {username}! Your coin balance is {user[2]}.")

# Start the bot
bot.polling(none_stop=True)
