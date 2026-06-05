
import streamlit as st

def inject_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900&display=swap');

    :root {
        --bg: #eef3fb;
        --card: #ffffff;
        --text: #16202a;
        --muted: #7a8899;
        --faint: #b0bac5;
        --primary: #0b7a7f;
        --primary-light: #dff3f1;
        --primary-hover: #085e62;
        --blue: #3b6fd8;
        --green: #27a765;
        --red: #d46b6b;
        --orange: #f0a500;
        --shadow: 0 8px 24px rgba(20,42,74,0.08);
        --shadow-sm: 0 2px 8px rgba(20,42,74,0.05);
        --r-lg: 24px;
        --r-md: 18px;
        --r-sm: 12px;
    }

    html, body, [class*="css"], .stApp {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl;
        background: var(--bg) !important;
    }

    #MainMenu, header, footer, .stDeployButton { visibility: hidden !important; }
    .viewerBadge_container__1QSob { display: none !important; }

    .block-container {
        max-width: 440px !important;
        padding: 0 12px 120px 12px !important;
        margin: 0 auto !important;
    }

    /* ── Top header ─────────────────────────────── */
    .top-header {
        background: #fff;
        border-radius: 0 0 28px 28px;
        padding: 16px 18px 14px;
        box-shadow: var(--shadow-sm);
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
    }
    .avatar-chip {
        width: 46px; height: 46px;
        border-radius: 15px;
        background: var(--primary);
        color: #fff;
        font-size: 1.3rem; font-weight: 800;
        display: flex; align-items: center; justify-content: center;
        flex-shrink: 0;
    }
    .user-meta { flex: 1; text-align: right; }
    .user-name { font-size: 1.3rem; font-weight: 800; color: var(--text); line-height: 1.2; }
    .user-date { font-size: 0.85rem; color: var(--muted); margin-top: 1px; }
    .notif-btn {
        width: 44px; height: 44px;
        border-radius: 14px;
        background: #f4f7fc;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.3rem; position: relative; cursor: pointer;
        flex-shrink: 0;
    }
    .notif-btn::after {
        content: ""; position: absolute; top: 8px; right: 8px;
        width: 9px; height: 9px;
        background: #eb5757; border-radius: 50%; border: 2px solid #fff;
    }

    /* ── Balance card ───────────────────────────── */
    .balance-card {
        background: #fff;
        border-radius: var(--r-lg);
        box-shadow: var(--shadow);
        padding: 18px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        margin-bottom: 14px;
    }
    .balance-info { text-align: right; flex: 1; }
    .balance-label { font-size: 0.9rem; color: var(--faint); margin-bottom: 4px; }
    .balance-value { font-size: 2rem; font-weight: 900; color: var(--primary); line-height: 1.1; }
    .balance-sub { font-size: 0.88rem; color: var(--muted); margin-top: 6px; }

    /* ── Donut ring ─────────────────────────────── */
    .ring-wrap { position: relative; width: 88px; height: 88px; flex-shrink: 0; }
    .ring-wrap svg { width: 88px; height: 88px; transform: rotate(-90deg); }
    .ring-bg { fill: none; stroke: #e8edf3; stroke-width: 8; }
    .ring-fill { fill: none; stroke: var(--primary); stroke-width: 8;
                 stroke-linecap: round; transition: stroke-dashoffset .6s ease; }
    .ring-label {
        position: absolute; top: 50%; left: 50%;
        transform: translate(-50%,-50%);
        font-size: 0.92rem; font-weight: 800; color: var(--primary);
    }

    /* ── Metric card ────────────────────────────── */
    .metric-card {
        background: #fff;
        border-radius: var(--r-md);
        box-shadow: var(--shadow-sm);
        padding: 14px 16px;
        display: grid;
        grid-template-columns: 54px 1fr auto;
        gap: 12px;
        align-items: center;
        margin-bottom: 11px;
    }
    .metric-icon {
        width: 52px; height: 52px;
        border-radius: 15px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.5rem; flex-shrink: 0;
    }
    .ic-purple { background: #eef0ff; }
    .ic-green  { background: #e8fff3; }
    .ic-yellow { background: #fff8e1; }
    .ic-red    { background: #fff0f0; }
    .ic-blue   { background: #e8f0ff; }

    .metric-mid { text-align: right; }
    .metric-title { font-size: 1.1rem; font-weight: 800; color: var(--text); line-height: 1.2; }
    .metric-sub { font-size: 0.82rem; color: var(--muted); margin-top: 2px; }
    .metric-pill {
        display: inline-block; background: var(--blue); color: #fff;
        padding: 2px 9px; border-radius: 8px; font-size: 0.78rem; margin-top: 5px;
    }
    .metric-right { text-align: left; min-width: 80px; }
    .metric-val { font-size: 1.3rem; font-weight: 800; color: var(--text); line-height: 1.1; }
    .trend-up   { font-size: 0.82rem; color: var(--green); margin-top: 4px; }
    .trend-down { font-size: 0.82rem; color: var(--red);   margin-top: 4px; }

    /* ── Section heading ────────────────────────── */
    .section-heading {
        font-size: 1.05rem; font-weight: 800; color: var(--text);
        margin: 18px 0 10px; padding-right: 4px;
    }

    /* ── Add page tabs ──────────────────────────── */
    .add-tabs { display: flex; gap: 8px; margin-bottom: 16px; flex-wrap: wrap; }
    .add-tab {
        flex: 1; min-width: 80px; padding: 8px 6px;
        border-radius: 12px; text-align: center;
        font-size: 0.82rem; font-weight: 700; cursor: pointer;
        background: #f4f7fc; color: var(--muted); border: none;
    }
    .add-tab.active { background: var(--primary-light); color: var(--primary); }

    /* ── Form card ──────────────────────────────── */
    .form-card {
        background: #fff;
        border-radius: var(--r-md);
        box-shadow: var(--shadow-sm);
        padding: 18px;
        margin-bottom: 14px;
    }
    .form-title { font-size: 1.1rem; font-weight: 800; color: var(--text); margin-bottom: 14px; }

    /* ── Data row ───────────────────────────────── */
    .data-row {
        background: #fff;
        border-radius: var(--r-sm);
        padding: 12px 14px;
        margin-bottom: 8px;
        display: flex; align-items: center; justify-content: space-between;
        box-shadow: var(--shadow-sm);
    }
    .data-row-info { text-align: right; }
    .data-row-name { font-size: 0.97rem; font-weight: 700; color: var(--text); }
    .data-row-sub  { font-size: 0.8rem; color: var(--muted); margin-top: 2px; }
    .data-row-amount { font-size: 1.1rem; font-weight: 800; color: var(--primary); }

    /* ── Progress bar ───────────────────────────── */
    .prog-bar-wrap { background: #e8edf3; border-radius: 99px; height: 8px; overflow: hidden; margin: 6px 0; }
    .prog-bar-fill { height: 100%; border-radius: 99px; background: var(--primary); transition: width .5s ease; }

    /* ── AI chat area ───────────────────────────── */
    .ai-header {
        background: linear-gradient(135deg, var(--primary) 0%, #0a9ea6 100%);
        border-radius: var(--r-lg);
        padding: 18px;
        color: #fff;
        margin-bottom: 14px;
    }
    .ai-title { font-size: 1.2rem; font-weight: 800; margin-bottom: 4px; }
    .ai-sub { font-size: 0.88rem; opacity: 0.85; }

    /* ── Bottom nav ─────────────────────────────── */
    .bottom-nav {
        position: fixed; bottom: 14px; left: 50%;
        transform: translateX(-50%);
        width: min(420px, calc(100vw - 20px));
        background: rgba(255,255,255,0.97);
        backdrop-filter: blur(16px);
        border-radius: 26px;
        padding: 8px 6px;
        box-shadow: 0 16px 40px rgba(23,40,70,0.16);
        display: grid; grid-template-columns: repeat(5, 1fr);
        gap: 2px; z-index: 9999;
    }
    .nav-btn {
        text-align: center; padding: 9px 4px;
        border-radius: 18px; cursor: pointer;
        color: var(--faint); text-decoration: none;
        display: block; transition: all .18s ease;
    }
    .nav-btn.active { color: var(--primary); background: var(--primary-light); }
    .nav-btn:hover:not(.active) { background: #f4f7fc; color: var(--muted); }
    .nav-icon { font-size: 1.35rem; display: block; margin-bottom: 2px; line-height: 1.2; }
    .nav-label { font-size: 0.73rem; font-weight: 700; }

    /* ── Streamlit overrides ────────────────────── */
    .stButton > button {
        width: 100%; border-radius: 14px !important;
        background: var(--primary) !important; color: #fff !important;
        font-family: 'Cairo', sans-serif !important;
        font-weight: 700 !important; font-size: 1rem !important;
        padding: 10px !important; border: none !important;
        box-shadow: 0 4px 14px rgba(11,122,127,0.25) !important;
        transition: all .18s ease !important;
    }
    .stButton > button:hover { background: var(--primary-hover) !important; transform: translateY(-1px); }

    .stTextInput input, .stNumberInput input, .stDateInput input, .stSelectbox select {
        direction: rtl !important; border-radius: 12px !important;
        font-family: 'Cairo', sans-serif !important;
        border: 1px solid #dde3ec !important;
    }
    .stSelectbox > div > div { border-radius: 12px !important; }

    div[data-testid="stChatMessage"] {
        border-radius: 18px !important;
        font-family: 'Cairo', sans-serif !important;
    }
    div[data-testid="stChatInput"] textarea {
        direction: rtl !important;
        font-family: 'Cairo', sans-serif !important;
        border-radius: 14px !important;
    }

    .stAlert { border-radius: 14px !important; font-family: 'Cairo', sans-serif !important; }
    .stMetric { font-family: 'Cairo', sans-serif !important; }
    label { font-family: 'Cairo', sans-serif !important; direction: rtl !important; }

    /* notification alert */
    .notif-alert {
        border-radius: 14px; padding: 12px 16px;
        margin-bottom: 10px; font-size: 0.92rem; font-weight: 700;
    }
    .notif-red    { background: #fff0f0; color: #c0392b; border-right: 4px solid #e74c3c; }
    .notif-yellow { background: #fff8e1; color: #b7770d; border-right: 4px solid #f0a500; }
    .notif-green  { background: #e8fff3; color: #1a7a46; border-right: 4px solid #27a765; }
    </style>
    """, unsafe_allow_html=True)
