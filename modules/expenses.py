
import streamlit as st
from datetime import date
from modules.i18n import T, CATEGORIES

def render_expenses():
    lang = st.session_state.get("lang", "ar")
    c = st.session_state.get("currency", "€")
    if "expenses" not in st.session_state:
        st.session_state.expenses = []

    cats = CATEGORIES.get(lang, CATEGORIES["ar"])

    st.markdown(f'<div class="section-heading">➕ {T("add_expense", lang)}</div>', unsafe_allow_html=True)
    with st.form("add_expense_form", clear_on_submit=True):
        name = st.text_input(T("expense_name", lang))
        cat  = st.selectbox(T("expense_cat", lang), cats)
        amount = st.number_input(T("expense_amount", lang), min_value=0.0, step=1.0)
        d = st.date_input(T("expense_date", lang), value=date.today())
        submitted = st.form_submit_button(T("save", lang))
        if submitted and name and amount > 0:
            st.session_state.expenses.append({"name": name, "cat": cat, "amount": amount, "date": str(d)})
            st.success("✅ " + ("تم الحفظ" if lang == "ar" else "Saved"))
            st.rerun()

    items = st.session_state.expenses
    if not items:
        st.markdown(f'<div style="text-align:center;color:#b0bac5;padding:24px;">{T("no_expenses",lang)}</div>', unsafe_allow_html=True)
        return

    st.markdown(f'<div class="section-heading">📋 {T("nav_expenses",lang)}</div>', unsafe_allow_html=True)
    total = sum(e["amount"] for e in items)
    st.markdown(f'<div style="text-align:right;font-weight:800;color:#0b7a7f;font-size:1.1rem;margin-bottom:10px;">الإجمالي: {total:,.2f} {c}</div>', unsafe_allow_html=True)

    for i, e in enumerate(items):
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"""
            <div class="data-row">
              <div class="data-row-info">
                <div class="data-row-name">{e['cat']} — {e['name']}</div>
                <div class="data-row-sub">{e['date']}</div>
              </div>
              <div class="data-row-amount">-{e['amount']:,.2f} {c}</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            if st.button("🗑️", key=f"del_exp_{i}"):
                st.session_state.expenses.pop(i)
                st.rerun()
