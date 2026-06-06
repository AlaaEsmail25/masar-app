
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

    /* ── FIX 1: إخفاء الشريط الجانبي تماماً ── */
    [data-testid="collapsedControl"] { display: none !important; }
    [data-testid="stSidebarCollapsedControl"] { display: none !important; }
    section[data-testid="stSidebar"] {
        transform: translateX(100%) !important;
        visibility: hidden !important;
        width: 0 !important;
        min-width: 0 !important;
    }
    section[data-testid="stSidebar"][aria-expanded="true"] {
        transform: translateX(0) !important;
        visibility: visible !important;
        width: 280px !important;
    }
    /* إخفاء الشريط الرفيع تماماً */
    .css-1lcbmhc, .css-hxt7ib, [data-testid="stSidebarNav"],
    div[class*="sidebar-content"],
    div.css-1d391kg { display: none !important; }

    .block-container {
        max-width: 460px !important;
        padding: 0 12px 140px 12px !important;
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

    /* ── FIX 3 & 4: بطاقات التبويب الاحترافية ─── */
    .add-tabs-header {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
        margin-bottom: 20px;
    }
    .add-tab-card {
        background: #fff;
        border-radius: 18px;
        padding: 16px 12px;
        text-align: center;
        cursor: pointer;
        border: 2.5px solid transparent;
        box-shadow: var(--shadow-sm);
        transition: all 0.2s ease;
        text-decoration: none;
        display: block;
    }
    .add-tab-card.active {
        border-color: var(--primary);
        background: var(--primary-light);
        box-shadow: 0 6px 20px rgba(11,122,127,0.18);
        transform: translateY(-2px);
    }
    .add-tab-card:hover:not(.active) {
        transform: translateY(-1px);
        box-shadow: var(--shadow);
    }
    .add-tab-icon {
        font-size: 1.8rem;
        margin-bottom: 6px;
        display: block;
    }
    .add-tab-label {
        font-size: 0.9rem;
        font-weight: 800;
        color: var(--text);
        font-family: 'Cairo', sans-serif;
    }
    .add-tab-card.active .add-tab-label { color: var(--primary); }

    /* ── FAB زر الإضافة ──────────────────────── */
    .fab-btn {
        position: fixed;
        bottom: 90px;
        left: 50%;
        transform: translateX(-50%);
        width: 64px; height: 64px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--primary) 0%, #0a9ea6 100%);
        color: #fff;
        font-size: 2rem;
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 8px 28px rgba(11,122,127,0.38);
        cursor: pointer;
        z-index: 9998;
        border: none;
        text-decoration: none;
        transition: all 0.2s ease;
    }
    .fab-btn:hover { transform: translateX(-50%) scale(1.1); }

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

    /* ── FIX 2: Bottom Nav — نصوص عربية كاملة ─── */
    .bottom-nav {
        position: fixed; bottom: 0; left: 0; right: 0;
        background: rgba(255,255,255,0.98);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-top: 1px solid #e8edf3;
        padding: 8px 4px 12px;
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 0;
        z-index: 9999;
        box-shadow: 0 -4px 24px rgba(20,42,74,0.08);
    }
    .nav-btn {
        text-align: center;
        padding: 6px 2px 4px;
        border-radius: 14px;
        cursor: pointer;
        color: var(--faint);
        text-decoration: none;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        transition: all .18s ease;
        min-width: 0;
    }
    .nav-btn.active {
        color: var(--primary);
    }
    .nav-btn.active .nav-icon-wrap {
        background: var(--primary-light);
        border-radius: 14px;
    }
    .nav-icon-wrap {
        width: 44px; height: 34px;
        display: flex; align-items: center; justify-content: center;
        border-radius: 14px;
        transition: all .18s ease;
        margin-bottom: 2px;
    }
    .nav-icon { font-size: 1.3rem; line-height: 1; }
    /* FIX 2: حجم النص في Nav أكبر + لا قطع */
    .nav-label {
        font-size: 0.72rem;
        font-weight: 700;
        font-family: 'Cairo', sans-serif !important;
        white-space: nowrap;
        overflow: visible;
        text-overflow: clip;
        line-height: 1.2;
        max-width: 60px;
        display: block;
    }

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

    .stTextInput input, .stNumberInput input, .stDateInput input {
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
    label { font-family: 'Cairo', sans-serif !important; direction: rtl !important; }

    /* ── Notification alerts ────────────────────── */
    .notif-alert {
        border-radius: 14px; padding: 12px 16px;
        margin-bottom: 10px; font-size: 0.92rem; font-weight: 700;
    }
    .notif-red    { background: #fff0f0; color: #c0392b; border-right: 4px solid #e74c3c; }
    .notif-yellow { background: #fff8e1; color: #b7770d; border-right: 4px solid #f0a500; }
    .notif-green  { background: #e8fff3; color: #1a7a46; border-right: 4px solid #27a765; }

    /* hide streamlit radio default styling for add page */
    div[data-testid="stRadio"] { display: none !important; }

    </style>
    """, unsafe_allow_html=True)
