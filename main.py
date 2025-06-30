import telebot
import requests
import os
from dotenv import load_dotenv

# 🔐 Load bot token from Railway Environment Variable
load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

# 🎬 Download Reel using SnapInsta API
def fetch_download_url(insta_url):
    api_url = 'https://api.snapinsta.app/api/reel'
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0'
    }
    payload = {'url': insta_url}
    try:
        res = requests.post(api_url, json=payload, headers=headers)
        print("SnapInsta Call:", insta_url)
        print("Status:", res.status_code)
        if res.status_code == 200:
            data = res.json()
            if 'media' in data and isinstance(data['media'], list):
                return data['media'][0]
    except Exception as e:
        print("Error:", e)
    return None

# 🤖 /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
        "👋 Welcome to *Instagram Reels Downloader Bot!*\n\n"
        "📥 Send any public Instagram Reel link.\n"
        "🚀 Instant download link with no watermark.\n\n"
        "🔥 Join [@movie_downloader_channel](https://t.me/movie_downloader_channel)",
        parse_mode="Markdown")

# 📩 Handle any message
@bot.message_handler(func=lambda m: True)
def handle_message(msg):
    text = msg.text.strip()
    print("Received:", text)

    if "instagram.com" in text and "/reel/" in text:
        bot.send_chat_action(msg.chat.id, 'typing')
        video_url = fetch_download_url(text)
        if video_url:
            bot.send_message(msg.chat.id, "🎬 *Your Download Link:*", parse_mode="Markdown")
            bot.send_message(msg.chat.id, video_url)
            bot.send_message(msg.chat.id,
                "🚀 For HD Reels, Click 👉 [YouTube.com](https://youtube.com)",
                parse_mode="Markdown", disable_web_page_preview=True)
        else:
            bot.send_message(msg.chat.id, "⚠️ Couldn't fetch video. Make sure it's a *public* reel.", parse_mode="Markdown")
    else:
        bot.send_message(msg.chat.id, "❌ Please send a valid Instagram *reel* link.", parse_mode="Markdown")

# 🔄 Keep polling
bot.infinity_polling()
