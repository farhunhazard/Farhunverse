# app.py — FarhunVerse | Animated Streamlit Portfolio (Stable + Header Fix)
# Developed by Mohamed Farhun M

import streamlit as st
from pathlib import Path
import requests
from PyPDF2 import PdfReader
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
from dotenv import load_dotenv
import os
from PIL import Image, ImageDraw, ImageFont,ImageFilter
import base64
import json

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# -----------------------------------------------
# 🧠 LOTTIE HELPER (STABLE)
# -----------------------------------------------
@st.cache_data
def load_lottie_url(url: str):
    """Load a Lottie animation from a URL and return a dict (or None)."""
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return res.json()
        else:
            st.warning(f"⚠️ Could not load Lottie: {url}")
            return None
    except Exception as e:
        st.error(f"Lottie load error: {e}")
        return None

def load_lottie_file(file_path: str):
    """Load a Lottie animation from a local JSON file."""
    try:
        if not os.path.exists(file_path):
            st.warning(f"⚠️ Lottie file not found: {file_path}")
            return None
        import json
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"❌ Failed to load Lottie file {file_path}: {e}")
        return None

# 🧩 Utility — Convert all images in a folder to base64
def load_images_from_folder(folder_path):
    images = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            with open(os.path.join(folder_path, filename), "rb") as img_file:
                b64 = base64.b64encode(img_file.read()).decode()
                images.append(b64)
    return images

# 🎨 Create FV logo PNG dynamically (Glowing Gradient Version)
def create_fv_logo():
    size = (256, 256)
    img = Image.new("RGBA", size, (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    # Define gradient colors
    top_color = (0, 198, 255)
    bottom_color = (0, 114, 255)

    # Create gradient background
    for y in range(size[1]):
        ratio = y / size[1]
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        draw.line([(0, y), (size[0], y)], fill=(r, g, b))

    # 🧠 Add FV text (centered)
    try:
        font = ImageFont.truetype("arialbd.ttf", 160)
    except:
        font = ImageFont.load_default()

    text = "FV"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    text_pos = ((size[0] - text_w) / 2, (size[1] - text_h) / 2.5)
    draw.text(text_pos, text, font=font, fill=(255, 255, 255, 255))

    # ✨ Apply subtle glow
    glow = img.filter(ImageFilter.GaussianBlur(8))
    img = Image.alpha_composite(glow, img)

    # Save logo to a file
    logo_path = Path("favicon.png")
    img.save(logo_path)
    return str(logo_path)

# ✅ Generate logo and store its path BEFORE Streamlit loads
favicon_path = create_fv_logo()

# -----------------------------------------------
# 🌐 PAGE CONFIGURATION
# -----------------------------------------------
st.set_page_config(
    page_title="FarhunVerse | Mohamed Farhun M",
    layout="wide",
    page_icon=favicon_path,
)

# 🌍 GLOBAL FOOTER FIX (Keep Footer Always Below Chat)
# -----------------------------------------------
st.markdown("""
<style>
footer {visibility: hidden;}  /* Hide Streamlit default footer */
div.block-container {padding-bottom: 70px;}  /* Space so content never overlaps footer */

/* 🌐 Custom Footer Styling */
#custom-footer {
    position: fixed;
    left: 60%;
    bottom: 0;
    transform: translateX(-50%);
    width: 100%;
    max-width: 100%;
    background: rgba(0, 0, 0, 0.7);
    color: white;
    text-align: center;
    padding: 12px 0;
    font-size: 15px;
    z-index: 9999;
    border-top: 1px solid rgba(255, 255, 255, 0.2);
    transition: all 0.3s ease-in-out;
}

/* 🩶 Light Theme Adjustment */
@media (prefers-color-scheme: light) {
    #custom-footer {
        background: rgba(255, 255, 255, 0.95);
        color: #000;
        border-top: 1px solid rgba(0, 0, 0, 0.1);
    }
}

/* ✨ Hover Effect */
#custom-footer:hover {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: #fff;
    border-top: none;
}
</style>
""", unsafe_allow_html=True)

# ✅ Verified, working Lottie JSONs
lottie_ai = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_1pxqjqps.json")       # futuristic AI circuit
lottie_code = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_qp1q7mct.json")      # coding animation
lottie_connect = load_lottie_url("https://assets1.lottiefiles.com/packages/lf20_jcikwtux.json")   # connection animation

# -----------------------------------------------
# 📁 DATA
# -----------------------------------------------
PROJECTS = [
    {
        "title": "FusePay — Decentralized Payroll Platform",
        "description": "Decentralized payroll platform integrating OLAS AI agents and Rootstock RBTC for transparent and automated payroll processing. Won $500 in Build with Celo 5 hackathon and gained collaborative, cross-cultural skills.",
        "stack": "React, Solidity, Streamlit, OLAS AI Agents",
        "demo": "https://fuse-pay.vercel.app/",
        "github": "https://github.com/farhunhazard/fusepay",
        "video": "https://youtu.be/6yoArObr7c8?si=O7Q4JWl-yj2jid2L",
        "hackathon": "https://buildwithcelo-5.hackerearth.com/",
    },
    {
        "title": "NEARVision — Blockchain Analytics Dashboard",
        "description": "AI-powered analytics dashboard for the NEAR blockchain that visualizes smart contract and transaction metrics in real time using Streamlit.Won $1000 participating solo.",
        "stack": "Python, Streamlit, NEAR RPC, Plotly",
        "demo": "https://nearvisionai.streamlit.app/",
        "github": "https://github.com/MohamedFarhun/NearVisionAI_Dashboard",
        "video": "https://youtu.be/Jf9Y7rbuf0w?si=uChIQEkRaNVjidhY",
        "hackathon": "https://nearhacks.hackerearth.com/?utm_source=header&utm_medium=search&utm_campaign=he-search",
    },
    {
        "title": "Stock Market Analysis Using Machine Learning",
        "description": "Streamlit analytics app using ML models to predict and visualize stock market movements — built during the Daisi hackathon.Won $2000 combined both rounds.",
        "stack": "Python, Streamlit, Scikit-learn, Pandas",
        "demo": "https://stockmarketanalysisdaisi.streamlit.app/",
        "github": "https://github.com/MohamedFarhun/StockMarketAnalysis",
        "video": "https://youtu.be/Gf1MbNDPrt4?si=lysyID7czRk03udX",
        "hackathon": "https://devpost.com/software/stock-market-analysis-dqvte4",
    },
    {
        "title": "Cryptographic Farming — Blockchain AgriTech Solution",
        "description": "Blockchain-based agricultural insurance & cryptographic solution. Notable Winner — Miami Hack Week x Rootstock.Won $1900 in Miami Hack Week and $480 in Rootstock.",
        "stack": "Blockchain, Smart Contracts, Cryptography",
        "github": "https://github.com/ManishR10/cryptographic_farming",
        "video": "https://youtu.be/i0zlup1ExM8?si=EY_CkHL4Cx2HVbHO",
        "hackathon": "https://devpost.com/software/cryptographic-farming-mz89ae",
    },
    {
        "title": "EduRegion Explorer: Advanced Educational Data Analysis and Visualization Platform",
        "description": "Interactive Chatbot Leveraging OpenAI's GPT-3.5 model to generate informative responses. Capable of creating complex SQL queries from natural language inputs to interact with Snowflake databases. Provides data tables and insightful analytics in response to diverse user queries.Won top 10 finalist award with snowflake baggies.",
        "stack": "Machine Learning , Data Science, AI/ML",
        "demo": "https://eduregionexplorer.streamlit.app/",
        "github": "https://github.com/MohamedFarhun/snowflake_hackathon_-EduRegion-Explorer",
        "video": "https://youtu.be/6fkC8R6mYtc?si=XuTP-rvFNnzU3L5m",
    },
        {
        "title": "GuardianAI: AI-Powered Cybersecurity Threat Detection and Response System",
        "description": "GuardianAI is a rule-based chat prototype designed to ensure ethical and legal compliance when using generative AI tools in the workplace.Won ₹5000 as finalist award in hackathon.",
        "stack": "Machine Learning , Data Science, AI/ML, openai,natural language processing",
        "demo": "https://guardianai.streamlit.app/",
        "github": "https://github.com/MohamedFarhun/GuardianAI",
        "video": "https://youtu.be/emYRkPeakzI?si=wc-b7tD0YCWSjkPm",
    },
]

SKILLS = {
    "AI / ML": ["Python", "LangChain", "Streamlit", "Pandas"],
    "Blockchain": ["Solidity", "Web3.js", "Smart Contracts", "NEAR", "Celo"],
    "DevOps / Automation": ["Jenkins", "Docker", "Git", "CI/CD", "Bash"],
    "Cloud & Infra": ["AWS", "Azure", "Linux", "Monitoring", "ServiceNow (IRIS)"],
}

SOCIALS = {
    "GitHub": "https://github.com/MohamedFarhun",
    "LinkedIn": "https://www.linkedin.com/in/mohamedfarhun/",
    "Devpost": "https://devpost.com/mohamedfarhun-it20",
    "Email": "mailto:mohamed.farhunm@hcltech.com",
}

RESUME_PATH = "resume.pdf"

# -----------------------------------------------
# ⚙️ UTILITIES
# -----------------------------------------------
def get_pdf_text(pdf_path):
    if not Path(pdf_path).exists():
        return ""
    reader = PdfReader(pdf_path)
    return "".join(page.extract_text() or "" for page in reader.pages)

def search_resume(query, text):
    query = query.lower()
    results = [line for line in text.split("\n") if query in line.lower()]
    return "\n\n".join(results[:6]) if results else "No matches found."

def radar_chart(skills):
    categories = list(skills.keys())
    # Custom proficiency values
    values_map = {
        "AI / ML": 85,
        "Blockchain": 70,
        "Devops / Automation": 60,
        "Cloud & Infra": 65,
    }
    values = [values_map.get(cat, 50) for cat in categories]  # default 50 if not mapped
    fig = go.Figure(go.Scatterpolar(r=values, theta=categories, fill='toself'))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        template="plotly_dark",
    )
    return fig

# File to store live view count
COUNTER_FILE = Path("view_count.json")

# Initialize counter file if not exists
if not COUNTER_FILE.exists():
    with open(COUNTER_FILE, "w") as f:
        json.dump({"views": 0}, f)

# Increment live counter once per session
if "viewed" not in st.session_state:
    with open(COUNTER_FILE, "r+") as f:
        data = json.load(f)
        data["views"] += 1
        f.seek(0)
        json.dump(data, f, indent=4)
    st.session_state["viewed"] = True

# Retrieve latest view count
with open(COUNTER_FILE, "r") as f:
    data = json.load(f)
view_count = data["views"]

# -----------------------------------------------
# 🧭 SIDEBAR
# -----------------------------------------------
st.sidebar.title("🌌 FarhunVerse - Where Code Meets Creativity")
menu = st.sidebar.radio("Navigate", ["🏠Home", "👨🏻‍💻Tech Showcase", "📝 AI Resume Navigator", "👉 Beyond the Code", "📩 Contact"])
st.sidebar.markdown("---")

# -----------------------------------------------
# 🧭 SIDEBAR (Upgraded Interactive Layout)
# -----------------------------------------------
with st.sidebar:
    # --- FV Logo ---
    st.markdown("""
    <style>
    .fv-logo {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 120px;
        height: 120px;
        margin: 10px auto;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
        border: 2px solid rgba(0, 180, 216, 0.4);
        box-shadow: 0 4px 20px rgba(0, 180, 216, 0.35);
        transition: all 0.3s ease-in-out;
    }
    .fv-logo:hover {
        transform: scale(1.07);
        box-shadow: 0 6px 28px rgba(0, 180, 216, 0.6);
    }
    @keyframes glowText {
      0%, 100% { text-shadow: 0 0 10px #00b4d8, 0 0 20px #00c6ff; }
      50% { text-shadow: 0 0 25px #0072ff, 0 0 35px #00b4d8; }
    }
    .fv-text {
        font-family: 'Poppins', sans-serif;
        font-size: 42px;
        font-weight: 800;
        background: linear-gradient(135deg, #00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 2px;
        animation: glowText 3s ease-in-out infinite alternate;
    }
    </style>
    <div class="fv-logo">
        <span class="fv-text">FV</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f"<h4 style='text-align:center;'>👁️ Visitors: <span style='color:#00b4d8;'>{view_count}</span></h4>",
        unsafe_allow_html=True,
    )   

    st.markdown("---")

    # 🧠 About Section
    with st.expander("👨‍💻 About This Portfolio"):
        st.markdown("""
        Welcome to **FarhunVerse**, a digital reflection of who I am —  
        an **AI-driven Technologist** and **Linux Engineer** passionate about merging  
        **innovation, intelligence, and infrastructure.**

        💡 Built entirely using **Streamlit**, it showcases:
        - My hackathon-winning projects
        - AI Resume Chatbot (LangChain + OpenAI)
        - Skills & Technical Visualizations
        - Personal stories “Beyond the Code”
        """)

    # 🌟 Hackathon Highlight
    with st.expander("🏆 Hackathon Highlights"):
        st.markdown("""
        - 🥇 Winner — Build with Celo 5  
        - 🏆 Winner — Rootstock x Miami Hack Week  
        - 🎯 Finalist — Daisi AI Challenge  
        - 💰 Earned over **₹3,00,000+** in global hackathons
        """)

    # 📝 Feedback Section
    st.markdown("---")
    st.subheader("💬 Feedback & Rating")
    rating = st.slider("Rate this portfolio", 1, 5, 4)
    feedback_text = st.text_area("Share your feedback")

    if st.button("📨 Submit Feedback"):
        st.success(f"✅ Thanks for rating {rating}⭐, Farhun appreciates your input!")
        if feedback_text:
            st.write("💭 Your thoughts:", feedback_text)
        # 🧭 Quick Links Section
        st.markdown("### 🔗 Quick Access")
        st.markdown(f"""
        - [🌐 Devpost Portfolio]({SOCIALS['Devpost']})
        - [💼 LinkedIn Profile]({SOCIALS['LinkedIn']})
        - [💻 GitHub Repos]({SOCIALS['GitHub']})
        """)

    st.markdown("---")
    st.info("👨‍💻 Developed by **Mohamed Farhun M** | AI & Linux Engineer @ HCL | Hackathon Champion 🏆")

# --- Detect page change globally (before rendering each page) ---
if "last_page" not in st.session_state:
    st.session_state.last_page = menu

# 🧹 Clear chat automatically when leaving AI Resume Navigator
if st.session_state.last_page == "📝 AI Resume Navigator" and menu != "📝 AI Resume Navigator":
    if "current_chat" in st.session_state:
        st.session_state.current_chat = []

# Update last page tracker
st.session_state.last_page = menu

# Initialize video states
for i, _ in enumerate(PROJECTS):
    st.session_state.setdefault(f"play_video_{i}", False)

# -----------------------------------------------
# 🏠 HOME (Fixed header + Lottie)
# -----------------------------------------------
if menu == "🏠Home":
    st.markdown(
        """
        <style>
        /* 🎨 HERO SECTION STYLING */
        .hero-section {
            display: flex;
            align-items: center;
            justify-content: flex-start;
            flex-wrap: wrap;
            gap: 30px; /* tighter spacing between name and image */
            padding: 40px 0;
        }

        .hero-text {
            flex: 1 1 auto;
            min-width: 300px;
        }

        h1.hero {
            background: linear-gradient(90deg, #00c6ff, #0072ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: clamp(34px, 5vw, 52px);
            font-weight: 800;
            line-height: 1.2;
            margin-bottom: 12px;
        }

        .tagline {
            font-size: 18px;
            color: var(--text-color);
            opacity: 0.85;
            line-height: 1.6;
            margin-bottom: 20px;
        }

        .hero-image {
            flex: 0 0 260px; /* 💥 Larger image container */
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: -25px; /* visually aligns image closer to text */
        }

        .hero-image img {
            width: 260px; /* 💥 Larger circular photo */
            height: 260px;
            border-radius: 50%;
            object-fit: cover;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
            border: 4px solid rgba(0, 114, 255, 0.2); /* subtle glowing border */
            transition: transform 0.35s ease, box-shadow 0.35s ease;
        }

        .hero-image img:hover {
            transform: scale(1.08);
            box-shadow: 0 14px 30px rgba(0, 114, 255, 0.5);
        }

        /* 📱 Responsive Design */
        @media screen and (max-width: 900px) {
            .hero-section {
                flex-direction: column;
                text-align: center;
                gap: 15px;
            }
            .hero-text {
                flex: 1 1 100%;
            }
            .hero-image {
                margin-top: 10px;
            }
            .hero-image img {
                width: 180px;
                height: 180px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ✅ Load image safely as base64
    img_path = "photo.jpeg"
    try:
        with open(img_path, "rb") as f:
            img_data = f.read()
            img_base64 = base64.b64encode(img_data).decode()
            img_src = f"data:image/jpeg;base64,{img_base64}"
    except Exception as e:
        st.error(f"⚠️ Could not load image: {e}")
        img_src = ""

    # 🧠 Hero Section Layout
    st.markdown(
        f"""
        <div class="hero-section">
            <div class="hero-text">
                <h1 class="hero">👋 Hi, I'm Mohamed&nbsp;Farhun&nbsp;M</h1>
                <p class="tagline">
                    💻 AI-driven Technologist | Linux & Cloud Engineer @ HCL<br>
                    ⚙️ Specializing in DevOps, GenAI, and Automation Infrastructure.<br>
                    🚀 Passionate about building self-healing, intelligent systems.
                </p>
                <div>
                    <p style="margin-bottom: 10px;">🏆 Multi-time Hackathon Winner — Celo, NEAR, Rootstock, Daisi</p>
                    <a href="{SOCIALS['Devpost']}" target="_blank" style="color: #00b4d8; font-weight: 600; text-decoration: none;">🌐 View My Devpost Portfolio</a>
                </div>
            </div>
            <div class="hero-image">
                <img src="{img_src}" alt="Mohamed Farhun M">
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.subheader("✨ Highlights")
    cols = st.columns(3)
    with cols[0]:
        if lottie_code:
            st_lottie(lottie_code, height=140)
        st.markdown("**AI & Automation Enthusiast**<br>Integrating AI with Linux systems.", unsafe_allow_html=True)
    with cols[1]:
        if lottie_connect:
            st_lottie(lottie_connect, height=140)
        st.markdown("**Hackathon Builder**<br>Winning with creativity and execution.", unsafe_allow_html=True)
    with cols[2]:
        if lottie_ai:
            st_lottie(lottie_ai, height=140)
        st.markdown("**Continuous Learner**<br>Always exploring the next frontier.", unsafe_allow_html=True)

    # --- About Me Section ---
    st.markdown("---")
    st.markdown("## 👨‍💻 About Me")
    about_col1, about_col2 = st.columns([1.5, 1])
    with about_col1:
        st.write(
            """
            I'm **Mohamed Farhun M**, an AI-driven technologist passionate about designing intelligent,
            self-healing infrastructures that bridge **AI, DevOps, and Cloud Engineering**.  
            At HCLTech, I specialize in **Linux, GenAI, and Automation frameworks** that make systems smarter and scalable.  
            I believe in building meaningful tech that solves real-world problems — 
            from decentralized payrolls to analytics dashboards powered by blockchain and machine learning.  
            Beyond code, I’m an explorer of emerging tech ecosystems like **Web3, Edge AI, and LLM frameworks**.
            """
        )
        st.info("🧠 Motto: *Innovate with purpose, automate with intelligence.*")

    with about_col2:
        about_lottie = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_w51pcehl.json")
        if about_lottie:
            st_lottie(about_lottie, height=240, key="about_anim")

    # --- Timeline Section (Animated + Theme-Responsive + Lottie Rocket) ---
    # --- Timeline Section (with fallback rocket Lottie) ---
    st.markdown("---")
    st.markdown("## 🕒 My Journey Timeline")

    # 🚀 Add rocket animation at top (fallback-safe)
    rocket_url = "https://assets2.lottiefiles.com/packages/lf20_x62chJ.json"
    try:
        st_lottie(load_lottie_url(rocket_url), height=120, key="rocket_anim")
    except Exception:
        st.write("")

    st.markdown(
        """
        <style>
        /* 🎨 Universal Style – theme-safe */
        .timeline { position: relative; max-width: 900px; margin: 60px auto; overflow: hidden; }
        .timeline::after {
            content: '';
            position: absolute;
            width: 4px;
            background: linear-gradient(180deg, #00b4d8, #ff61a6);
            top: 0;
            bottom: 0;
            left: 50%;
            margin-left: -2px;
            animation: fadeInLine 2s ease-in-out;
        }

        .timeline-item { opacity: 0; transform: translateY(40px); animation: fadeInUp 1s forwards ease-out; }
        .timeline-item:nth-child(1) { animation-delay: 0.3s; }
        .timeline-item:nth-child(2) { animation-delay: 0.6s; }
        .timeline-item:nth-child(3) { animation-delay: 0.9s; }
        .timeline-item:nth-child(4) { animation-delay: 1.2s; }
        .timeline-item:nth-child(5) { animation-delay: 1.5s; }
        .timeline-item:nth-child(6) { animation-delay: 1.8s; }

        @keyframes fadeInUp { from { opacity: 0; transform: translateY(40px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes fadeInLine { from { height: 0; } to { height: 100%; } }
        @keyframes pulseGlow { 0% { box-shadow: 0 0 6px #00b4d8; } 50% { box-shadow: 0 0 20px #ff61a6; } 100% { box-shadow: 0 0 6px #00b4d8; } }

        .container { padding: 20px 40px; position: relative; width: 50%; }
        .container::after {
            content: '';
            position: absolute;
            width: 18px; height: 18px;
            right: -9px; top: 25px;
            background-color: #00b4d8;
            border-radius: 50%; z-index: 1;
            animation: pulseGlow 2.5s infinite ease-in-out;
        }

        .left { left: 0; }
        .right { left: 50%; }

        .left::before, .right::before {
            content: " "; height: 0; position: absolute; top: 33px;
            border: medium solid #00b4d8;
        }
        .left::before { right: 30px; border-width: 10px 0 10px 10px; border-color: transparent transparent transparent #00b4d8; }
        .right::before { left: 30px; border-width: 10px 10px 10px 0; border-color: transparent #00b4d8 transparent transparent; }

        .content {
            padding: 20px 30px;
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.15);
            transition: transform 0.3s ease, box-shadow 0.3s ease, border 0.3s ease;
            color: #fff;  /* Default text color for dark mode */
        }

        /* Force text color for dark/light mode */
        .content h4 {
            color: #00FFFF !important; 
        }
        .content p {
            color: #FFD700 !important; 
        }

        /* 🩶 Light mode overrides */
        @media (prefers-color-scheme: light) {
            .content {
                background: rgba(0,0,0,0.05);
                border: 1px solid rgba(0,0,0,0.1);
                color: #000; /* text color for light mode */
            }
        }

        .content:hover {
            transform: translateY(-6px);
            border: 1px solid #00b4d8;
            box-shadow: 0 6px 16px rgba(0, 180, 216, 0.4);
        }

        @media screen and (max-width: 600px) {
            .timeline::after { left: 31px; }
            .container { width: 100%; padding-left: 70px; padding-right: 25px; }
            .container::after { left: 15px; }
            .right { left: 0%; }
            .right::before { left: 60px; border-width: 10px 0 10px 10px; border-color: transparent transparent transparent #00b4d8; }
        }
        </style>

        <div class="timeline">
            <div class="timeline-item container left">
                <div class="content">
                    <h4>🎓 2020 — Started B.Tech in IT</h4>
                    <p>Developed strong fundamentals in Computer Science, AI, and Linux systems.</p>
                </div>
            </div>
            <div class="timeline-item container right">
                <div class="content">
                    <h4>🏆 2021 — Won First Blockchain Hackathon</h4>
                    <p>Built a decentralized payroll prototype integrating smart contracts.</p>
                </div>
            </div>
            <div class="timeline-item container left">
                <div class="content">
                    <h4>👨🏻‍💻2022 — Explored AI & ML</h4>
                    <p>Developed early models using Scikit-learn and Streamlit dashboards.</p>
                </div>
            </div>
            <div class="timeline-item container right">
                <div class="content">
                    <h4>🚀 2023 — Built NEARVision & FusePay</h4>
                    <p>Delivered hackathon-winning blockchain analytics and payroll platforms.</p>
                </div>
            </div>
            <div class="timeline-item container left">
                <div class="content">
                    <h4>💼 2024 — Joined HCLTech</h4>
                    <p>Working on Linux, AI integrations, and GenAI automation in infrastructure.</p>
                </div>
            </div>
            <div class="timeline-item container right">
                <div class="content">
                    <h4>⚙️ 2025 — AI + Infra Specialist</h4>
                    <p>Leading projects combining generative AI, cloud & automation for scalable systems.</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- Certifications Section ---
    st.markdown("---")
    st.markdown("## 🏅 Certifications & Recognitions")
    st.markdown(
        """
        - **AWS Certified Cloud Practitioner** ☁️  
        - **Linux Foundation Training** 🐧  
        - **Winner — Build with Celo 5 (Decentralized Payroll)** 🥇  
        - **Winner — Rootstock x Miami Hack Week (Blockchain AgriTech)** 🏆  
        - **Finalist — Daisi Hackathon (AI + ML Challenge)** 🎯  
        """
    )

    # --- Tech Philosophy Section ---
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align:center; padding:25px; font-size:20px; font-style:italic;'>
        “Technology isn’t about replacing people — it’s about augmenting potential.”  
        <br>— <b>Mohamed Farhun M</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------------------------
# 🚀 TECH SHOWCASE (Interactive Projects + Skills)
# -----------------------------------------------
elif menu == "👨🏻‍💻Tech Showcase":
    st.markdown("## 🚀 Tech Showcase — Projects & Skills")
    st.markdown("Explore my award-winning hackathon projects and the technology stack that powers them.")
    st.markdown("---")

    # --- Filter Chips ---
    CATEGORIES = ["All", "AI/ML", "Blockchain", "Data Science"]
    if "selected_category" not in st.session_state:
        st.session_state.selected_category = "All"

    st.markdown("### 🔍 Filter by Category")
    filter_cols = st.columns(len(CATEGORIES))
    for i, cat in enumerate(CATEGORIES):
        button_style = (
            "background-color: #00b4d8; color: white; font-weight:600;"
            if st.session_state.selected_category == cat
            else "background-color: rgba(0,0,0,0.05); color: var(--text-color);"
        )
        if filter_cols[i].button(f"🎯 {cat}", key=f"cat_{cat}", use_container_width=True):
            st.session_state.selected_category = cat

    # --- Categorization Logic ---
    def categorize_project(title, description, stack):
        text = f"{title} {description} {stack}".lower()
        if "eduregion" in text or "guardianai" in text:
            return ["AI/ML", "Data Science"]
        elif "blockchain" in text or "near" in text or "rootstock" in text or "celo" in text:
            return ["Blockchain"]
        elif "ai" in text or "ml" in text or "langchain" in text:
            return ["AI/ML"]
        elif "data" in text or "pandas" in text or "analysis" in text:
            return ["Data Science"]
        return ["General"]

    # --- Lottie URLs per project (topic-specific) ---
    lottie_map = {
        "FusePay": "assets/Celo_Icon.json",
        "NEARVision": "assets/Robot_AI.json",
        "Stock Market Analysis": "assets/Data_Analysis.json",
        "Cryptographic Farming": "assets/Farming.json",
        "EduRegion": "assets/Book_loading.json",
        "GuardianAI": "assets/Live_chatbot.json",
    }

    # --- CSS Styling (Center aligned + animation) ---
    st.markdown("""
    <style>
    .project-row {
         display: flex;
        justify-content: center;
        align-items: stretch;
        gap: 25px;                /* spacing between animation & card */
        width: 90%;
        max-width: 1100px;
        padding: 15px 0;          /* adds space above and below each row */
        margin-bottom: 20px;      /* vertical gap between cards */
        flex-wrap: wrap;
    }
    .project-card {
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        background: rgba(255, 255, 255, 0.05);
        transition: transform 0.4s ease, box-shadow 0.4s ease;
        animation: slideInLeft 1s ease forwards;
        box-sizing: border-box;
        margin-bottom: 5px;
    }
    .project-card.right { animation: slideInRight 1s ease forwards;text-align: left; }
    .project-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 10px 25px rgba(0, 180, 216, 0.45);
        border-color: #00b4d8;
    }
    @keyframes slideInLeft {
        from {opacity: 0; transform: translateX(-100px);}
        to {opacity: 1; transform: translateX(0);}
    }
    @keyframes slideInRight {
        from {opacity: 0; transform: translateX(100px);}
        to {opacity: 1; transform: translateX(0);}
    }
    .project-card h3 {
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800; font-size: 22px; margin-bottom: 10px;
    }
    .stack-badge {
        display: inline-block;
        background: rgba(0, 180, 216, 0.15);
        color: #00b4d8;
        border: 1px solid rgba(0,180,216,0.3);
        border-radius: 12px;
        padding: 3px 10px;
        margin: 2px;
        font-size: 13px;
    }
    .proj-links a { text-decoration: none; margin-right: 10px; font-weight: 600; }
    .proj-links a:hover { text-decoration: underline; }

    @media (prefers-color-scheme: light) {
        .project-card {
            background: rgba(0,0,0,0.05);
            border: 1px solid rgba(0,0,0,0.1);
        }
        .stack-badge {
            background: rgba(0,0,0,0.05);
            color: #0072ff;
        }
    }
    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(30px);}
        to {opacity: 1; transform: translateY(0);}
    }
    .project-card, .project-row {
        animation: fadeIn 1s ease forwards;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- Filtered Projects ---
    filtered_projects = []
    for p in PROJECTS:
        cats = categorize_project(p["title"], p["description"], p["stack"])
        if st.session_state.selected_category in cats or st.session_state.selected_category == "All":
            filtered_projects.append(p)

    # --- Render Projects with Alternating Animations ---
    st.markdown("<div class='project-grid'>", unsafe_allow_html=True)
    for idx, proj in enumerate(filtered_projects):
        is_left = idx % 2 == 0
        # Determine if Lottie path is local or URL
        lottie_path = next((path for key, path in lottie_map.items() if key.lower() in proj["title"].lower()), None)
        if lottie_path:
            if lottie_path.startswith("assets/"):
                lottie_obj = load_lottie_file(lottie_path)
            else:
                lottie_obj = load_lottie_url(lottie_path)
        else:
            lottie_obj = None

        st.markdown("<div class='project-row'>", unsafe_allow_html=True)
        col_left, col_right = st.columns([1.2, 1.2])
        with col_left if is_left else col_right:
            if lottie_obj:
                st_lottie(lottie_obj, height=220, speed=1, key=f"proj_lottie_{idx}")
        with col_right if is_left else col_left:
            stack_tags = " ".join([f"<span class='stack-badge'>{tag.strip()}</span>" for tag in proj.get("stack", "").split(",")])
            demo = f"<a href='{proj.get('demo')}' target='_blank'>▶ Live Demo</a>" if proj.get("demo") else ""
            github = f"<a href='{proj.get('github')}' target='_blank'>💻 GitHub</a>" if proj.get("github") else ""
            video = f"<a href='{proj.get('video')}' target='_blank'>🎬 Video</a>" if proj.get("video") else ""
            hack = f"<a href='{proj.get('hackathon')}' target='_blank'>🏁 Hackathon</a>" if proj.get("hackathon") else ""
            side_class = "right" if not is_left else ""
            st.markdown(f"""
            <div class='project-card {side_class}'>
                <h3>{proj['title']}</h3>
                <p>{proj['description']}</p>
                <div>{stack_tags}</div>
                <div class='proj-links'>{demo} {github} {video} {hack}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div>", unsafe_allow_html=True)

    # --- Skills Section ---
    st.markdown("---")
    st.markdown("## 🧠 Core Technical Skills")
    st.write("Here’s a visualization of my core proficiencies:")

    st.plotly_chart(radar_chart(SKILLS), use_container_width=True)
    for category, items in SKILLS.items():
        st.markdown(f"### {category}")
        st.markdown(" ".join([f"<span class='stack-badge'>{i}</span>" for i in items]), unsafe_allow_html=True)
    
    st.markdown("---")

    # --- Programming Languages Efficiency Data ---
    languages = ["Python", "JavaScript / TypeScript", "Solidity", "SQL", "Shell / Bash", "C / C++", "HTML / CSS", "Java"]
    efficiency = [85, 60, 65, 80, 50, 45, 75, 40]

    st.markdown("### 💻 Programming Languages Efficiency")

    lang_fig = go.Figure()

    lang_fig.add_trace(go.Bar(
        x=efficiency,
        y=languages,
        orientation='h',
        marker=dict(
            color=efficiency,
            colorscale="blues",
            line=dict(color='rgba(255,255,255,0.2)', width=1)
        ),
        text=[f"{v}%" for v in efficiency],
        textposition="outside",
        hovertemplate='%{y}: %{x}%',
    ))

    lang_fig.update_layout(
        xaxis=dict(showgrid=False, showticklabels=False, range=[0, 100]),
        yaxis=dict(showgrid=False),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#e2e8f0", size=14),
        margin=dict(l=80, r=50, t=20, b=40),
        height=430,
        transition=dict(duration=800, easing="cubic-in-out")
    )

    st.plotly_chart(lang_fig, use_container_width=True)

    st.markdown("---")

    # --- Frameworks / Libraries Proficiency Data ---
    frameworks = [
        "Streamlit", "Django", "React.js", "LangChain", "Flask",
        "Node.js / Express", "PyTorch / TensorFlow", "Docker", "Jenkins"
    ]
    proficiency = [95, 85, 70, 80, 75, 65, 60, 70, 65]

    st.markdown("### 🧱 Frameworks & Tools Expertise")

    framework_fig = go.Figure(go.Pie(
        labels=frameworks,
        values=proficiency,
        hole=0.45,
        marker=dict(
            colors=[
                "#00b4d8", "#0077b6", "#90e0ef", "#48cae4",
                "#00bfff", "#5ce1e6", "#219ebc", "#023e8a", "#8ecae6"
            ],
            line=dict(color='rgba(0,0,0,0)', width=1)
        ),
        text=[f"{v}%" for v in proficiency],  # show actual %
        textinfo="text",
        hovertemplate='%{label}: %{value}%',
    ))

    framework_fig.update_layout(
        showlegend=True,
        legend_title_text="Frameworks",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#e2e8f0", size=13),
        margin=dict(l=40, r=40, t=20, b=40),
        height=500,
        transition=dict(duration=800, easing="cubic-in-out")
    )

    st.plotly_chart(framework_fig, use_container_width=True)

    st.markdown("<br><hr><center>🧠 Continuously growing across AI, Data Science, and Blockchain innovation.</center>", unsafe_allow_html=True)

# -----------------------------------------------
# 🤖 AI RESUME NAVIGATOR
# -----------------------------------------------
elif menu == "📝 AI Resume Navigator":
    st.markdown("## FarhunBot — Resume Assistant (LangChain + OpenAI) 🎯")

    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import FAISS
    from langchain_openai import OpenAIEmbeddings
    from openai import OpenAI  # 👈 added this line
    from langchain.chains import ConversationalRetrievalChain
    from langchain.memory import ConversationBufferMemory
    from langchain_openai import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

    # --- Resume Download ---
    if Path(RESUME_PATH).exists():
        with open(RESUME_PATH, "rb") as f:
            st.download_button("📄 Download My Resume", f, file_name="Mohamed_Farhun_Resume.pdf", mime="application/pdf")
    else:
        st.warning("⚠️ Resume file not found!")

    # --- Maintain chat within same page only ---
    if "current_chat" not in st.session_state:
        st.session_state.current_chat = []
    if "active_page" not in st.session_state:
        st.session_state.active_page = "📝 AI Resume Navigator"

    # 🧹 Clear chat automatically if user switched pages
    if st.session_state.active_page != "📝 AI Resume Navigator":
        st.session_state.current_chat = []
        st.session_state.active_page = "📝 AI Resume Navigator"

    st.markdown("---")
    st.write("💬 Ask me anything about my resume, skills, or experience — I’ll answer like Mohamed Farhun himself!")

    # --- Load Resume & Create FAISS Vector Store ---
    @st.cache_resource(show_spinner=True)
    def load_resume_embeddings():
        text = get_pdf_text(RESUME_PATH)
        if not text:
            return None
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=200)
        chunks = splitter.split_text(text)
        embeddings = OpenAIEmbeddings(
        model="text-embedding-3-large",
         api_key=OPENAI_API_KEY
         )
        return FAISS.from_texts(chunks, embeddings)

    vectorstore = load_resume_embeddings()
    if not vectorstore:
        st.error("❌ Could not load or embed resume.")
    else:
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        # --- System Prompt ---
        system_prompt = """
        You are FarhunBot — an intelligent, friendly AI assistant built by Mohamed Farhun M.
        Your purpose is to help users understand Mohamed’s professional background, skills, projects, and achievements.

        Core Info about Mohamed:
        - Full Name: Mohamed Farhun M
        - Profession: AI & Linux Engineer at HCLTech
        - Expertise: AI/ML, DevOps, GenAI, Automation, Cloud Infrastructure
        - Key Skills: Python, Streamlit, Jenkins, Docker, LangChain, AWS, Azure, Linux
        - Awards: Multi-time Hackathon Winner (Celo, NEAR, Rootstock, Daisi)
        - Motto: "Innovate with purpose, automate with intelligence."
        - Passionate about building intelligent, self-healing systems combining AI and infrastructure automation.

        Use the following context from Mohamed’s resume to answer accurately:
        {context}

        Rules:
        - Always answer confidently.
        - Never say “I don’t know.”
        - Speak in first person (“I specialize in...”) as if you are Mohamed Farhun.
        - Be concise, friendly, and technically sound.
        """

        qa_prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template("{question}")
        ])

        llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.3, model="gpt-4o-mini")

        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            memory=memory,
            combine_docs_chain_kwargs={"prompt": qa_prompt},
            return_source_documents=False,
            verbose=False,
        )

        # --- Chat UI ---
        for msg in st.session_state.current_chat:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if user_query := st.chat_input("💬 Ask FarhunBot..."):
            st.session_state.current_chat.append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.markdown(user_query)

            with st.chat_message("assistant"):
                with st.spinner("Thinking... 🤔"):
                    response = qa_chain({"question": user_query})
                    answer = response["answer"]
                    st.markdown(answer)

            st.session_state.current_chat.append({"role": "assistant", "content": answer})

# -----------------------------------------------
# 🌟 Beyond the Code PAGE — Fixed HTML Rendering
# -----------------------------------------------
elif menu == "👉 Beyond the Code":
    # Load all photos dynamically from folders
    football_photos = load_images_from_folder("photos/football")
    hackathon_photos = load_images_from_folder("photos/hackathons")
    model_photos = load_images_from_folder("photos/modelling")
    gym_photos = load_images_from_folder("photos/gym")
    music_photos = load_images_from_folder("photos/music")

    # 🎨 CSS Styling
    st.markdown("""
    <style>
    .others-section { 
        padding: 40px 20px; 
        font-family: "Poppins", sans-serif; 
    }

    /* 🌟 Glassmorphic Card with Gradient Glow */
    .glass-card {
        max-width: 900px;
        margin: 40px auto;
        padding: 30px;
        border-radius: 20px;
        background: rgba(255,255,255,0.06);
        backdrop-filter: blur(14px);
        border: 1px solid rgba(255,255,255,0.15);
        box-shadow: 0 8px 25px rgba(0,0,0,0.35);
        position: relative;
        overflow: hidden;
        transition: all 0.35s ease-in-out;
    }

    /* ✨ Glowing Gradient Border Effect */
    .glass-card::before {
        content: "";
        position: absolute;
        inset: 0;
        border-radius: 20px;
        padding: 1px;
        background: linear-gradient(120deg, #00c6ff, #0072ff);
        -webkit-mask: 
            linear-gradient(#fff 0 0) content-box, 
            linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
                mask-composite: exclude;
        opacity: 0;
        transition: opacity 0.4s ease-in-out;
    }

    /* 💫 Hover Animation (Glow + Lift) */
    .glass-card:hover::before {
        opacity: 1;
    }

    .glass-card:hover { 
        transform: translateY(-6px);
        box-shadow: 0 12px 30px rgba(0,180,216,0.45);
    }

    h2 { 
        color: #00b4d8; 
        text-align: center; 
        font-weight: 800; 
    }

    .desc { 
        font-size: 17px; 
        opacity: 0.9; 
        text-align: justify; 
        margin-bottom: 20px; 
    }

    .quote { 
        text-align: center; 
        color: #00c6ff; 
        font-style: italic; 
        font-weight: 600; 
        margin-top: 15px; 
    }

    .slideshow {
        position: relative; 
        width: 100%; 
        max-width: 820px; 
        height: 440px;
        margin: 20px auto; 
        border-radius: 18px; 
        overflow: hidden;
        box-shadow: 0 10px 25px rgba(0,0,0,0.4);
    }

    .slides {
        display: flex; 
        animation: fadeSlide 25s infinite;
    }

    .slides img {
        width: 100%; 
        height: 440px; 
        object-fit: contain;
        background: #000; 
        border-radius: 18px; 
        flex-shrink: 0;
    }

    @keyframes fadeSlide {
        0%,20% {transform: translateX(0);}
        25%,40% {transform: translateX(-100%);}
        45%,60% {transform: translateX(-200%);}
        65%,80% {transform: translateX(-300%);}
        85%,100% {transform: translateX(0);}
    }
    </style>
    """, unsafe_allow_html=True)

    def generate_slideshow(base64_images):
        imgs_html = "".join([f'<img src="data:image/jpeg;base64,{img}">' for img in base64_images])
        return f'<div class="slideshow"><div class="slides">{imgs_html}</div></div>'

    st.markdown("<div class='others-section'>", unsafe_allow_html=True)

    # 🌟 Section Title
    st.markdown("""
        <div style="
            text-align:center; 
            margin-bottom: 60px;
            ">
            <h1 style="
                background: linear-gradient(90deg, #00c6ff, #0072ff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 42px;
                font-weight: 900;
                letter-spacing: 1px;
            ">
                🚀 Beyond the Code
            </h1>
            <p style="
                font-size: 18px; 
                opacity: 0.85; 
                max-width: 800px; 
                margin: 10px auto 0; 
                line-height: 1.6;
            ">
                A glimpse into my world outside of tech — where passion meets creativity.  
                From the adrenaline of football fields to the calm rhythm of music, this is where I recharge, grow, and stay inspired.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # ⚽ Football
    st.markdown("""
    <div class="glass-card">
        <h2>⚽ Football — My Passion</h2>
        <p class="desc">
            Football isn’t just a sport for me — it’s an emotion that defines my rhythm of life.
            Watching matches and playing the game gives me an adrenaline rush like no other.
            The strategy, teamwork, and thrill of a perfect goal always remind me why I fell in love with football.
            My inspiration? The one and only <b>Eden Hazard</b> — whose elegance and creativity on the field never fail to amaze me.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(generate_slideshow(football_photos), unsafe_allow_html=True)
    st.markdown('<p class="quote">"When I have the ball at my feet, I’m the happiest person on Earth." 🥅</p>', unsafe_allow_html=True)

    # 💡 Hackathons
    st.markdown("""
    <div class="glass-card">
        <h2>💡 Hackathons — The Game Changer</h2>
        <p class="desc">
            Hackathons have shaped who I am as a technologist.
            They’ve helped me win over ₹3,00,000 across multiple events and explore domains like AI, Machine Learning, Blockchain, and DevOps.
            Every hackathon I’ve participated in taught me something invaluable — from teamwork and time management to hands-on coding experience.
            I firmly believe that <b>knowledge grows when you build, not when you just read</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(generate_slideshow(hackathon_photos), unsafe_allow_html=True)
    st.markdown('<p class="quote">"Learning by doing is the only way to stand out in a crowd of learners." 🚀</p>', unsafe_allow_html=True)

    # 👔 Modelling
    st.markdown("""
    <div class="glass-card">
        <h2>👔 Modelling — Confidence Meets Style</h2>
        <p class="desc">
            Modelling is more than just posing for pictures — it’s about confidence, expression, and owning who you are.
            I’ve developed courage and self-assurance through it, and it has become an art that reflects my personality.
            No matter what happens, two things never fade away from me — <b>Smile and Style</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(generate_slideshow(model_photos), unsafe_allow_html=True)
    st.markdown('<p class="quote">"Smile and Style — my unshakable constants in life." 😎</p>', unsafe_allow_html=True)

    # 🏋️‍♂️ Gym
    st.markdown("""
    <div class="glass-card">
        <h2>🏋️‍♂️ Fitness — Aging Like Fine Wine</h2>
        <p class="desc">
            Staying fit is my top priority. I believe that health is the foundation of every success.
            My dream is to age like fine wine — strong, flexible, and full of vitality, even in my 60s.
            I draw my inspiration from personalities like <b>Nagarjuna</b>, who prove that age is just a number when you take care of your body.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(generate_slideshow(gym_photos), unsafe_allow_html=True)
    st.markdown('<p class="quote">"Train hard, stay humble, and let your discipline speak louder than words." 💪</p>', unsafe_allow_html=True)

    # 🎧 Music
    st.markdown("""
    <div class="glass-card">
        <h2>🎧 Music — My Soul’s Escape</h2>
        <p class="desc">
            Music heals me in ways words can’t describe.
            I often find myself dancing alone, lost in the rhythm of my favorite Tamil classics and English hits.
            It’s my way of resetting — a quiet joy that fuels my creativity and focus.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(generate_slideshow(music_photos), unsafe_allow_html=True)
    st.markdown('<p class="quote">"When words fail, music speaks." 🎵</p>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------- # 📬 CONTACT # ----------------------------------------------- 
elif menu == "📩 Contact":
    import smtplib
    from email.message import EmailMessage

    st.markdown("## 📬 Let's Connect")
    col1, col2 = st.columns([2, 1])

    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    RECEIVER_EMAIL = "farhunhazard@gmail.com"  # You’ll receive all messages here

    def send_email(name, sender_email, message):
        try:
            msg = EmailMessage()
            msg["Subject"] = f"📩 New Message from {name} — FarhunVerse Portfolio"
            msg["From"] = EMAIL_USER
            msg["To"] = RECEIVER_EMAIL
            msg.set_content(
                f"""
Hey Farhun 👋,

You just got a new message from your FarhunVerse portfolio site!

🧑 Name: {name}
📧 Email: {sender_email}

💬 Message:
{message}

----------------------------
This email was automatically sent from your Streamlit portfolio.
                """
            )

            # Send the email via Gmail SMTP
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(EMAIL_USER, EMAIL_PASS)
                smtp.send_message(msg)
            return True
        except Exception as e:
            st.error(f"❌ Failed to send email: {e}")
            return False

    with col1:
        with st.form("contact_form"):
            name = st.text_input("Your Name")
            email = st.text_input("Your Email")
            message = st.text_area("Your Message")

            submitted = st.form_submit_button("Send Message")
            if submitted:
                if not name or not email or not message:
                    st.warning("⚠️ Please fill in all fields before submitting.")
                else:
                    with st.spinner("📨 Sending your message..."):
                        if send_email(name, email, message):
                            st.success(f"✅ Thanks {name}! Your message has been sent successfully.")
                            st.balloons()
                        else:
                            st.error("❌ Something went wrong. Please try again later.")

        st.markdown("---")
        st.markdown("### 🌐 Connect on Other Platforms")
        for platform, link in SOCIALS.items():
            st.markdown(f"- [{platform}]({link})")

    with col2:
        if lottie_connect:
            st_lottie(lottie_connect, height=250, key="contact_lottie")

# -----------------------------------------------
# 🌐 GLOBAL FOOTER (Displayed on all pages)
# -----------------------------------------------
st.markdown("""
<div id="custom-footer">
    🚀 Built with ❤️ using Streamlit | © 2025 Mohamed Farhun M
</div>
""", unsafe_allow_html=True)
