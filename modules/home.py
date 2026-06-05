
import streamlit as st
from datetime import date
from modules.i18n import T

def _ring(percent: int) -> str:
    r = 36
    circ = 2 * 3.14159 * r
    offset = circ * (1 - percent / 100)
    return f"""
    <div class="ring-wrap">
      <svg viewBox="0 0 88 88">
        <circle class="ring-bg" cx="44" cy="44" r="{r}"/>
        <circle class="ring-fill" cx="44" cy="44" r="{r}"
          stroke-dasharray="{circ:.1f}"
          stroke-dashoffset="{offset:.1f}"/>
      </svg>
      <div class="ring-label">{percent}%</div>
    </div>"""

def _metric(icon, ic_cls, title, sub, value, trend, trend_cls="trend-up", pill=""):
    pill_html = f'<div class="metric-pill">{pill}</div>' if pill else ""
    return f"""
    <div class="metric-card">
      <div class="metric-icon {ic_cls}">{icon}</div>
      <div class="metric-mid">
        <div class="metric-title">{title}</div>
        <div class="metric-sub">{sub}</div>
        {pill_html}
      </div>
      <div class="metric-right">
        <div class="metric-val">{value}</div>
        <div class="{trend_cls}">{trend}</div>
      </div>
    </div>"""

def _smart_alerts(income, total_exp, total_debt, total_sav, lang):
    alerts = []
    if income == 0:
        alerts.append(("notif-yellow", T("tip_no_income", lang)))
    else:
        balance = income - total_exp
        if balance < 0:
            alerts.append(("notif-red", T("tip_balance_neg", lang)))
        save_rate = (total_sav / income * 100) if income > 0 else 0
        if save_rate < 10:
            alerts.append(("notif-yellow", T("tip_saverate_low", lang)))
        elif save_rate >= 20:
            alerts.append(("notif-green", T("tip_saverate_great", lang)))
        debt_ratio = (total_debt / income * 100) if income > 0 else 0
        if debt_ratio > 50:
            alerts.append(("notif-red", T("tip_debt_high", lang)))
        elif debt_ratio > 30:
            alerts.append(("notif-yellow", T("tip_debt_ok", lang)))
    return alerts

def render_home():
    lang = st.session_state.get("lang", "ar")
    c = st.session_state.get("currency", "€")
    income = st.session_state.get("income", 0)
    expenses_list = st.session_state.get("expenses", [])
    savings_list  = st.session_state.get("savings", [])
    debts_list    = st.session_state.get("debts", [])
    goals_list    = st.session_state.get("goals", [])
    invs_list     = st.session_state.get("investments", [])

    total_exp  = sum(e["amount"] for e in expenses_list)
    total_sav  = sum(s["amount"] for s in savings_list)
    total_debt = sum(d["total"] - d.get("paid", 0) for d in debts_list)
    total_inv  = sum(i["amount"] for i in invs_list)
    total_saved_goals = sum(g.get("saved", 0) for g in goals_list)
    remaining  = income - total_exp
    balance_pct = min(int((remaining / income * 100) if income > 0 else 0), 100)
    balance_pct = max(balance_pct, 0)

    name = st.session_state.get("user_name", "المستخدم")
    today = date.today()
    months_ar = ["يناير","فبراير","مارس","أبريل","مايو","يونيو",
                 "يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"]
    month_label = f"{months_ar[today.month-1]} {today.year}" if lang == "ar" else today.strftime("%B %Y")

    # ── Header ──────────────────────────────────────────────────────
    initial = name[0].upper() if name else "م"
    st.markdown(f"""
    <div class="top-header">
      <div class="avatar-chip">{initial}</div>
      <div class="user-meta">
        <div class="user-name">{name}</div>
        <div class="user-date">{month_label}</div>
      </div>
      <div class="notif-btn">🔔</div>
    </div>""", unsafe_allow_html=True)

    # ── Smart alerts ─────────────────────────────────────────────────
    alerts = _smart_alerts(income, total_exp, total_debt, total_sav, lang)
    for cls, msg in alerts[:2]:
        st.markdown(f'<div class="notif-alert {cls}">{msg}</div>', unsafe_allow_html=True)

    # ── Balance card ─────────────────────────────────────────────────
    st.markdown(f"""
    <div class="balance-card">
      <div class="balance-info">
        <div class="balance-label">{T('balance', lang)}</div>
        <div class="balance-value">{remaining:,.0f} {c}</div>
        <div class="balance-sub">من إجمالي {income:,.0f}{c}</div>
      </div>
      {_ring(balance_pct)}
    </div>""", unsafe_allow_html=True)

    # ── Metric cards ─────────────────────────────────────────────────
    exp_count = len(expenses_list)
    exp_trend_pct = 12
    sav_count = len(savings_list)
    goals_done = sum(1 for g in goals_list if g.get("saved", 0) >= g.get("target", 1))
    goals_pct  = int((goals_done / len(goals_list) * 100) if goals_list else 0)
    debt_count = len(debts_list)
    inv_return = 8.3

    html  = _metric("🧾","ic-purple", T("nav_expenses",lang),
                    f"{exp_count} {'معاملة' if lang=='ar' else 'transactions'}",
                    f"{total_exp:,.0f} {c}", f"↑ +{exp_trend_pct}%",
                    pill=f"{exp_count} {'مصاريف هذا الشهر' if lang=='ar' else 'this month'}")

    html += _metric("💰","ic-green", T("nav_savings",lang),
                    f"{sav_count} {'أوعية' if lang=='ar' else 'accounts'}",
                    f"{total_sav:,.0f} {c}", "↑ +8%")

    html += _metric("🎯","ic-yellow", T("nav_goals",lang),
                    f"{len(goals_list)} {'هدف' if lang=='ar' else 'goals'} — {goals_pct}% {'مكتمل' if lang=='ar' else 'done'}",
                    f"{goals_pct}%", "↑ جيد" if lang=="ar" else "↑ Good")

    html += _metric("💳","ic-red", T("nav_debts",lang),
                    f"{debt_count} {'قرض نشط' if lang=='ar' else 'active loans'}",
                    f"{total_debt:,.0f} {c}", "↓ -3%", "trend-down")

    html += _metric("📈","ic-blue", T("nav_investments",lang),
                    "محفظة نشطة" if lang=="ar" else "Active portfolio",
                    f"+{inv_return}%", "↑ ممتاز" if lang=="ar" else "↑ Excellent")

    st.markdown(html, unsafe_allow_html=True)
