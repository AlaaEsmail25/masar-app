
import streamlit as st
from datetime import date
from modules.i18n import T

PLATFORMS = {
    "Trade Republic":   {"logo": "TR", "url_register": "https://app.traderepublic.com/signup",     "url_login": "https://app.traderepublic.com/login"},
    "Scalable Capital": {"logo": "SC", "url_register": "https://de.scalable.capital/en/register",  "url_login": "https://de.scalable.capital/cockpit"},
    "Bitpanda":         {"logo": "BP", "url_register": "https://web.bitpanda.com/en/register",      "url_login": "https://web.bitpanda.com/user/login"},
    "DEGIRO":           {"logo": "DG", "url_register": "https://www.degiro.eu/register",            "url_login": "https://trader.degiro.nl/login/"},
}

def render_investments():
    lang = st.session_state.get("lang", "ar")
    c = st.session_state.get("currency", "€")
    if "investments" not in st.session_state:
        st.session_state.investments = []

    st.markdown(f'<div class="section-heading">🏦 {T("trusted_wallets", lang)}</div>', unsafe_allow_html=True)
    cols = st.columns(2)
    for idx, (pname, pdata) in enumerate(PLATFORMS.items()):
        with cols[idx % 2]:
            st.markdown(f"""
            <div class="data-row" style="flex-direction:column;gap:8px;align-items:center;text-align:center;">
              <div style="width:44px;height:44px;border-radius:12px;background:#0b7a7f;color:#fff;
                          display:flex;align-items:center;justify-content:center;font-weight:900;font-size:1rem;">
                {pdata['logo']}
              </div>
              <div style="font-weight:800;font-size:.95rem;color:#16202a;">{pname}</div>
              <div style="font-size:.75rem;color:#27a765;font-weight:700;">✅ {T('trusted_badge',lang)}</div>
            </div>""", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.link_button("📝 " + T("open_account", lang), pdata["url_register"], use_container_width=True)
            with c2:
                st.link_button("🔑 Login", pdata["url_login"], use_container_width=True)

    st.markdown(f'<div class="section-heading">➕ {T("record_inv", lang)}</div>', unsafe_allow_html=True)
    with st.form("add_inv_form", clear_on_submit=True):
        platform = st.selectbox(T("inv_platform", lang), list(PLATFORMS.keys()))
        amount   = st.number_input(T("inv_amount", lang), min_value=0.0, step=1.0)
        d        = st.date_input(T("inv_date", lang), value=date.today())
        note     = st.text_input(T("inv_note", lang), "")
        submitted = st.form_submit_button(T("inv_save", lang))
        if submitted and amount > 0:
            st.session_state.investments.append({"platform": platform, "amount": amount, "date": str(d), "note": note})
            st.success("✅ " + ("تم الحفظ" if lang == "ar" else "Saved"))
            st.rerun()

    items = st.session_state.investments
    if not items:
        st.markdown(f'<div style="text-align:center;color:#b0bac5;padding:24px;">{T("no_investments",lang)}</div>', unsafe_allow_html=True)
        return

    total = sum(i["amount"] for i in items)
    st.markdown(f'<div class="section-heading">📊 {T("inv_total",lang)}: <span style="color:#0b7a7f">{total:,.2f} {c}</span></div>', unsafe_allow_html=True)
    for i, inv in enumerate(items):
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"""
            <div class="data-row">
              <div class="data-row-info">
                <div class="data-row-name">📈 {inv['platform']}</div>
                <div class="data-row-sub">{inv['date']} {("— " + inv['note']) if inv.get('note') else ""}</div>
              </div>
              <div class="data-row-amount">{inv['amount']:,.2f} {c}</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            if st.button("🗑️", key=f"del_inv_{i}"):
                st.session_state.investments.pop(i)
                st.rerun()
