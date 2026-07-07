import time
import os
import sqlite3
import re
from gtts import gTTS

# 🧠 ML ENGINE LOGIC
def predict_phishing_url(url):
    score = 0
    reasons = []
    if len(url) > 50: score += 2; reasons.append("URL ki lambai bohot zyada hai")
    if re.search(r'(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}', url): 
        score += 3; reasons.append("Numeric IP Address use kiya hai")
    if url.count('-') >= 2: score += 2; reasons.append("Fake bank domain pattern (-)")
    
    keywords = ['free', 'recharge', 'jio', 'login', 'verify', 'gift', 'win', 'kyc', 'update']
    found = [w for w in keywords if w in url.lower()]
    if found: score += len(found) * 1.5; reasons.append(f"Fraud triggers mile: {found}")
    
    return (score >= 3), ", ".join(reasons)

# 🧠 AUTOMATED ZERO-ACTION LISTENER
def simulate_incoming_whatsapp_message(sender, message_text):
    print(f"\n📨 [NEW MESSAGE FROM: {sender}]: {message_text}")
    print("⏳ KAVACH Background AI automatically scanning the message... (No User Action Required)")
    time.sleep(1.5) 
    
    urls = re.findall(r'(https?://[^\s]+)', message_text)
    
    if not urls:
        print("✅ No links found. Message is safe for the user.")
        return

    for url in urls:
        print(f"🔗 Detected Link inside message: {url}")
        is_malicious, reasons = predict_phishing_url(url)
        
        if is_malicious:
            print(f"🚨 [ALERT]: PHISHING DETECTED! Reason: {reasons}")
            
            # 1. Database Entry
            conn = sqlite3.connect('kavach.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO phishing_links (url, detected_by, ip_address, location) VALUES (?, 'Background Automation', '127.0.0.1', 'Jaipur Hub')", (url,))
            cursor.execute("INSERT INTO police_alerts (alert_type, description, source_info) VALUES ('CRITICAL - ZERO CLICK', ?, ?)", 
                           (f"Background Scanner blocked fraud text for inexperienced user. Analysis: {reasons}", sender))
            conn.commit()
            conn.close()
            print("🚨 Police Live Dashboard updated successfully.")

            # 2. Loud Hindi Voice Warning via Windows Default Media Player
            warning_text = "चेतावनी! आपके व्हाट्सएप पर एक फ्रॉड मैसेज आया है। कृपया इस मैसेज को न छुएं, यह धोखा है!"
            if not os.path.exists('static'):
                os.makedirs('static')
                
            audio_path = os.path.abspath("static/background_alert.mp3")
            tts = gTTS(text=warning_text, lang='hi', slow=False)
            tts.save(audio_path)
            
            print("🔊 [LOUD AUDIO]: Playing Hindi Threat Warning to user...")
            # 🚀 Windows ka system command use karke direct mp3 play karna bina kisi third-party module ke!
            os.system(f'start "" "{audio_path}"')
            
            print("\n🛑 SCREEN BLOCKER ENGAGED: [RED FULL-SCREEN OVERLAY DISPLAYED ON SMARTPHONE]")
        else:
            print("✅ Link patterns look normal according to current ML model.")

if __name__ == "__main__":
    print("=== PROJECT KAVACH: ZERO-ACTION BACKGROUND DEMO ===")
    
    # Test Case 1: Safe Message
    simulate_incoming_whatsapp_message("+91 98765XXXXX", "Hello, kal college ka timing kya h?")
    time.sleep(2)
    
    # Test Case 2: Fraud Message
    simulate_incoming_whatsapp_message("+91 82091XXXXX", "Apna Jio ka 399 ka recharge free me karein abhi click karein: http://192.168.43.10/jio-free-offer-secure")