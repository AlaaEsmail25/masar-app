
import streamlit as st
from datetime import date
from modules.i18n import T

def render_debts():
    lang = st.session_state.get("lang", "ar")
    c = st.session_state.get("currency", "€")
    if "debts" not in st.session_state:
        st.session_state.debts = []

    st.markdown(f'<div class="section-heading">➕ {T("add_debt", lang)}</div>', unsafe_allow_html=True)
    with st.form("add_debt_form", clear_on_submit=True):
        name    = st.text_input(T("debt_name", lang))
        total   = st.number_input(T("debt_total", lang), min_value=1.0, step=10.0)
        monthly = st.number_input(T("debt_monthly", lang), min_value=0.0, step=1.0)
        paid    = st.number_input(T("paid", lang), min_value=0.0, step=1.0)
        d       = st.date_input(T("debt_start", lang), value=date.today())
        submitted = st.form_submit_button(T("save", lang))
        if submitted and name and total > 0:
            st.session_state.debts.append({"name": name, "total": total, "monthly": monthly, "paid": paid, "start": str(d)})
            st.success("✅ " + ("تم الحفظ" if lang == "ar" else "Saved"))
            st.rerun()

    items = st.session_state.debts
    if not items:
        st.markdown(f'<div style="text-align:center;color:#b0bac5;padding:24px;">{T("no_debts",lang)}</div>', unsafe_allow_html=True)
        return

    st.markdown(f'<div class="section-heading">💳 {T("nav_debts",lang)}</div>', unsafe_allow_html=True)
    for i, d in enumerate(items):
        remaining = d["total"] - d.get("paid", 0)
        pct = min(int(d.get("paid", 0) / d["total"] * 100), 100)
        months_left = int(remaining / d["monthly"]) if d.get("monthly", 0) > 0 else 0
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"""
            <div class="data-row" style="flex-direction:column;align-items:flex-start;gap:8px;">
              <div style="display:flex;justify-content:space-between;width:100%;">
                <div class="data-row-name">💳 {d['name']}</div>
                <div class="data-row-amount" style="color:#d46b6b;">{remaining:,.0f} {c}</div>
              </div>
              <div class="prog-bar-wrap" style="width:100%;">
                <div class="prog-bar-fill" style="width:{pct}%;background:#27a765;"></div>
              </div>
              <div style="display:flex;justify-content:space-between;width:100%;font-size:.8rem;color:#7a8899;">
                <span>✅ {T('paid',lang)}: {d.get('paid',0):,.0f} {c}</span>
                <span>📅 ~{months_left} {T('months',lang)}</span>
              </div>
            </div>""", unsafe_allow_html=True)
        with col2:
            if st.button("🗑️", key=f"del_debt_{i}"):
                st.session_state.debts.pop(i)
                st.rerun()
