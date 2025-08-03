from flask import Flask, request, render_template
import telegram
import asyncio
import requests
from datetime import datetime, timezone

app = Flask(__name__)

# Telegram Bot Info
BOT_TOKEN = '8329766691:AAG1XLV63gdBEvhSesyfvJWlBaIbrHm27qg'
CHAT_ID = '7991797378'
bot = telegram.Bot(token=BOT_TOKEN)

last_login = {}

def get_location(ip):
    try:
        res = requests.get(f'https://ipapi.co/{ip}/json/')
        data = res.json()
        city = data.get("city", "")
        country = data.get("country_name", "")
        return f"{city}, {country}" if city and country else country or ip
    except:
        return ip

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # ✅ CHECK: Only allow if admin / 1234
    if username != "admin" or password != "1234":
        return {'status': '❌ Invalid credentials'}

    ip = data.get('ip') or 'Unknown IP'
    device = data.get('device') or 'Unknown Device'
    latitude = data.get('latitude') or '0'
    longitude = data.get('longitude') or '0'
    accuracy_raw = data.get('accuracy')

    # 🛡 Safe conversion to int
    try:
        acc_val = int(accuracy_raw)
    except (TypeError, ValueError):
        acc_val = 0

    now = datetime.now(timezone.utc).strftime("%d/%m/%Y at %H:%M:%S UTC")
    location = get_location(ip)
    maps_link = f"https://maps.google.com/?q={latitude},{longitude}"

    prev = last_login.get(username)
    if not prev or prev['ip'] != ip or prev['device'] != device:
        message = f"""
*New login.*

Dear *{username}*, we detected a login into your account from a new device on {now}.

Device: `{device}`  
IP Location: `{location}`  
GPS Coordinates: `{latitude}, {longitude}` (±{acc_val}m)  
📍 [View on Google Maps]({maps_link})

If this wasn't you, you can terminate that session in *Settings > Devices* (or *Privacy & Security > Active Sessions*).

If you think that somebody logged in to your account against your will, you can enable *Two-Step Verification* in Privacy and Security settings.
"""
        asyncio.run(bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown'))
        last_login[username] = {'ip': ip, 'device': device}

    return {'status': '✅ Login recorded'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('cert.pem', 'key.pem'))
