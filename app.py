import logging
import os
import time
import threading
import mysql.connector
import schedule
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from config import SLACK_BOT_TOKEN, SLACK_APP_TOKEN, SLACK_SIGNING_SECRET

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Slack App
app = App(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)
client = WebClient(token=SLACK_BOT_TOKEN)

# Connect to MySQL
db = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", ""),
    database=os.getenv("DB_NAME", "slackbot")
)
cursor = db.cursor()

# Ensure preferences table exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS preferences (
    user_id VARCHAR(50) PRIMARY KEY,
    wants_tips BOOLEAN NOT NULL
)
""")
db.commit()

# Respond to @mentions
@app.event("app_mention")
def handle_mention(event, say):
    say("Hi there! 👋 I heard you mentioned me.")

# Respond to DM messages
@app.event("message")
def handle_message(event, say, client):
    channel = event.get("channel")
    user_id = event.get("user")
    text = event.get("text", "").strip().lower()

    if not user_id or event.get("subtype") == "bot_message":
        return

    try:
        # Confirm it's a DM
        channel_info = client.conversations_info(channel=channel)
        is_im = channel_info["channel"]["is_im"]
    except Exception as e:
        print(f"Error checking DM channel: {e}")
        return

    if is_im:
        print(f"DM received from {user_id}: {text}")
        if text == "yes":
            cursor.execute("REPLACE INTO preferences (user_id, wants_tips) VALUES (%s, %s)", (user_id, True))
            db.commit()
            say("✅ You are now subscribed to daily updates!")
        elif text == "no":
            cursor.execute("REPLACE INTO preferences (user_id, wants_tips) VALUES (%s, %s)", (user_id, False))
            db.commit()
            say("❌ You have opted out of daily updates.")
        else:
            say("📩 Would you like to receive daily updates? (yes/no)")

# Handle slash command
@app.command("/crawling_updates")
def handle_slash_command(ack, respond, command):
    ack()
    respond("Slash command received! You can also DM me with 'yes' or 'no' to subscribe or unsubscribe.")

# Scheduled update sender
def send_scheduled_updates():
    try:
        cursor.execute("SELECT user_id FROM preferences WHERE wants_tips = TRUE")
        users = cursor.fetchall()
        for (user_id,) in users:
            client.chat_postMessage(channel=user_id, text="🕘 This is your 9 PM daily update! Stay awesome! 🚀")
        logging.info("Scheduled updates sent.")
    except Exception as e:
        logging.error(f"Error sending scheduled messages: {e}")

# Background scheduler thread
def run_schedule():
    # Testing version: run every minute
    # schedule.every(1).minutes.do(send_scheduled_updates)
    
    # Production version: run at 9 PM daily
    schedule.every().day.at("21:00").do(send_scheduled_updates)
    while True:
        schedule.run_pending()
        time.sleep(60)

# Run the bot
if __name__ == "__main__":
    print("Bot is running...")
    threading.Thread(target=run_schedule).start()
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()



