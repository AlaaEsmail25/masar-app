
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

# ── Page config ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="مسار | إدارة مالية ذكية",
    page_icon="💶",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── Session state defaults ───────────────────────────────────────────
DEFAULTS = {
    "lang":        "ar",
    "currency":    "€",
    "income":      0,
    "user_name":   "المستخدم",
    "expenses":    [],
    "savings":     [],
    "debts":       [],
    "goals":       [],
    "investments": [],
    "active_tab":  "home",
    "add_sub":     "expense",
    "chat_messages": [],
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

inject_styles()

# ── Settings sidebar ─────────────────────────────────────────────────
with st.sidebar:
    lang = st.session_state.lang
    st.markdown(f"### ⚙️ {T('settings', lang)}")
    st.session_state.user_name = st.text_input(
        T("user_name", lang), value=st.session_state.user_name)
    st.session_state.income = st.number_input(
        T("monthly_income", lang), min_value=0.0, value=float(st.session_state.income), step=50.0)
    st.session_state.currency = st.selectbox(
        T("currency", lang), ["€", "$", "£", "﷼", "د.إ", "TL"], index=["€","$","£","﷼","د.إ","TL"].index(st.session_state.currency))
    lang_options = {"العربية": "ar", "Deutsch": "de", "English": "en"}
    lang_label = {v: k for k, v in lang_options.items()}.get(st.session_state.lang, "العربية")
    chosen_lang = st.selectbox(T("language", lang), list(lang_options.keys()), index=list(lang_options.keys()).index(lang_label))
    st.session_state.lang = lang_options[chosen_lang]

# ── Bottom navigation renderer ───────────────────────────────────────
def render_bottom_nav():
    lang = st.session_state.lang
    active = st.session_state.active_tab
    tabs = [
        ("account", "👤", T("settings", lang)),
        ("tips",    "💡", T("nav_tips",  lang)[:4]),
        ("add",     "➕", T("nav_add",   lang)),
        ("reports", "📊", T("nav_reports", lang)[:6]),
        ("home",    "🏠", T("nav_dashboard", lang)[:5]),
    ]
    html = '<div class="bottom-nav">'
    for key, icon, label in tabs:
        cls = "nav-btn active" if active == key else "nav-btn"
        html += f'<a class="{cls}" href="?tab={key}" target="_self"><span class="nav-icon">{icon}</span><span class="nav-label">{label}</span></a>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

# ── Resolve active tab from URL ──────────────────────────────────────
tab_param = st.query_params.get("tab", None)
if tab_param and tab_param != st.session_state.active_tab:
    st.session_state.active_tab = tab_param

active = st.session_state.active_tab

# ── Page router ──────────────────────────────────────────────────────
if active == "home":
    render_home()

elif active == "add":
    lang = st.session_state.lang
    sub_options = {
        T("nav_expenses",lang): "expense",
        T("nav_savings",lang):  "saving",
        T("nav_goals",lang):    "goal",
        T("nav_debts",lang):    "debt",
        T("nav_investments",lang): "investment",
    }
    sub_labels = list(sub_options.keys())
    cur_idx = list(sub_options.values()).index(st.session_state.add_sub) if st.session_state.add_sub in sub_options.values() else 0
    chosen = st.radio("", sub_labels, index=cur_idx, horizontal=True, label_visibility="collapsed")
    st.session_state.add_sub = sub_options[chosen]

    if st.session_state.add_sub == "expense":
        render_expenses()
    elif st.session_state.add_sub == "saving":
        render_savings()
    elif st.session_state.add_sub == "goal":
        render_goals()
    elif st.session_state.add_sub == "debt":
        render_debts()
    elif st.session_state.add_sub == "investment":
        render_investments()

elif active == "reports":
    render_reports()

elif active == "tips":
    render_tips()

elif active == "account":
    lang = st.session_state.lang
    st.markdown(f'<div class="section-heading">👤 {T("settings",lang)}</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:#fff;border-radius:20px;padding:20px;box-shadow:0 8px 24px rgba(20,42,74,0.08);">
      <div style="font-size:1.1rem;font-weight:800;margin-bottom:4px;">{st.session_state.user_name}</div>
      <div style="font-size:.9rem;color:#7a8899;">
        {T('monthly_income',lang)}: {st.session_state.income:,.0f} {st.session_state.currency}
      </div>
    </div>""", unsafe_allow_html=True)
    st.info("⚙️ " + ("غيّر الإعدادات من القائمة الجانبية ← " if lang=="ar" else "Change settings from sidebar ←"))

    # Summary stats
    expenses  = st.session_state.expenses
    savings   = st.session_state.savings
    debts     = st.session_state.debts
    goals     = st.session_state.goals
    invs      = st.session_state.investments
    c = st.session_state.currency
    st.markdown(f'<div class="section-heading">📋 ملخص البيانات</div>', unsafe_allow_html=True)
    for label, count in [
        (T("nav_expenses",lang), len(expenses)),
        (T("nav_savings",lang),  len(savings)),
        (T("nav_debts",lang),    len(debts)),
        (T("nav_goals",lang),    len(goals)),
        (T("nav_investments",lang), len(invs)),
    ]:
        st.markdown(f"""
        <div class="data-row">
          <div class="data-row-info"><div class="data-row-name">{label}</div></div>
          <div class="data-row-amount">{count}</div>
        </div>""", unsafe_allow_html=True)

render_bottom_nav()
