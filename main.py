import telebot
import os
from dotenv import load_dotenv

# Load your Telegram bot token from environment
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# 👇 Backend bot and your admin chat ID
FORWARD_TO = "@SaveAsBot"
ADMIN_CHAT_ID = 8195087542

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message,
        "👋 *Welcome to Insta Reel Downloader!*\n\n"
        "📥 Send me any public Instagram reel link.\n"
        "🚀 I’ll fetch and send you the download link in seconds.\n\n"
        "🔥 Join [@movie_downloader_channel](https://t.me/movie_downloader_channel) for more tools!",
        parse_mode="Markdown")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    text = message.text.strip()
    print("Received:", text)

    if "instagram.com" in text and "/reel/" in text:
        bot.send_chat_action(message.chat.id, 'typing')
        
        try:
            forwarded = bot.forward_message(FORWARD_TO, message.chat.id, message.message_id)
            bot.send_message(message.chat.id, "⏳ Fetching your download link...")
            bot.send_message(ADMIN_CHAT_ID, f"📨 New reel request:\n{text}")
        except Exception as e:
            print("Forward Error:", e)
            bot.send_message(message.chat.id, "⚠️ Failed to forward. Try again later.")
    else:
        bot.send_message(message.chat.id, "❌ Please send a valid Instagram *reel* link.", parse_mode="Markdown")

# (Optional) Relay response from backend bot to admin
@bot.message_handler(content_types=['video', 'photo', 'text'])
def relay_response(message):
    if message.from_user.username == FORWARD_TO.replace("@", ""):
        try:
            # Send it back to the admin (you)
            if message.video:
                bot.send_video(ADMIN_CHAT_ID, message.video.file_id, caption=message.caption or "🎬")
            elif message.photo:
                bot.send_photo(ADMIN_CHAT_ID, message.photo[-1].file_id, caption=message.caption or "")
            elif message.text:
                bot.send_message(ADMIN_CHAT_ID, f"📩 Bot replied:\n\n{message.text}")
        except Exception as e:
            print("Relay Error:", e)
if __name__ == "__main__":
    print("Bot started...")
    bot.infinity_polling()
