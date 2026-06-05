
import streamlit as st
from datetime import date
from modules.i18n import T

def render_goals():
    lang = st.session_state.get("lang", "ar")
    c = st.session_state.get("currency", "€")
    if "goals" not in st.session_state:
        st.session_state.goals = []

    st.markdown(f'<div class="section-heading">➕ {T("add_goal", lang)}</div>', unsafe_allow_html=True)
    with st.form("add_goal_form", clear_on_submit=True):
        name    = st.text_input(T("goal_name", lang))
        target  = st.number_input(T("goal_target", lang), min_value=1.0, step=10.0)
        saved   = st.number_input(T("goal_saved", lang), min_value=0.0, step=1.0)
        dead    = st.date_input(T("goal_deadline", lang), value=date.today())
        submitted = st.form_submit_button(T("save", lang))
        if submitted and name and target > 0:
            st.session_state.goals.append({"name": name, "target": target, "saved": saved, "deadline": str(dead)})
            st.success("✅ " + ("تم الحفظ" if lang == "ar" else "Saved"))
            st.rerun()

    items = st.session_state.goals
    if not items:
        st.markdown(f'<div style="text-align:center;color:#b0bac5;padding:24px;">{T("no_goals",lang)}</div>', unsafe_allow_html=True)
        return

    st.markdown(f'<div class="section-heading">🎯 {T("nav_goals",lang)}</div>', unsafe_allow_html=True)
    for i, g in enumerate(items):
        pct = min(int(g["saved"] / g["target"] * 100), 100) if g["target"] > 0 else 0
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"""
            <div class="data-row" style="flex-direction:column;align-items:flex-start;gap:8px;">
              <div style="display:flex;justify-content:space-between;width:100%;">
                <div class="data-row-name">🎯 {g['name']}</div>
                <div class="data-row-amount">{pct}%</div>
              </div>
              <div class="prog-bar-wrap" style="width:100%;">
                <div class="prog-bar-fill" style="width:{pct}%;"></div>
              </div>
              <div style="display:flex;justify-content:space-between;width:100%;font-size:.8rem;color:#7a8899;">
                <span>{g['saved']:,.0f} {c} / {g['target']:,.0f} {c}</span>
                <span>📅 {g['deadline']}</span>
              </div>
            </div>""", unsafe_allow_html=True)
        with col2:
            if st.button("🗑️", key=f"del_goal_{i}"):
                st.session_state.goals.pop(i)
                st.rerun()
