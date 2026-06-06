import streamlit as st
from modules.styles import inject_styles
from modules.i18n import T
from modules.home import render_home
from modules.expenses import render_expenses
from modules.savings import render_savings
from modules.goals import render_goals
from modules.debts import render_debts
from modules.investments import render_investments
from modules.reports import render_reports
from modules.tips import render_tips

st.set_page_config(
    page_title="مسار | إدارة مالية ذكية",
    page_icon="💶",
    layout="centered",
    initial_sidebar_state="collapsed"
)

DEFAULTS = {
    "lang": "ar", "currency": "€", "income": 0,
    "user_name": "المستخدم", "expenses": [], "savings": [],
    "debts": [], "goals": [], "investments": [],
    "active_tab": "home", "add_sub": "expense", "chat_messages": [],
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

inject_styles()

with st.sidebar:
    lang = st.session_state.lang
    st.markdown(f"### ⚙️ {T('settings', lang)}")
    st.session_state.user_name = st.text_input(T("user_name", lang), value=st.session_state.user_name)
    st.session_state.income = st.number_input(T("monthly_income", lang), min_value=0.0, value=float(st.session_state.income), step=50.0)
    st.session_state.currency = st.selectbox(T("currency", lang), ["€","$","£","﷼","د.إ","TL"], index=["€","$","£","﷼","د.إ","TL"].index(st.session_state.currency))
    lang_options = {"العربية": "ar", "Deutsch": "de", "English": "en"}
    lang_label = {v: k for k, v in lang_options.items()}.get(st.session_state.lang, "العربية")
    chosen_lang = st.selectbox(T("language", lang), list(lang_options.keys()), index=list(lang_options.keys()).index(lang_label))
    st.session_state.lang = lang_options[chosen_lang]

tab_param = st.query_params.get("tab", None)
if tab_param and tab_param != st.session_state.active_tab:
    st.session_state.active_tab = tab_param

sub_param = st.query_params.get("sub", None)
if sub_param and sub_param != st.session_state.add_sub:
    st.session_state.add_sub = sub_param

active = st.session_state.active_tab
lang   = st.session_state.lang


def render_bottom_nav():
    lg = st.session_state.lang
    at = st.session_state.active_tab
    labels = {
        "ar": [("home","🏠","الرئيسية"),("reports","📊","التقارير"),("add","➕","إضافة"),("tips","💡","نصائح"),("account","👤","حسابي")],
        "de": [("home","🏠","Start"),("reports","📊","Berichte"),("add","➕","Neu"),("tips","💡","Tipps"),("account","👤","Konto")],
        "en": [("home","🏠","Home"),("reports","📊","Reports"),("add","➕","Add"),("tips","💡","Tips"),("account","👤","Account")],
    }
    tabs = labels.get(lg, labels["ar"])
    parts = []
    for key, icon, label in tabs:
        cls = "nav-btn active" if at == key else "nav-btn"
        parts.append(
            f'<a class="{cls}" href="?tab={key}" target="_self">' +
            f'<div class="nav-icon-wrap"><span class="nav-icon">{icon}</span></div>' +
            f'<span class="nav-label">{label}</span></a>'
        )
    st.markdown('<nav class="bottom-nav">' + "".join(parts) + "</nav>", unsafe_allow_html=True)


def render_add_page():
    lg = st.session_state.lang
    sub_data = [
        ("expense","🧾",T("nav_expenses",lg)),
        ("saving","🏦",T("nav_savings",lg)),
        ("goal","🎯",T("nav_goals",lg)),
        ("debt","💳",T("nav_debts",lg)),
        ("investment","📈",T("nav_investments",lg)),
    ]
    current = st.session_state.add_sub
    st.markdown(f'<div class="section-heading">➕ {T("nav_add", lg)}</div>', unsafe_allow_html=True)

    parts = []
    for key, icon, label in sub_data:
        cls = "add-tab-card active" if current == key else "add-tab-card"
        parts.append(
            f'<a class="{cls}" href="?tab=add&sub={key}" target="_self">' +
            f'<span class="add-tab-icon">{icon}</span>' +
            f'<span class="add-tab-label">{label}</span></a>'
        )
    st.markdown('<div class="add-tabs-header">' + "".join(parts) + "</div>", unsafe_allow_html=True)

    sub = st.session_state.add_sub
    if sub == "expense":      render_expenses()
    elif sub == "saving":     render_savings()
    elif sub == "goal":       render_goals()
    elif sub == "debt":       render_debts()
    elif sub == "investment": render_investments()


def render_account():
    lg = st.session_state.lang
    c  = st.session_state.currency
    st.markdown(f"""
    <div style="background:#fff;border-radius:20px;padding:20px;
                box-shadow:0 8px 24px rgba(20,42,74,0.08);margin-bottom:14px;">
      <div style="font-size:1.3rem;font-weight:900;margin-bottom:4px;">{st.session_state.user_name}</div>
      <div style="font-size:0.9rem;color:#7a8899;">{T('monthly_income',lg)}: {st.session_state.income:,.0f} {c}</div>
    </div>""", unsafe_allow_html=True)
    msg_map = {"ar": "غيّر إعداداتك من القائمة الجانبية ☰", "de": "Einstellungen in der Seitenleiste ☰", "en": "Change settings in the sidebar ☰"}
    st.info("⚙️ " + msg_map.get(lg, msg_map["ar"]))
    st.markdown('<div class="section-heading">📋 ملخص البيانات</div>', unsafe_allow_html=True)
    for label, count in [
        (T("nav_expenses",lg), len(st.session_state.expenses)),
        (T("nav_savings",lg),  len(st.session_state.savings)),
        (T("nav_debts",lg),    len(st.session_state.debts)),
        (T("nav_goals",lg),    len(st.session_state.goals)),
        (T("nav_investments",lg), len(st.session_state.investments)),
    ]:
        st.markdown(f'<div class="data-row"><div class="data-row-info"><div class="data-row-name">{label}</div></div><div class="data-row-amount">{count}</div></div>', unsafe_allow_html=True)


if   active == "home":    render_home()
elif active == "add":     render_add_page()
elif active == "reports": render_reports()
elif active == "tips":    render_tips()
elif active == "account": render_account()

render_bottom_nav()
