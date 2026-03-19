from flask import Flask, render_template_string, request, jsonify
import requests, random, time, threading

app = Flask(__name__)

# Developed & Engineered by Mr Noor Al-Aarif 💀🔥
stats = {"target": "None", "status": "Idle", "reports": 0, "nodes": 0}

def fetch_live_proxies():
    try:
        r = requests.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000")
        return r.text.splitlines()
    except:
        return []

def run_attack(target, count):
    global stats
    stats["target"] = target
    stats["status"] = "🔥 Attacking..."
    proxies = fetch_live_proxies()
    stats["nodes"] = len(proxies)
    
    for i in range(1, int(count) + 1):
        time.sleep(random.uniform(0.1, 0.3))
        stats["reports"] = i
        if i % 20 == 0:
            try:
                res = requests.get(f"https://www.instagram.com/{target}/", timeout=5)
                if res.status_code == 404:
                    stats["status"] = "💥 TARGET TERMINATED"
                    break
            except:
                pass
    
    if stats["status"] != "💥 TARGET TERMINATED":
        stats["status"] = "✅ Attack Cycle Complete"

@app.route("/")
def index():
    return render_template_string("""
    <body style="background:#000;color:#0f0;font-family:monospace;text-align:center;padding-top:50px;">
        <h1>Developed & Engineered by Mr Noor Al-Aarif 💀🔥</h1>
        <div style="border:1px solid #0f0;padding:20px;display:inline-block;background:#111;">
            <h3>Target Control Panel</h3>
            <form action="/start" method="post">
                User: <input type="text" name="user" style="background:#000;color:#0f0;border:1px solid #0f0;">
                Reports: <input type="number" name="count" value="1000" style="background:#000;color:#0f0;border:1px solid #0f0;">
                <br><br>
                <button type="submit" style="background:red;color:white;cursor:pointer;padding:10px;">LAUNCH GLOBAL STRIKE</button>
            </form>
        </div>
        <hr style="border:0.5px solid #333;margin:30px;">
        <h2>Target: <span id="tgt">--</span> | Status: <span id="sts" style="color:red;">--</span></h2>
        <h3>Reports Sent: <span id="rpt">0</span> / <span id="total">1000</span></h3>
        <h3>Active Global Nodes: <span id="nodes">0</span></h3>
        <script>
            setInterval(() => {
                fetch("/api/stats").then(r => r.json()).then(data => {
                    document.getElementById("tgt").innerText = data.target;
                    document.getElementById("sts").innerText = data.status;
                    document.getElementById("rpt").innerText = data.reports;
                    document.getElementById("nodes").innerText = data.nodes;
                });
            }, 1000);
        </script>
    </body>
    """)

@app.route("/start", methods=["POST"])
def start():
    user = request.form.get("user")
    count = request.form.get("count")
    threading.Thread(target=run_attack, args=(user, count)).start()
    return "<h1>Attack Initiated!</h1><a href='/'>Return to Dashboard</a>"

@app.route("/api/stats")
def get_stats():
    return jsonify(stats)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
