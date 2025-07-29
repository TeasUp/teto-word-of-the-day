from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import logging
from flask import Flask, request
import os

logging.basicConfig(level=logging.INFO)

# Replace this with your actual bot token
BOT_TOKEN = '7285496835:AAGk-utGF4yZYLSQCBMuV5olti4Ybq99hR8'
MEDIA_PATH = 'ban_response.mp4'  # Video file path

# Flask app for webhook
app = Flask(__name__)

async def ban_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    # Only act in group/supergroup and when replying
    if not msg.chat.type.endswith('group') or not msg.reply_to_message:
        return

    # Only allow group admins to use this
    admins = await context.bot.get_chat_administrators(msg.chat.id)
    if msg.from_user.id not in [admin.user.id for admin in admins]:
        return

    # Trigger only if message is exactly "بن"
    if msg.text.strip() != "بن":
        return

    target_id = msg.reply_to_message.from_user.id

    try:
        await context.bot.ban_chat_member(msg.chat.id, target_id)

        # Send video with no caption
        with open(MEDIA_PATH, 'rb') as media:
            await msg.reply_video(InputFile(media))

    except Exception as e:
        await msg.reply_text(f"خطا در بن کردن: {e}")

# Initialize bot
bot_app = ApplicationBuilder().token(BOT_TOKEN).build()
bot_app.add_handler(MessageHandler(filters.TEXT & filters.REPLY, ban_handler))

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot_app.bot)
    bot_app.process_update(update)
    return 'OK'

@app.route('/')
def home():
    return 'Bot is running!'

if __name__ == "__main__":
    # Get port from environment variable
    port = int(os.environ.get('PORT', 8080))
    
    # Set webhook URL
    webhook_url = f"https://your-railway-domain.railway.app/webhook"
    
    # Set webhook
    bot_app.bot.set_webhook(url=webhook_url)
    
    # Run Flask app
    app.run(host='0.0.0.0', port=port) 