from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database Setup
def init_db():
    conn = sqlite3.connect('kavach.db')
    conn.execute('CREATE TABLE IF NOT EXISTS logs (time TEXT, info TEXT, status TEXT)')
    conn.commit()
    conn.close()
init_db()

# HTML Interface
HTML = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { background: #0b0e14; color: white; font-family: sans-serif; text-align: center; padding: 20px; }
        .box { padding: 20px; border: 2px solid #4facfe; background: #1a1a2e; max-width: 600px; margin: 10px auto; border-radius: 15px; }
        .alert { padding: 20px; margin: 20px auto; font-size: 20px; font-weight: bold; border-radius: 10px; }
        .red { color: #ff4d4d; border: 3px solid #ff4d4d; }
        .green { color: #28a745; border: 3px solid #28a745; }
        table { width: 90%; margin: 20px auto; border-collapse: collapse; background: #1a1a2e; }
        td, th { border: 1px solid #444; padding: 10px; }
    </style>
</head>
<body>
    <h1>PROJECT KAVACH: CYBER DEFENSE</h1>
    
    <div class="box">
        <h3>SMARTPHONE: LINK ANALYZER</h3>
        <form method="POST" action="/analyze_link">
            <input name="url" placeholder="Paste suspicious link..." style="width:80%; padding:10px;" required>
            <br><br><button type="submit">ANALYZE</button>
        </form>
    </div>

    <div class="box" style="border-color: #28a745;">
        <h3>KEYPAD: SMS FORWARD SIMULATOR (Forward to 5)</h3>
        <form method="POST" action="/simulate_sms">
            <input name="sms_content" placeholder="Paste SMS content..." style="width:80%; padding:10px;" required>
            <br><br><button type="submit" style="background:#28a745;">FORWARD TO 5</button>
        </form>
    </div>

    {% if alert_text %}
    <div class="alert {{ color_class }}">{{ alert_text | safe }}</div>
    <script>
        function speak(text, lang) {
            let msg = new SpeechSynthesisUtterance(text);
            msg.lang = lang;
            window.speechSynthesis.speak(msg);
        }
        speak("{{ eng_text }}", "en-US");
        speak("{{ hi_text }}", "hi-IN");
    </script>
    {% endif %}

    <h3>LIVE CYBER THREAT LOGS</h3>
    <table>
        <tr><th>TIME</th><th>DATA</th><th>STATUS</th></tr>
        {% for log in logs %}
        <tr><td>{{log[0]}}</td><td>{{log[1]}}</td><td>{{log[2]}}</td></tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route('/')
def index():
    conn = sqlite3.connect('kavach.db')
    logs = conn.execute("SELECT * FROM logs ORDER BY rowid DESC").fetchall()
    conn.close()
    return render_template_string(HTML, logs=logs)

@app.route('/analyze_link', methods=['POST'])
def analyze_link():
    url = request.form['url']
    status = "BLOCKED" if any(x in url.lower() for x in ["bank", "prize", "login", "paypal"]) else "CLEARED"
    
    conn = sqlite3.connect('kavach.db')
    conn.execute("INSERT INTO logs VALUES (?, ?, ?)", (datetime.now().strftime("%H:%M:%S"), "URL: "+url, status))
    conn.commit()
    logs = conn.execute("SELECT * FROM logs ORDER BY rowid DESC").fetchall()
    conn.close()
    
    alert_data = {
        "alert_text": "🚨 ALERT: THREAT DETECTED!" if status=="BLOCKED" else "✅ SAFE: CONTENT CLEAN",
        "color_class": "red" if status=="BLOCKED" else "green",
        "eng_text": "Critical threat detected" if status=="BLOCKED" else "Content is safe",
        "hi_text": "चेतावनी! यह एक खतरनाक लिंक है" if status=="BLOCKED" else "यह लिंक पूरी तरह सुरक्षित है"
    }
    return render_template_string(HTML, logs=logs, **alert_data)

@app.route('/simulate_sms', methods=['POST'])
def simulate_sms():
    content = request.form['sms_content']
    status = "BLOCKED" if any(x in content.lower() for x in ["bank", "prize", "login", "lottery"]) else "CLEARED"
    
    conn = sqlite3.connect('kavach.db')
    conn.execute("INSERT INTO logs VALUES (?, ?, ?)", (datetime.now().strftime("%H:%M:%S"), "SMS: "+content, status))
    conn.commit()
    logs = conn.execute("SELECT * FROM logs ORDER BY rowid DESC").fetchall()
    conn.close()
    
    alert_data = {
        "alert_text": "🚨 FRAUD DETECTED!" if status=="BLOCKED" else "✅ SAFE: NO ACTION",
        "color_class": "red" if status=="BLOCKED" else "green",
        "eng_text": "Fraud detected in SMS" if status=="BLOCKED" else "SMS is safe",
        "hi_text": "आपके मैसेज में धोखाधड़ी पाई गई है" if status=="BLOCKED" else "यह मैसेज सुरक्षित है"
    }
    return render_template_string(HTML, logs=logs, **alert_data)

if __name__ == '__main__':
    app.run(port=9000, debug=True)