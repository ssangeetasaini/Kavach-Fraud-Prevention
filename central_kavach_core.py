import sqlite3
import re
import time
from datetime import datetime

def init_central_db():
    conn = sqlite3.connect('kavach_central.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS intercept_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        victim_phone TEXT,
                        message_content TEXT,
                        detected_link TEXT,
                        threat_level TEXT,
                        action_taken TEXT,
                        timestamp TEXT)''')
    conn.commit()
    conn.close()

# 📞 AUTOMATED VOICE CALL-BACK SIMULATOR
def trigger_voice_call_alert(victim_phone, incident_type):
    print("\n------------------------------------------------------------")
    print(f"📞 [AUTOMATED CYBER CELL DIALER]: Dialing target {victim_phone}...")
    time.sleep(1.5)
    print("📲 [HANDSET STATUS]: Call Connected! Target picked up the phone.")
    time.sleep(1)
    
    # Text-to-Speech Script Simulation for illiterate/elderly users
    print("\n🤖 [ROBOTIC VOICE ALERT (hi-IN)]:")
    if incident_type == "SMS_PHISHING":
        print(' > "नमस्कार, जयपुर साइबर सेल से कवच सुरक्षा बोल रहा हूँ। \n'
              ' > अभी आपके फोन पर बिजली बिल या लॉटरी का जो नकली मैसेज आया है, \n'
              ' > वह पूरी तरह फ्रॉड है। कृपया उस लिंक को न छुएं और काट दें।"')
    print("\n📴 [HANDSET STATUS]: Call Disconnected. User safely alerted without typing!")
    print("------------------------------------------------------------\n")

def analyze_incoming_stream(phone_number, message_text):
    print(f"\n📡 [TELECOM CARRIER INTERCEPT]: Scanning active feed for {phone_number}...")
    time.sleep(1)
    
    urls = re.findall(r'(https?://[^\s]+)', message_text)
    
    if not urls:
        return {"status": "ALLOWED", "reason": "No threat vectors identified."}
        
    for url in urls:
        if len(url) > 50 or "kyc" in url.lower() or "bank" in url.lower() or "gift" in url.lower():
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Central logs save karna
            conn = sqlite3.connect('kavach_central.db')
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO intercept_logs 
                              (victim_phone, message_content, detected_link, threat_level, action_taken, timestamp) 
                              VALUES (?, ?, ?, 'CRITICAL', 'VOICE_CALL_ALERT_DISPATCHED', ?)''', 
                           (phone_number, message_text, url, timestamp))
            conn.commit()
            conn.close()
            
            # 🚀 Triggering Zero-Touch Voice Protection
            trigger_voice_call_alert(phone_number, "SMS_PHISHING")
            
            return {"status": "BLOCKED", "reason": "Phishing Link Intercepted. Auto-Call Fired."}
            
    return {"status": "ALLOWED", "reason": "Safe message link."}

if __name__ == "__main__":
    init_central_db()
    print("🧠 KAVACH Central Core (v2.0 - Voice Alert Integrated): ACTIVE")
    print("---------------------------------------------------------------------")
    
    # Simulation: Ek aisi dadi/buzurg jinhe smartphone bilkul chalana nahi aata
    target_user = "+91 94145XXXXX (Elderly Citizen)"
    fraud_sms = "Dear customer aapka SBI Account BLOCK ho gaya hai, KYC update karein: http://sbi-verification-login-secure.net"
    
    analyze_incoming_stream(target_user, fraud_sms)