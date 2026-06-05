
import streamlit as st
from datetime import date
from modules.i18n import T

def render_savings():
    lang = st.session_state.get("lang", "ar")
    c = st.session_state.get("currency", "€")
    if "savings" not in st.session_state:
        st.session_state.savings = []

    st.markdown(f'<div class="section-heading">➕ {T("add_saving", lang)}</div>', unsafe_allow_html=True)
    with st.form("add_saving_form", clear_on_submit=True):
        name   = st.text_input(T("saving_name", lang))
        amount = st.number_input(T("saving_amount", lang), min_value=0.0, step=1.0)
        d      = st.date_input(T("saving_date", lang), value=date.today())
        submitted = st.form_submit_button(T("save", lang))
        if submitted and name and amount > 0:
            st.session_state.savings.append({"name": name, "amount": amount, "date": str(d)})
            st.success("✅ " + ("تم الحفظ" if lang == "ar" else "Saved"))
            st.rerun()

    items = st.session_state.savings
    if not items:
        st.markdown(f'<div style="text-align:center;color:#b0bac5;padding:24px;">{T("no_savings",lang)}</div>', unsafe_allow_html=True)
        return

    st.markdown(f'<div class="section-heading">🏦 {T("nav_savings",lang)}</div>', unsafe_allow_html=True)
    total = sum(s["amount"] for s in items)
    st.markdown(f'<div style="text-align:right;font-weight:800;color:#0b7a7f;font-size:1.1rem;margin-bottom:10px;">الإجمالي: {total:,.2f} {c}</div>', unsafe_allow_html=True)

    for i, s in enumerate(items):
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"""
            <div class="data-row">
              <div class="data-row-info">
                <div class="data-row-name">💰 {s['name']}</div>
                <div class="data-row-sub">{s['date']}</div>
              </div>
              <div class="data-row-amount">+{s['amount']:,.2f} {c}</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            if st.button("🗑️", key=f"del_sav_{i}"):
                st.session_state.savings.pop(i)
                st.rerun()
