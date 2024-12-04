import telebot
import sqlite3

# Initialize the bot with your token
TOKEN = '7667533446:AAEW0BafwTz6HHuhTBUrjdISoqFmkk9Bi4s'  # Replace this with your bot's token
bot = telebot.TeleBot(TOKEN)

# Create SQLite database to store user info and coin balance
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

# Handler for the /start command
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username

    # Check if the user already exists in the database
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if not user:
        # If user doesn't exist, add them to the database
        cursor.execute('INSERT INTO users (user_id, username) VALUES (?, ?)', (user_id, username))
        conn.commit()
        bot.reply_to(message, f"Welcome to BOLDX Coin Mining App {username}! You're now registered, we will be listing on January 20th!.")
    else:
        bot.reply_to(message, f"Welcome back, {username}! Your current coin balance is {user[2]}.")

# Handler for the /coin_balance command
@bot.message_handler(commands=['coin_balance'])
def coin_balance(message):
    user_id = message.from_user.id

    cursor.execute('SELECT coin_balance FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        bot.reply_to(message, f"Your current coin balance is {user[0]}.")
    else:
        bot.reply_to(message, "You are not registered. Use /start to register.")

# Handler for adding coins (for testing purposes)
@bot.message_handler(commands=['add_coins'])
def add_coins(message):
    user_id = message.from_user.id
    cursor.execute('SELECT coin_balance FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        new_balance = user[0] + 10  # Add 10 coins for example
        cursor.execute('UPDATE users SET coin_balance = ? WHERE user_id = ?', (new_balance, user_id))
        conn.commit()
        bot.reply_to(message, f"10 coins have been added! Your new balance is {new_balance}.")
    else:
        bot.reply_to(message, "You are not registered. Use /start to register.")

# Start polling
bot.polling(none_stop=True)
