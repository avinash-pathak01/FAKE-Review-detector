import streamlit as st
from utils import clean_text
import joblib
import os

# ✅ Absolute path fix
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE_DIR, 'model.pkl'))
vectorizer = joblib.load(os.path.join(BASE_DIR, 'vectorizer.pkl'))

# Page config
st.set_page_config(
    page_title="FakeGuard AI",
    page_icon="🛡️",
    layout="wide"
)

# ✅ Impressive Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=Inter:wght@300;400;500&display=swap');

    * { font-family: 'Inter', sans-serif; }

    .stApp {
        background: linear-gradient(135deg, #0f0c29, #1a1a2e, #16213e);
        min-height: 100vh;
    }

    .hero-badge {
        display: inline-block;
        background: rgba(99,202,183,0.15);
        border: 1px solid rgba(99,202,183,0.4);
        color: #63cab7;
        padding: 6px 18px;
        border-radius: 50px;
        font-size: 13px;
        font-weight: 500;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 16px;
    }

    .hero-title {
        font-family: 'Syne', sans-serif;
        font-size: 58px;
        font-weight: 800;
        background: linear-gradient(90deg, #ffffff 0%, #63cab7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
        margin: 0 0 12px 0;
    }

    .hero-sub {
        color: rgba(255,255,255,0.5);
        font-size: 17px;
        font-weight: 300;
        margin-bottom: 40px;
    }

    .card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 28px;
        backdrop-filter: blur(10px);
    }

    .result-fake {
        background: linear-gradient(135deg, rgba(255,75,75,0.15), rgba(255,75,75,0.05));
        border: 1px solid rgba(255,75,75,0.4);
        border-radius: 16px;
        padding: 24px 32px;
        text-align: center;
    }

    .result-genuine {
        background: linear-gradient(135deg, rgba(99,202,183,0.15), rgba(99,202,183,0.05));
        border: 1px solid rgba(99,202,183,0.4);
        border-radius: 16px;
        padding: 24px 32px;
        text-align: center;
    }

    .result-label {
        font-family: 'Syne', sans-serif;
        font-size: 36px;
        font-weight: 800;
        margin: 0;
    }

    .result-fake .result-label { color: #ff4b4b; }
    .result-genuine .result-label { color: #63cab7; }

    .result-desc {
        color: rgba(255,255,255,0.5);
        font-size: 14px;
        margin-top: 6px;
    }

    .metric-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 18px 20px;
        text-align: center;
    }

    .metric-value {
        font-family: 'Syne', sans-serif;
        font-size: 28px;
        font-weight: 700;
        color: #63cab7;
    }

    .metric-label {
        color: rgba(255,255,255,0.4);
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 4px;
    }

    .tip-item {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        padding: 10px 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        color: rgba(255,255,255,0.65);
        font-size: 14px;
    }

    .tip-icon { color: #63cab7; font-size: 16px; }

    .stTextArea > label {
        color: rgba(255,255,255,0.7) !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        letter-spacing: 0.5px !important;
    }

    .stTextArea textarea {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 12px !important;
        color: white !important;
        font-size: 15px !important;
        line-height: 1.6 !important;
    }

    .stTextArea textarea:focus {
        border-color: rgba(99,202,183,0.5) !important;
        box-shadow: 0 0 0 2px rgba(99,202,183,0.1) !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #63cab7, #3a9e8d) !important;
        color: #0f0c29 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 40px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        font-family: 'Syne', sans-serif !important;
        letter-spacing: 0.5px !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(99,202,183,0.35) !important;
    }

    .stProgress > div > div {
        background: linear-gradient(90deg, #63cab7, #3a9e8d) !important;
        border-radius: 10px !important;
    }

    .stProgress > div {
        background: rgba(255,255,255,0.08) !important;
        border-radius: 10px !important;
        height: 10px !important;
    }

    section[data-testid="stSidebar"] {
        background: rgba(15,12,41,0.95) !important;
        border-right: 1px solid rgba(255,255,255,0.06) !important;
    }

    .sidebar-stat {
        background: rgba(99,202,183,0.08);
        border: 1px solid rgba(99,202,183,0.2);
        border-radius: 10px;
        padding: 14px 16px;
        margin-bottom: 10px;
    }

    .sidebar-stat-label {
        color: rgba(255,255,255,0.4);
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .sidebar-stat-value {
        color: #63cab7;
        font-family: 'Syne', sans-serif;
        font-size: 20px;
        font-weight: 700;
        margin-top: 2px;
    }

    .footer {
        text-align: center;
        color: rgba(255,255,255,0.2);
        font-size: 13px;
        padding: 40px 0 20px;
    }

    hr { border-color: rgba(255,255,255,0.06) !important; }

    h3 { color: white !important; }
    </style>
""", unsafe_allow_html=True)


# ── Sidebar ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div style='padding: 10px 0 24px'>
            <div style='font-family:Syne,sans-serif;font-size:22px;font-weight:800;color:white'>
                🛡️ FakeGuard
            </div>
            <div style='color:rgba(255,255,255,0.35);font-size:13px;margin-top:4px'>
                AI-Powered Review Analysis
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class='sidebar-stat'>
            <div class='sidebar-stat-label'>Model</div>
            <div class='sidebar-stat-value'>Logistic Regression</div>
        </div>
        <div class='sidebar-stat'>
            <div class='sidebar-stat-label'>Vectorizer</div>
            <div class='sidebar-stat-value'>TF-IDF</div>
        </div>
        <div class='sidebar-stat'>
            <div class='sidebar-stat-label'>Built by</div>
            <div class='sidebar-stat-value'>Avinash 🚀</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
        <div style='color:rgba(255,255,255,0.35);font-size:12px;line-height:1.8'>
            This tool uses Natural Language Processing 
            and Machine Learning to classify product 
            reviews as fake or genuine in real-time.
        </div>
    """, unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────
st.markdown("""
    <div style='padding: 40px 0 32px'>
        <div class='hero-badge'>🛡️ AI Powered Detection</div>
        <div class='hero-title'>Fake Review<br>Detector</div>
        <div class='hero-sub'>Instantly detect whether a product review is genuine or AI-generated / fake using NLP + ML</div>
    </div>
""", unsafe_allow_html=True)


# ── Main Layout ───────────────────────────────────────────
col_left, col_right = st.columns([3, 2], gap="large")

with col_left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    review = st.text_area(
        "PASTE YOUR REVIEW BELOW",
        placeholder="e.g. This product is absolutely amazing!!! Best purchase ever!!!",
        height=220
    )
    st.markdown("<div style='margin-top:16px'>", unsafe_allow_html=True)
    analyze = st.button("🔍 Analyze Review")
    st.markdown("</div></div>", unsafe_allow_html=True)

with col_right:
    st.markdown("""
        <div class='card'>
            <div style='color:rgba(255,255,255,0.7);font-size:13px;font-weight:600;
                        letter-spacing:1.5px;text-transform:uppercase;margin-bottom:16px'>
                🔎 Fake Review Signals
            </div>
            <div class='tip-item'><span class='tip-icon'>⚡</span> Excessive exclamation marks & ALL CAPS</div>
            <div class='tip-item'><span class='tip-icon'>🔁</span> Repetitive or generic praise language</div>
            <div class='tip-item'><span class='tip-icon'>😅</span> Overly positive with no specific details</div>
            <div class='tip-item'><span class='tip-icon'>📦</span> No mention of actual product features</div>
            <div class='tip-item' style='border:none'><span class='tip-icon'>🤖</span> Unnatural, robotic sentence structure</div>
        </div>
    """, unsafe_allow_html=True)


# ── Analysis Result ───────────────────────────────────────
if analyze:
    if review.strip() == "":
        st.warning("⚠️ Please enter a review to analyze.")
    else:
        clean = clean_text(review)
        vec = vectorizer.transform([clean])
        prediction = model.predict(vec)[0]
        prob = model.predict_proba(vec)[0]
        confidence = max(prob) * 100

        st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        # Result + Confidence
        r1, r2 = st.columns([1, 1], gap="large")

        with r1:
            if prediction == 1:
                st.markdown("""
                    <div class='result-fake'>
                        <div class='result-label'>❌ FAKE</div>
                        <div class='result-desc'>This review appears to be inauthentic</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class='result-genuine'>
                        <div class='result-label'>✅ GENUINE</div>
                        <div class='result-desc'>This review appears to be authentic</div>
                    </div>
                """, unsafe_allow_html=True)

        with r2:
            st.markdown(f"""
                <div class='card' style='text-align:center'>
                    <div style='color:rgba(255,255,255,0.4);font-size:12px;
                                text-transform:uppercase;letter-spacing:1px'>
                        Model Confidence
                    </div>
                    <div style='font-family:Syne,sans-serif;font-size:48px;
                                font-weight:800;color:#63cab7;margin:8px 0 4px'>
                        {confidence:.1f}%
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.progress(int(confidence))

        # Metrics
        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
        st.markdown("""
            <div style='color:rgba(255,255,255,0.5);font-size:12px;
                        text-transform:uppercase;letter-spacing:2px;margin-bottom:14px'>
                📊 Review Insights
            </div>
        """, unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns(4)
        metrics = [
            (m1, len(review), "Characters"),
            (m2, len(review.split()), "Word Count"),
            (m3, review.count('!'), "Exclamations"),
            (m4, sum(1 for c in review if c.isupper()), "Uppercase"),
        ]
        for col, val, label in metrics:
            with col:
                st.markdown(f"""
                    <div class='metric-card'>
                        <div class='metric-value'>{val}</div>
                        <div class='metric-label'>{label}</div>
                    </div>
                """, unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────
st.markdown("""
    <div class='footer'>
        Made with ❤️ by Avinash &nbsp;·&nbsp; Powered by Streamlit &nbsp;·&nbsp; NLP + ML
    </div>
""", unsafe_allow_html=True)
