import streamlit as st
from utils import clean_text
import joblib
import os
import requests
import re

# ✅ Absolute path fix
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model      = joblib.load(os.path.join(BASE_DIR, 'model.pkl'))
vectorizer = joblib.load(os.path.join(BASE_DIR, 'vectorizer.pkl'))

# ── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title="FakeGuard AI",
    page_icon="🛡️",
    layout="wide"
)

# ── CSS ───────────────────────────────────────────────────
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
    .result-desc { color: rgba(255,255,255,0.5); font-size: 14px; margin-top: 6px; }
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
    }
    .stTextArea textarea {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 12px !important;
        color: white !important;
        font-size: 15px !important;
    }
    .stTextInput > div > input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 12px !important;
        color: white !important;
        font-size: 15px !important;
        padding: 14px 16px !important;
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
        width: 100% !important;
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
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.04) !important;
        border-radius: 12px !important;
        gap: 4px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        color: rgba(255,255,255,0.5) !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(99,202,183,0.2) !important;
        color: #63cab7 !important;
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
    .review-item {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 10px;
    }
    .review-fake-tag {
        background: rgba(255,75,75,0.15);
        border: 1px solid rgba(255,75,75,0.3);
        color: #ff4b4b;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    .review-genuine-tag {
        background: rgba(99,202,183,0.15);
        border: 1px solid rgba(99,202,183,0.3);
        color: #63cab7;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    .summary-fake {
        background: linear-gradient(135deg, rgba(255,75,75,0.12), rgba(255,75,75,0.04));
        border: 1px solid rgba(255,75,75,0.3);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
    }
    .summary-genuine {
        background: linear-gradient(135deg, rgba(99,202,183,0.12), rgba(99,202,183,0.04));
        border: 1px solid rgba(99,202,183,0.3);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
    }
    .summary-num {
        font-family: 'Syne', sans-serif;
        font-size: 52px;
        font-weight: 800;
    }
    .summary-fake .summary-num { color: #ff4b4b; }
    .summary-genuine .summary-num { color: #63cab7; }
    .summary-label { color: rgba(255,255,255,0.5); font-size: 14px; margin-top: 4px; }
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


# ── Helper Functions ──────────────────────────────────────
def extract_asin(url):
    patterns = [
        r'/dp/([A-Z0-9]{10})',
        r'/gp/product/([A-Z0-9]{10})',
        r'/product/([A-Z0-9]{10})',
        r'asin=([A-Z0-9]{10})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def fetch_amazon_reviews(asin, api_key, page=1):
    url = "https://real-time-amazon-data.p.rapidapi.com/product-reviews"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "real-time-amazon-data.p.rapidapi.com"
    }
    params = {
        "asin": asin,
        "country": "US",
        "page": str(page),
        "star_rating": "ALL",
        "sort_by": "TOP_REVIEWS",
        "verified_purchases_only": "false"
    }
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        data = response.json()
        reviews = data.get("data", {}).get("reviews", [])
        product_title = data.get("data", {}).get("product_title", "Unknown Product")
        return reviews, product_title
    except Exception as e:
        return None, str(e)


def classify_review(text):
    clean = clean_text(text)
    vec = vectorizer.transform([clean])
    pred = model.predict(vec)[0]
    prob = model.predict_proba(vec)[0]
    confidence = max(prob) * 100
    return pred, confidence


# ── Sidebar ───────────────────────────────────────────────
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
        <div style='color:rgba(255,255,255,0.6);font-size:13px;font-weight:600;
                    letter-spacing:1px;text-transform:uppercase;margin-bottom:8px'>
            🔑 RapidAPI Key
        </div>
    """, unsafe_allow_html=True)
    api_key = st.text_input(
        "API Key",
        type="password",
        placeholder="Paste your RapidAPI key",
        label_visibility="collapsed"
    )
    st.markdown("""
        <div style='color:rgba(255,255,255,0.3);font-size:11px;margin-top:6px'>
            Get free key at rapidapi.com<br>
            Search: "Real-Time Amazon Data"
        </div>
    """, unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────
st.markdown("""
    <div style='padding: 40px 0 32px'>
        <div class='hero-badge'>🛡️ AI Powered Detection</div>
        <div class='hero-title'>Fake Review<br>Detector</div>
        <div class='hero-sub'>Detect fake reviews instantly — paste a single review or drop an Amazon product link</div>
    </div>
""", unsafe_allow_html=True)


# ── Tabs ──────────────────────────────────────────────────
tab1, tab2 = st.tabs(["✍️  Single Review", "🔗  Amazon Product Link"])


# ══════════════════════════════════════════════════════════
# TAB 1 — Single Review
# ══════════════════════════════════════════════════════════
with tab1:
    col_left, col_right = st.columns([3, 2], gap="large")

    with col_left:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        review = st.text_area(
            "PASTE YOUR REVIEW BELOW",
            placeholder="e.g. This product is absolutely amazing!!! Best purchase ever!!!",
            height=220
        )
        st.markdown("<div style='margin-top:16px'>", unsafe_allow_html=True)
        analyze = st.button("🔍 Analyze Review", key="single")
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

    if analyze:
        if review.strip() == "":
            st.warning("⚠️ Please enter a review to analyze.")
        else:
            pred, confidence = classify_review(review)
            st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
            st.markdown("<hr>", unsafe_allow_html=True)

            r1, r2 = st.columns([1, 1], gap="large")
            with r1:
                if pred == 1:
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

            st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
            m1, m2, m3, m4 = st.columns(4)
            for col, val, label in [
                (m1, len(review), "Characters"),
                (m2, len(review.split()), "Words"),
                (m3, review.count('!'), "Exclamations"),
                (m4, sum(1 for c in review if c.isupper()), "Uppercase"),
            ]:
                with col:
                    st.markdown(f"""
                        <div class='metric-card'>
                            <div class='metric-value'>{val}</div>
                            <div class='metric-label'>{label}</div>
                        </div>
                    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# TAB 2 — Amazon Product Link
# ══════════════════════════════════════════════════════════
with tab2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    amazon_url = st.text_input(
        "PASTE AMAZON PRODUCT URL",
        placeholder="https://www.amazon.com/dp/B08N5WRWNW",
    )
    col_btn1, col_btn2 = st.columns([2, 1])
    with col_btn1:
        fetch_btn = st.button("🚀 Fetch & Analyze Reviews", key="amazon")
    with col_btn2:
        pages = st.selectbox("Pages to fetch", [1, 2, 3], index=0)
    st.markdown("</div>", unsafe_allow_html=True)

    if fetch_btn:
        if not api_key:
            st.error("⚠️ Please enter your RapidAPI key in the sidebar first.")
        elif not amazon_url.strip():
            st.warning("⚠️ Please enter an Amazon product URL.")
        else:
            asin = extract_asin(amazon_url)
            if not asin:
                st.error("❌ Could not extract ASIN from URL. Make sure it's a valid Amazon product link.")
            else:
                st.markdown(f"""
                    <div style='color:rgba(255,255,255,0.4);font-size:13px;margin:12px 0'>
                        📦 ASIN detected: <span style='color:#63cab7;font-weight:600'>{asin}</span>
                    </div>
                """, unsafe_allow_html=True)

                all_reviews = []
                product_title = ""

                with st.spinner("🔍 Fetching reviews from Amazon..."):
                    for page in range(1, pages + 1):
                        reviews, title = fetch_amazon_reviews(asin, api_key, page)
                        if reviews is None:
                            st.error(f"❌ API Error: {title}")
                            break
                        if page == 1:
                            product_title = title
                        all_reviews.extend(reviews)

                if all_reviews:
                    st.markdown(f"""
                        <div style='margin: 20px 0 8px;color:rgba(255,255,255,0.8);
                                    font-family:Syne,sans-serif;font-size:18px;font-weight:700'>
                            🛍️ {product_title}
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown("<hr>", unsafe_allow_html=True)

                    results = []
                    with st.spinner("🤖 Analyzing reviews with AI..."):
                        for r in all_reviews:
                            text = r.get("review_comment", "") or r.get("review_title", "")
                            if text.strip():
                                pred, conf = classify_review(text)
                                results.append({
                                    "text": text,
                                    "prediction": pred,
                                    "confidence": conf,
                                    "rating": r.get("review_star_rating", "N/A"),
                                    "author": r.get("review_author", "Anonymous"),
                                })

                    total       = len(results)
                    fake        = sum(1 for r in results if r["prediction"] == 1)
                    genuine     = total - fake
                    fake_pct    = (fake / total * 100) if total else 0
                    genuine_pct = (genuine / total * 100) if total else 0

                    # Summary cards
                    st.markdown("""
                        <div style='color:rgba(255,255,255,0.5);font-size:12px;
                                    text-transform:uppercase;letter-spacing:2px;margin:24px 0 14px'>
                            📊 Analysis Summary
                        </div>
                    """, unsafe_allow_html=True)

                    s1, s2, s3 = st.columns(3)
                    with s1:
                        st.markdown(f"""
                            <div class='metric-card'>
                                <div class='metric-value'>{total}</div>
                                <div class='metric-label'>Total Reviews</div>
                            </div>
                        """, unsafe_allow_html=True)
                    with s2:
                        st.markdown(f"""
                            <div class='summary-genuine'>
                                <div class='summary-num'>{genuine}</div>
                                <div class='summary-label'>✅ Genuine ({genuine_pct:.1f}%)</div>
                            </div>
                        """, unsafe_allow_html=True)
                    with s3:
                        st.markdown(f"""
                            <div class='summary-fake'>
                                <div class='summary-num'>{fake}</div>
                                <div class='summary-label'>❌ Fake ({fake_pct:.1f}%)</div>
                            </div>
                        """, unsafe_allow_html=True)

                    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='color:rgba(255,255,255,0.4);font-size:12px;margin-bottom:4px'>✅ Genuine — {genuine_pct:.1f}%</div>", unsafe_allow_html=True)
                    st.progress(int(genuine_pct))
                    st.markdown(f"<div style='color:rgba(255,255,255,0.4);font-size:12px;margin:10px 0 4px'>❌ Fake — {fake_pct:.1f}%</div>", unsafe_allow_html=True)
                    st.progress(int(fake_pct))

                    # Side-by-side review lists
                    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
                    col_g, col_f = st.columns(2, gap="large")

                    with col_g:
                        st.markdown(f"""
                            <div style='color:#63cab7;font-family:Syne,sans-serif;
                                        font-size:16px;font-weight:700;margin-bottom:14px'>
                                ✅ Genuine Reviews ({genuine})
                            </div>
                        """, unsafe_allow_html=True)
                        for r in [x for x in results if x["prediction"] == 0]:
                            st.markdown(f"""
                                <div class='review-item'>
                                    <div style='display:flex;justify-content:space-between;
                                                align-items:center;margin-bottom:8px'>
                                        <span class='review-genuine-tag'>✅ Genuine</span>
                                        <span style='color:rgba(255,255,255,0.3);font-size:12px'>
                                            ⭐ {r['rating']} · {r['author']}
                                        </span>
                                    </div>
                                    <div style='color:rgba(255,255,255,0.7);font-size:14px;line-height:1.6'>
                                        {r['text'][:200]}{'...' if len(r['text']) > 200 else ''}
                                    </div>
                                    <div style='color:rgba(255,255,255,0.25);font-size:12px;margin-top:8px'>
                                        Confidence: {r['confidence']:.1f}%
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)

                    with col_f:
                        st.markdown(f"""
                            <div style='color:#ff4b4b;font-family:Syne,sans-serif;
                                        font-size:16px;font-weight:700;margin-bottom:14px'>
                                ❌ Fake Reviews ({fake})
                            </div>
                        """, unsafe_allow_html=True)
                        for r in [x for x in results if x["prediction"] == 1]:
                            st.markdown(f"""
                                <div class='review-item'>
                                    <div style='display:flex;justify-content:space-between;
                                                align-items:center;margin-bottom:8px'>
                                        <span class='review-fake-tag'>❌ Fake</span>
                                        <span style='color:rgba(255,255,255,0.3);font-size:12px'>
                                            ⭐ {r['rating']} · {r['author']}
                                        </span>
                                    </div>
                                    <div style='color:rgba(255,255,255,0.7);font-size:14px;line-height:1.6'>
                                        {r['text'][:200]}{'...' if len(r['text']) > 200 else ''}
                                    </div>
                                    <div style='color:rgba(255,255,255,0.25);font-size:12px;margin-top:8px'>
                                        Confidence: {r['confidence']:.1f}%
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                else:
                    st.warning("⚠️ No reviews found. Try a different URL or increase pages.")


# ── Footer ────────────────────────────────────────────────
st.markdown("""
    <div class='footer'>
        Made with ❤️ by Avinash &nbsp;·&nbsp; Powered by Streamlit &nbsp;·&nbsp; NLP + ML
    </div>
""", unsafe_allow_html=True)
