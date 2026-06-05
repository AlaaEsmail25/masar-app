
import streamlit as st
import json
from datetime import date
from modules.i18n import T

def render_reports():
    lang = st.session_state.get("lang", "ar")
    c = st.session_state.get("currency", "€")
    income    = st.session_state.get("income", 0)
    expenses  = st.session_state.get("expenses", [])
    savings   = st.session_state.get("savings", [])
    debts     = st.session_state.get("debts", [])
    goals     = st.session_state.get("goals", [])
    invs      = st.session_state.get("investments", [])

    total_exp  = sum(e["amount"] for e in expenses)
    total_sav  = sum(s["amount"] for s in savings)
    total_debt = sum(d["total"] - d.get("paid",0) for d in debts)
    total_inv  = sum(i["amount"] for i in invs)
    balance    = income - total_exp
    save_pct   = (total_sav / income * 100) if income > 0 else 0
    score = 100
    if income == 0: score = 0
    else:
        if balance < 0: score -= 40
        if save_pct < 10: score -= 20
        elif save_pct < 20: score -= 10
        if (total_debt / income * 100) > 50: score -= 30
        elif (total_debt / income * 100) > 30: score -= 15
    score = max(score, 0)
    if score >= 80: score_label, score_color = ("ممتاز 🏆" if lang=="ar" else "Excellent 🏆"), "#27a765"
    elif score >= 60: score_label, score_color = ("جيد 👍" if lang=="ar" else "Good 👍"), "#f0a500"
    else: score_label, score_color = ("يحتاج تحسين ⚠️" if lang=="ar" else "Needs Work ⚠️"), "#d46b6b"

    st.markdown(f'<div class="section-heading">📊 {T("nav_reports",lang)}</div>', unsafe_allow_html=True)

    # Health score card
    st.markdown(f"""
    <div style="background:#fff;border-radius:20px;padding:20px;text-align:center;box-shadow:0 8px 24px rgba(20,42,74,0.08);margin-bottom:14px;">
      <div style="font-size:.9rem;color:#7a8899;margin-bottom:8px;">{T('health_score',lang)}</div>
      <div style="font-size:3rem;font-weight:900;color:{score_color};">{score}</div>
      <div style="font-size:1rem;font-weight:700;color:{score_color};">{score_label}</div>
    </div>""", unsafe_allow_html=True)

    # KPI grid
    kpis = [
        ("💰", T("income",lang), f"{income:,.0f} {c}", "#e8fff3"),
        ("🧾", T("total_expenses",lang), f"{total_exp:,.0f} {c}", "#fff0f0"),
        ("🏦", T("total_savings",lang), f"{total_sav:,.0f} {c}", "#eef0ff"),
        ("💳", T("total_debts",lang), f"{total_debt:,.0f} {c}", "#fff8e1"),
        ("📈", T("nav_investments",lang), f"{total_inv:,.0f} {c}", "#dff3f1"),
        ("⚖️", T("balance",lang), f"{balance:,.0f} {c}", "#f4f7fc"),
    ]
    cols = st.columns(2)
    for idx, (icon, label, val, bg) in enumerate(kpis):
        with cols[idx % 2]:
            st.markdown(f"""
            <div style="background:{bg};border-radius:16px;padding:14px;text-align:center;margin-bottom:10px;">
              <div style="font-size:1.5rem;">{icon}</div>
              <div style="font-size:.8rem;color:#7a8899;margin:4px 0;">{label}</div>
              <div style="font-size:1.1rem;font-weight:800;color:#16202a;">{val}</div>
            </div>""", unsafe_allow_html=True)

    # Expenses by category
    if expenses:
        st.markdown(f'<div class="section-heading">🧾 {T("nav_expenses",lang)}</div>', unsafe_allow_html=True)
        cat_totals = {}
        for e in expenses:
            cat_totals[e["cat"]] = cat_totals.get(e["cat"], 0) + e["amount"]
        for cat, amt in sorted(cat_totals.items(), key=lambda x: -x[1]):
            pct = amt / total_exp * 100 if total_exp > 0 else 0
            st.markdown(f"""
            <div style="background:#fff;border-radius:12px;padding:10px 14px;margin-bottom:6px;box-shadow:0 2px 8px rgba(20,42,74,0.05);">
              <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                <span style="font-weight:700;font-size:.9rem;">{cat}</span>
                <span style="font-weight:800;color:#0b7a7f;">{amt:,.2f} {c} ({pct:.0f}%)</span>
              </div>
              <div class="prog-bar-wrap">
                <div class="prog-bar-fill" style="width:{pct:.0f}%;"></div>
              </div>
            </div>""", unsafe_allow_html=True)

    # Export JSON
    st.markdown(f'<div class="section-heading">📤 تصدير البيانات</div>', unsafe_allow_html=True)
    data_export = {
        "income": income, "currency": c,
        "expenses": expenses, "savings": savings,
        "debts": debts, "goals": goals, "investments": invs,
        "exported_at": str(date.today())
    }
    st.download_button(
        label="⬇️ تحميل البيانات (JSON)",
        data=json.dumps(data_export, ensure_ascii=False, indent=2),
        file_name=f"masar_report_{date.today()}.json",
        mime="application/json",
        use_container_width=True
    )
