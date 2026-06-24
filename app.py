import streamlit as st
import re

# --- 1. Smart URL Detection Logic ---
def analyze_url(url):
    url = url.lower().strip()
    
    # Unsafe Signs (Red Flags)
    suspicious_indicators = [
        "bit.ly", "tinyurl", "t.co", "short.url", "is.gd",
        "login", "verify", "update", "bank", "account", "secure", "signin",
        "free", "gift", "winner", "lucky", "offer", "prize", "kbc", "lottery",
        "@", "-", "0", "1", "2", ".xyz", ".top", ".click"
    ]
    
    # Rule 1: Check for IP Address
    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", url.replace("https://", "").replace("http://", "")):
        return "🚨 Unsafe: Direct IP access is highly suspicious!"

    # Rule 2: Check for missing HTTPS
    if not url.startswith("https"):
        return "⚠️ Caution: Site is not encrypted (No HTTPS). High risk of data theft."

    # Rule 3: Pattern Scoring
    score = 0
    detected_flags = []
    for flag in suspicious_indicators:
        if flag in url:
            score += 1
            detected_flags.append(flag)

    # Decision Making
    if score >= 2 or len(url) > 65:
        return f"🚨 Phishing Alert: Suspicious patterns detected ({', '.join(detected_flags[:2])})."
    elif any(domain in url for domain in ["google.com", "facebook.com", "amazon.in", "github.com", "aktu.ac.in"]):
        return "✅ Verified Safe: Official and trusted domain."
    else:
        if len(url) > 45:
             return "🚨 Warning: URL looks abnormally long or randomized."
        return "✅ Safe Website"

# --- 2. Smart SMS Detection Logic ---
def analyze_sms(msg):
    msg = msg.lower()
    
    # Deep Fraud Keywords for Indian Context
    fraud_keywords = [
        'lottery', 'winner', 'kbc', 'crore', 'prize', 'gift', 'lucky draw', # Prize scams
        'electricity bill', 'power cut', 'disconnection', 'electricity office', # Utility scams
        'account blocked', 'kyc update', 'pan card', 'otp', 're-verify', 'bank', # Bank frauds
        'job offer', 'work from home', 'salary', 'part time job', # Job scams
        'click here', 'bit.ly', 'tinyurl', 'wa.me', 't.me' # Suspicious links
    ]
    
    found_words = [word for word in fraud_keywords if word in msg]
    
    if found_words:
        return True, found_words
    return False, []

# --- 3. Streamlit UI Dashboard ---
def main():
    st.set_page_config(page_title="AI Cyber Shield", page_icon="🛡️", layout="centered")
    
    # Header Section
    st.title("🛡️ AI Cyber Crime Detection System")
    st.markdown("---")

    tab1, tab2 = st.tabs(["🌐 Website URL Scanner", "📩 SMS/Email Fraud Scanner"])

    # --- TAB 1: URL SCANNER ---
    with tab1:
        st.subheader("Detect Phishing & Fake Sites")
        url_input = st.text_input("Paste the URL below:", placeholder="Example: http://kbc-lottery-winner.xyz")
        
        if st.button("Start AI Scan"):
            if url_input:
                with st.spinner('Analyzing URL patterns...'):
                    result = analyze_url(url_input)
                    if "Safe" in result:
                        st.success(result)
                    else:
                        st.error(result)
                        st.info("**AI Advice:** Do not enter your passwords or bank details on this site.")
            else:
                st.warning("Please enter a link to scan.")

    # --- TAB 2: SMS SCANNER ---
    with tab2:
        st.subheader("Analyze Suspicious Messages")
        msg_input = st.text_area("Paste the SMS or Email content here:", height=150, 
                                 placeholder="Example: Your electricity bill is pending. Call 987XXXXXXX immediately.")
        
        if st.button("Check for Fraud"):
            if msg_input:
                is_fraud, patterns = analyze_sms(msg_input)
                
                if is_fraud:
                    st.error(f"⚠️ FRAUD DETECTED! Found triggers: {', '.join(patterns)}")
                    st.warning("""
                        **🚨 Safety Checklist for You:**
                        1. **DO NOT** click any links in this message.
                        2. **DO NOT** share any OTP or personal ID.
                        3. **BLOCK** the sender immediately.
                        4. This looks like a common scam tactic.
                    """)
                else:
                    st.success("✅ No obvious fraud patterns detected. But always stay cautious!")
            else:
                st.warning("Please paste a message first.")

    # Footer
    st.markdown("---")
    st.caption("Developed by Aadarsh Dubey | AI-Powered Cyber Safety Tool 2026")

if __name__ == '__main__':
    main()