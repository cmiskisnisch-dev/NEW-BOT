import telebot
import requests
import os
from flask import Flask
from threading import Thread

TOKEN = '8984084657:AAH9kAxahBwZbDWLR5rn8vU3XCTbF29ujmU'
bot = telebot.TeleBot(TOKEN)

# --- Servidor Web para manter o bot acordado ---
app = Flask(__name__)

@app.route('/')
def home():
    return "O bot está online e funcionando!"

def run_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
# -----------------------------------------------

@bot.message_handler(func=lambda message: message.text.startswith('http'))
def handle_link(message):
    url = message.text
    bot.reply_to(message, "Iniciando o download... aguarde.")
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        nome_arquivo = url.split("/")[-1].split("?")[0] or "arquivo_baixado"
        
        with open(nome_arquivo, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        with open(nome_arquivo, 'rb') as f:
            bot.send_document(message.chat.id, f)

        os.remove(nome_arquivo)
    except Exception as e:
        bot.reply_to(message, f"Erro: {e}")

# Inicia o servidor web em segundo plano
Thread(target=run_server).start()

# Inicia o bot
bot.polling()
