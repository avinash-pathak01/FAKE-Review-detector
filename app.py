from utils import predict_review, clean_text
import joblib

# Load model + vectorizer
model = joblib.load('model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Page config
st.set_page_config(
    page_title="AI Fake Review Detector",
    page_icon="🧠",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .stTextArea textarea {
        font-size: 16px;
    }
    .title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: #4A90E2;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<p class="title">🧠 AI Fake Review Detector</p>', unsafe_allow_html=True)
st.write("### Detect whether a review is **Fake ❌** or **Genuine ✅**")

# Sidebar
st.sidebar.title("⚙️ Options")
st.sidebar.write("This tool uses NLP + ML to classify reviews.")
st.sidebar.write("Built by Avinash 🚀")

# Layout
col1, col2 = st.columns([2, 1])

with col1:
    review = st.text_area("✍️ Enter Review Text", height=200)

with col2:
    st.info("💡 Tips:\n- Fake reviews are often repetitive\n- Too many '!!!'\n- Overly positive tone")

# Button
if st.button("🔍 Analyze Review"):
    if review.strip() == "":
        st.warning("⚠️ Please enter a review")
    else:
        clean = clean_text(review)
        vec = vectorizer.transform([clean])

        prediction = model.predict(vec)[0]
        prob = model.predict_proba(vec)[0]

        confidence = max(prob) * 100

        st.markdown("---")

        # Result Display
        if prediction == 1:
            st.error(f"❌ Fake Review Detected")
        else:
            st.success(f"✅ Genuine Review")

        # Confidence
        st.write(f"### Confidence: {confidence:.2f}%")
        st.progress(int(confidence))

        # Extra Insights
        st.markdown("### 📊 Review Insights")
        st.write(f"- Length: {len(review)} characters")
        st.write(f"- Exclamation Marks: {review.count('!')}")
        st.write(f"- Uppercase Letters: {sum(1 for c in review if c.isupper())}")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")
