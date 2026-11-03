import telebot
import requests
from bs4 import BeautifulSoup

TOKEN = "9054688908:AAFFMvMRvIqMPiBR4QNfA4xSnuKTs390CNE"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Main Pinterest Image Downloader Bot hoon. Mujhe koi bhi Pinterest ka link bhejo, main image nikal kar dunga!")

@bot.message_handler(func=lambda message: message.text and ("pinterest.com" in message.text or "pin.it" in message.text))
def download_pinterest(message):
    url = message.text.strip()
    sent_msg = bot.reply_to(message, "🔍 Pinterest link process ho raha hai...")
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        session = requests.Session()
        response = session.get(url, headers=headers, allow_redirects=True, timeout=10)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tag = soup.find('meta', property='og:image')
        
        if img_tag and img_tag.get('content'):
            img_url = img_tag['content']
            bot.send_photo(message.chat.id, img_url, caption="✅ Yeh lijiye aapki Pinterest image!")
            bot.delete_message(message.chat.id, sent_msg.message_id)
        else:
            bot.edit_message_text("❌ Image nahi mil payi. Kripya doosra link try karein.", message.chat.id, sent_msg.message_id)
            
    except Exception as e:
        bot.edit_message_text(f"❌ Error aa gaya: {str(e)}", message.chat.id, sent_msg.message_id)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Kripya sirf valid Pinterest link bhejiye.")

if __name__ == '__main__':
    print("Bot is starting...")
    bot.infinity_polling()
