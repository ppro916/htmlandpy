import os
import subprocess
import time
import requests
from threading import Thread

def run_flask():
    os.system("python app.py")

def run_ngrok():
    ngrok = subprocess.Popen(["./ngrok", "http", "5000"])
    time.sleep(3)
    try:
        res = requests.get("http://localhost:4040/api/tunnels")
        tunnel_url = res.json()["tunnels"][0]["public_url"]
        print(f"\n🔗 Public HTTPS URL: {tunnel_url}\n")
    except:
        print("❌ ngrok URL मिळवता आलं नाही")

if __name__ == "__main__":
    Thread(target=run_flask).start()
    time.sleep(1)
    run_ngrok()
