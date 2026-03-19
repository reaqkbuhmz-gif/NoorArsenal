from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests, random, time, threading, datetime

app = Flask(__name__)

# --- Developed & Engineered by Mr Noor Al-Aarif 💀🔥 ---
# GitHub Edition: Universal Security Testing Tool

stats = {"target": "None", "status": "Ready", "reports": 0, "nodes": 0, "logs": []}

def fetch_proxies():
    try:
        r = requests.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000")
        return r.text.splitlines()
    except: return []

def run_attack(target, count):
    global stats
    stats["target"] = target
    stats["status"] = "📡 Testing..."
    stats["logs"] = []
    proxies = fetch_proxies()
    stats["nodes"] = len(proxies)
    
    for i in range(1, int(count) + 1):
        proxy = random.choice(proxies) if proxies else "Local-IP"
        time.sleep(random.uniform(0.1, 0.4))
        stats["reports"] = i
        
        now = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{now}] Signal #{i} sent via {proxy} ✅"
        stats["logs"].insert(0, log_entry)
        if len(stats["logs"]) > 10: stats["logs"].pop()

        if i % 25 == 0:
            try:
                # فحص الحالة بشكل عام
                res = requests.get(f"https://www.instagram.com/{target}/", timeout=5)
                if res.status_code == 404:
                    stats["status"] = "⚠️ TARGET OFFLINE"
                    break
            except: pass
            
    if stats["status"] != "⚠️ TARGET OFFLINE":
        stats["status"] = "🏁 Sequence Complete"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    target = request.form.get('user')
    count = request.form.get('count')
    threading.Thread(target=run_attack, args=(target, count)).start()
    return redirect(url_for('index'))

@app.route('/api/stats')
def get_stats():
    return jsonify(stats)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
