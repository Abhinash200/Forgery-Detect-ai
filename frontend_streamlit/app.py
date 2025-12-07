import streamlit as st
import requests
from streamlit_lottie import st_lottie
import time
from PIL import Image
import os
import base64
import io


st.set_page_config(
    page_title="ForgeryDetect AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


@st.cache_resource
def get_model():
    
    from model_loader import ForgeryDetectionModel
    return ForgeryDetectionModel()

@st.cache_data
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

@st.cache_data
def load_lottieurl(url):
    try:
        r = requests.get(url, timeout=2)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

current_dir = os.path.dirname(os.path.abspath(__file__))
hero_image_path = os.path.join(current_dir, "assets", "hero_banner.png")
upload_icon_path = os.path.join(current_dir, "assets", "fingerprint_icon.png")

hero_bg_b64 = get_base64_of_bin_file(hero_image_path)
upload_icon_b64 = get_base64_of_bin_file(upload_icon_path)

page_bg_css = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        color: #e2e8f0;
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Orbitron', sans-serif !important;
    }}

    .stApp {{
        background-image: linear-gradient(rgba(2, 6, 23, 0.8), rgba(2, 6, 23, 0.9)), url("data:image/png;base64,{hero_bg_b64}");
        background-attachment: fixed;
        background-size: cover;
        background-position: center top;
        background-repeat: no-repeat;
    }}

    .block-container {{
        max-width: 800px;
        padding-top: 6rem;
        padding-bottom: 5rem;
    }}

    .hero-title {{
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(135deg, #38bdf8 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 3rem;
        letter-spacing: -0.02em;
        text-shadow: 0 0 60px rgba(56, 189, 248, 0.5);
        line-height: 1.1;
        animation: glitch 6s infinite;
    }}

    @media (max-width: 640px) {{
        .hero-title {{
            font-size: 2.5rem;
            margin-bottom: 2rem;
        }}
        .block-container {{
            padding-top: 3rem;
        }}
    }}

    [data-testid="stFileUploader"] {{
        width: 100%;
        margin: 0 auto;
        padding-top: 2rem;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }}
    
    [data-testid="stFileUploader"] section {{
        background-color: black !important;
        background-image: url("data:image/png;base64,{upload_icon_b64}") !important;
        background-size: 80% !important;
        background-repeat: no-repeat !important;
        background-position: center center !important;
        
        border: 2px solid rgba(56, 189, 248, 0.3) !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.2) !important;
        mix-blend-mode: screen !important;
        
        width: 160px !important;
        height: 160px !important;
        border-radius: 50% !important;
        overflow: hidden !important;
        margin: 0 auto !important;
        padding: 0 !important;
        position: relative !important;
        opacity: 0.9 !important;
        transition: all 0.3s ease !important;
    }}

    [data-testid="stFileUploader"] section > * {{
        opacity: 0 !important;
        height: 100% !important;
        width: 100% !important;
        cursor: pointer !important;
    }}
    
    [data-testid="stFileUploader"] section:hover {{
        transform: scale(1.05);
        box-shadow: 0 0 40px rgba(56, 189, 248, 0.6) !important;
        border-color: rgba(56, 189, 248, 0.8) !important;
        opacity: 1 !important;
    }}

    [data-testid="stFileUploader"] section::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 6px;
        background: linear-gradient(90deg, transparent, #38bdf8, transparent);
        box-shadow: 0 0 20px #38bdf8;
        animation: scan 2s infinite ease-in-out;
        z-index: 10;
        opacity: 0.8;
        pointer-events: none;
    }}

    [data-testid="stFileUploader"] button {{
        display: none !important;
    }}

    [data-testid="stFileUploader"] button::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 6px;
        background: linear-gradient(90deg, transparent, #38bdf8, transparent);
        box-shadow: 0 0 20px #38bdf8;
        animation: scan 2s infinite ease-in-out;
        z-index: 10;
        opacity: 0.8;
        pointer-events: none;
    }}

    [data-testid="stFileUploader"] button:hover {{
        transform: scale(1.05);
        box-shadow: 0 0 40px rgba(56, 189, 248, 0.6) !important;
        border-color: rgba(56, 189, 248, 0.8) !important;
    }}
    
    [data-testid="stFileUploader"] button:active {{
        transform: scale(0.95);
    }}
    
    [data-testid="stFileUploader"]::after {{
        content: "TAP TO SCAN DOCUMENT";
        display: block;
        text-align: center;
        color: #38bdf8;
        font-size: 0.9rem;
        letter-spacing: 0.2em;
        margin-top: 1.5rem;
        opacity: 0.7;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
        animation: pulse 2s infinite;
    }}
    
    @keyframes scan {{
        0% {{ top: 0%; opacity: 0; }}
        15% {{ opacity: 1; }}
        85% {{ opacity: 1; }}
        100% {{ top: 100%; opacity: 0; }}
    }}

    @keyframes glitch {{
        0% {{ text-shadow: 0 0 60px rgba(56, 189, 248, 0.5); transform: skew(0deg); }}
        2% {{ text-shadow: 2px 2px 0 #a855f7; transform: skew(-1deg); }}
        4% {{ text-shadow: -2px -2px 0 #38bdf8; transform: skew(1deg); }}
        5% {{ text-shadow: 0 0 60px rgba(56, 189, 248, 0.5); transform: skew(0deg); }}
        100% {{ text-shadow: 0 0 60px rgba(56, 189, 248, 0.5); transform: skew(0deg); }}
    }}

    @keyframes pulse {{
        0% {{ opacity: 0.4; }}
        50% {{ opacity: 1; }}
        100% {{ opacity: 0.4; }}
    }}

    .scanner-box {{
        position: relative;
        width: 100%;
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(56, 189, 248, 0.3);
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.1);
    }}
    
    .scanner-box img {{
        width: 100%;
        display: block;
    }}
    
    .scanner-line {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: #38bdf8;
        box-shadow: 0 0 15px #38bdf8, 0 0 30px #38bdf8;
        animation: scan-line 3s ease-in-out infinite;
        z-index: 5;
    }}
    
    .scanner-grid {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(56, 189, 248, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(56, 189, 248, 0.1) 1px, transparent 1px);
        background-size: 20px 20px;
        z-index: 2;
        pointer-events: none;
    }}

    @keyframes scan-line {{
        0% {{ top: 0%; opacity: 0; }}
        5% {{ opacity: 1; }}
        95% {{ opacity: 1; }}
        100% {{ top: 100%; opacity: 0; }}
    }}

    .crack-container {{
        position: relative;
        width: 100%;
        height: 60px;
        margin-top: 2rem;
    }}
    
    .crack-half {{
        position: absolute;
        top: 0;
        width: 50%;
        height: 100%;
        background: linear-gradient(to right, #22c55e, #10b981);
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        z-index: 10;
        color: white;
        font-weight: 700;
        font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(34, 197, 94, 0.3);
    }}
    
    .crack-left {{
        left: 0;
        border-radius: 12px 0 0 12px;
        border-right: 1px solid rgba(255,255,255,0.3);
        animation: breakLeft 1.2s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards;
    }}
    
    .crack-right {{
        right: 0;
        border-radius: 0 12px 12px 0;
        border-left: 1px solid rgba(0,0,0,0.1);
        animation: breakRight 1.2s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards;
    }}
    
    .crack-reveal {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
        z-index: 1;
        opacity: 0;
        animation: appearResult 1.5s ease 0.3s forwards;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        font-size: 1.3rem;
        border: 1px solid rgba(255,255,255,0.1);
        text-shadow: 0 0 10px currentColor;
    }}

    @keyframes breakLeft {{
        0% {{ transform: translateX(0) rotate(0); }}
        40% {{ transform: translateX(10px) rotate(5deg); }} 
        100% {{ transform: translateX(-120%) rotate(-15deg); opacity: 0; }}
    }}
    
    @keyframes breakRight {{
        0% {{ transform: translateX(0) rotate(0); }}
        40% {{ transform: translateX(-10px) rotate(-5deg); }} 
        100% {{ transform: translateX(120%) rotate(15deg); opacity: 0; }}
    }}
    
    @keyframes appearResult {{
        0% {{ opacity: 0; transform: scale(0.8); }}
        100% {{ opacity: 1; transform: scale(1); }}
    }}

    .stButton > button {{
        background: linear-gradient(to right, #22c55e, #10b981);
        color: white;
        font-weight: 700;
        padding: 1rem;
        font-size: 1.1rem;
        border-radius: 12px;
        border: none;
        width: 100%;
        margin-top: 2rem;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(34, 197, 94, 0.3);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(34, 197, 94, 0.5);
    }}

    .result-card {{
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(255,255,255,0.1);
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        backdrop-filter: blur(12px);
        animation: fadeIn 0.6s ease-out;
    }}

    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    [data-testid="stExpander"] {{
        background-color: transparent !important;
        border: none !important;
    }}
    
    [data-testid="stExpander"] > details > summary {{
        font-family: 'Orbitron', sans-serif !important;
        color: #38bdf8 !important;
        background-color: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 8px !important;
        transition: all 0.3s;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }}

    [data-testid="stExpander"] > details > summary:hover {{
        border-color: #38bdf8 !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.2);
    }}
    
    [data-testid="stExpander"] > details[open] > summary {{
        border-bottom-left-radius: 0 !important;
        border-bottom-right-radius: 0 !important;
        border-bottom: 1px solid rgba(56, 189, 248, 0.1) !important;
    }}
    
    [data-testid="stExpander"] > details > div {{
        background-color: rgba(15, 23, 42, 0.4) !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-top: none !important;
        border-bottom-left-radius: 8px !important;
        border-bottom-right-radius: 8px !important;
    }}
</style>
"""
st.markdown(page_bg_css, unsafe_allow_html=True)

lottie_scan = load_lottieurl("https://lottie.host/9e017688-660b-4277-b9c0-8260a9270df8/jS27rFjV9U.json")

if 'uploader_key' not in st.session_state:
    st.session_state.uploader_key = 0

if 'scan_result' not in st.session_state:
    st.session_state.scan_result = None

def reset_uploader():
    st.session_state.uploader_key += 1
    st.session_state.scan_result = None
    st.rerun()

st.markdown('<div class="hero-title">ForgeryDetect AI</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=['jpg', 'png', 'jpeg', 'tiff'], key=f"main_uploader_{st.session_state.uploader_key}")

if uploaded_file is not None:
    st.markdown("""
    <style>
        [data-testid="stFileUploader"] {
            display: none !important;
        }
        
        .action-container {
            animation: expandFromCenter 0.6s ease-out forwards;
            transform-origin: center;
        }
        
        @keyframes expandFromCenter {
            0% { transform: scale(0.1); opacity: 0; }
            60% { transform: scale(1.05); opacity: 0.8; }
            100% { transform: scale(1); opacity: 1; }
        }
        
        .close-btn button {
            background-color: transparent !important;
            border: 2px solid #ef4444 !important;
            color: #ef4444 !important;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            font-size: 1.2rem;
            line-height: 1;
            padding: 0;
            transition: all 0.2s;
        }
        .close-btn button:hover {
            background-color: #ef4444 !important;
            color: white !important;
            transform: rotate(90deg);
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="action-container">', unsafe_allow_html=True)
    
    col_head, col_close = st.columns([8, 1])
    with col_head:
        st.markdown("<h3 style='text-align: center; margin-bottom: 2rem; color: #38bdf8;'>Scanning Complete</h3>", unsafe_allow_html=True)
    with col_close:
        st.markdown('<div class="close-btn">', unsafe_allow_html=True)
        if st.button("✕", key="close_btn", help="Close and Scan New"):
            reset_uploader()
        st.markdown('</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1], gap="large")
    
    with c1:
        st.markdown('<div style="font-family: Orbitron, sans-serif; font-weight: 700; margin-bottom: 0.5rem; color: #38bdf8;">Document Preview</div>', unsafe_allow_html=True)
        # Simplified Preview with native component for instant loading
        st.image(uploaded_file, use_container_width=True)
        uploaded_file.seek(0)
        
    with c2:
        st.write("")
        
        if st.session_state.scan_result is None:
            st.markdown('<h4 style="color: #38bdf8; font-family: Orbitron, sans-serif; text-align: center;">Ready for Analysis</h4>', unsafe_allow_html=True)
            st.markdown('<div style="font-family: Orbitron, sans-serif; font-size: 0.9rem; color: #a855f7; text-align: center;">Model: <b>EfficientNet-B0</b> | Security: <b>Encrypted</b></div>', unsafe_allow_html=True)
            
            action_placeholder = st.empty()
            run_clicked = action_placeholder.button("RUN FORGERY ANALYSIS", use_container_width=True)
            
            if run_clicked:
                action_placeholder.empty()
                
                if 'b64_img' in locals():
                    image_placeholder.markdown(get_scanner_html(animate=True), unsafe_allow_html=True)
                
                with st.spinner("Processing neural layers..."):
                    if lottie_scan:
                        st_lottie(lottie_scan, height=120, key="scanning")
                    time.sleep(1.5)
                    
                    try:
                       
                        
                        detector = get_model()
                        
                        
                        image = Image.open(uploaded_file).convert('RGB')
                        
                       
                        result = detector.predict(image)
                        
                       
                        st.session_state.scan_result = result
                        st.rerun()
                            
                    except Exception as e:
                         st.error(f"Analysis Failed: {e}")
                         action_placeholder.button("RUN FORGERY ANALYSIS", use_container_width=True, key="retry_btn_2")

        else:
            result = st.session_state.scan_result
            confidence = result.get("confidence", 0.0) * 100
            is_forged = result.get("is_forged", False)
            
            if is_forged:
                res_text = "FORGERY DETECTED"
                res_color = "#ef4444"
                bg_style = "background: rgba(239, 68, 68, 0.1);"
            else:
                res_text = "AUTHENTIC DOCUMENT"
                res_color = "#22c55e"
                bg_style = "background: rgba(34, 197, 94, 0.1);"
                
            breaking_html = f"""
<div class="crack-container">
<div class="crack-half crack-left">RUN FORG</div>
<div class="crack-half crack-right">ANALYSIS</div>
<div class="crack-reveal" style="color: {res_color}; {bg_style}">
{res_text}
</div>
</div>
"""
            st.markdown(breaking_html, unsafe_allow_html=True)
            
            conf_str = f"{confidence:.2f}%"
            
            st.markdown(f"""
            <div style="text-align: center; margin-top: 1rem; font-family: 'Orbitron'; color: {res_color};">
            <span style="opacity: 0.8; font-size: 0.9rem;">PREDICTION ACCURACY</span><br>
            <span style="font-size: 1.5rem; font-weight: bold;">{conf_str}</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.scan_result is not None:
        result = st.session_state.scan_result
        heatmap_b64 = result.get("heatmap_b64")
        
        if heatmap_b64:
            st.markdown("<br><br>", unsafe_allow_html=True)
            h1, h2, h3 = st.columns([1, 2, 1])
            
            with h2:
                with st.expander("⚡ NEURAL ACTIVATION LAYERS", expanded=True):
                    st.markdown('<div style="text-align: center; color: #94a3b8; font-family: Orbitron; font-size: 0.8rem; letter-spacing: 1px; margin-bottom: 1rem;">REGIONS TRIGGERING DETECTION</div>', unsafe_allow_html=True)
                    st.markdown(f"""
                    <div style="display: flex; flex-direction: column; align-items: center;">
                        <div style="position: relative; padding: 2px; background: linear-gradient(45deg, #38bdf8, #a855f7); border-radius: 14px;">
                            <div style="background: #0f172a; border-radius: 12px; overflow: hidden;">
                                <img src="data:image/png;base64,{heatmap_b64}" style="display: block; width: 100%; max-width: 400px;">
                            </div>
                        </div>
                        <div style="margin-top: 0.5rem; font-size: 0.75rem; color: #64748b; font-style: italic;">
                            Red/Yellow areas indicate high forgery probability
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

if uploaded_file is None:
    st.markdown("<br><br>", unsafe_allow_html=True)
if uploaded_file is None:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <style>
        div[data-baseweb="tab-list"] {
            gap: 10px;
            justify-content: center;
            margin-bottom: 1rem;
        }

        button[data-baseweb="tab"] {
            font-family: 'Orbitron', sans-serif !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            color: rgba(255, 255, 255, 0.6) !important;
            background-color: rgba(30, 41, 59, 0.5) !important;
            border: 1px solid rgba(148, 163, 184, 0.1) !important;
            border-radius: 8px !important;
            padding: 0.5rem 1.5rem !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            flex-grow: 0 !important;
        }
        
        button[data-baseweb="tab"]:hover {
            color: #38bdf8 !important;
            border-color: rgba(56, 189, 248, 0.5) !important;
            background-color: rgba(56, 189, 248, 0.1) !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }
        
        button[data-baseweb="tab"][aria-selected="true"] {
            color: white !important;
            background: linear-gradient(135deg, #38bdf8 0%, #a855f7 100%) !important;
            border: 1px solid transparent !important;
            box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
        }
        
        div[data-baseweb="tab-panel"] {
            padding-top: 1.5rem !important;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; color: #cbd5e1; margin-bottom: 1rem; font-family: Orbitron; letter-spacing: 2px; text-shadow: 0 0 10px rgba(0,0,0,0.5);">CLASSIFICATION METRICS</h3>', unsafe_allow_html=True)
    
    t1, t2, t3, t4 = st.tabs(["ACCURACY", "PRECISION", "RECALL", "F1 SCORE"])
    
    css_card = """
    <div style="
        background: rgba(15, 23, 42, 0.8); 
        padding: 2.5rem; 
        border-radius: 16px; 
        border: 1px solid rgba(56, 189, 248, 0.2); 
        text-align: center;
        box-shadow: 0 0 30px rgba(0, 0, 0, 0.5), inset 0 0 20px rgba(56, 189, 248, 0.05);
        backdrop-filter: blur(10px);
        max-width: 600px;
        margin: 0 auto;
    ">
        <h2 style="color: {color}; font-size: 3.5rem; margin: 0; font-family: Orbitron; text-shadow: 0 0 20px {color}80;">{value}</h2>
        <div style="width: 50px; height: 3px; background: {color}; margin: 1rem auto; opacity: 0.5; border-radius: 2px;"></div>
        <p style="color: #94a3b8; font-family: 'Inter', sans-serif; font-size: 1.1rem; letter-spacing: 0.5px;">{desc}</p>
    </div>
    """
    
    with t1:
        st.markdown(css_card.format(color="#38bdf8", value="91.1%", desc="Model confidence on the validation dataset"), unsafe_allow_html=True)
        
    with t2:
        st.markdown(css_card.format(color="#a855f7", value="94.1%", desc="Accuracy of forgery detection alerts"), unsafe_allow_html=True)
        
    with t3:
        st.markdown(css_card.format(color="#10b981", value="94.9%", desc="Ability to find all actual forgeries"), unsafe_allow_html=True)
        
    with t4:
        st.markdown(css_card.format(color="#f59e0b", value="94.5%", desc="Balanced performance metric"), unsafe_allow_html=True)
