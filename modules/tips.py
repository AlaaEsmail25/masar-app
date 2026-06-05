
import streamlit as st
import os
import requests
from math import pow
from modules.i18n import T

def _ask_groq(question: str, lang: str) -> str:
    api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))
    model   = st.secrets.get("GROQ_MODEL",   os.getenv("GROQ_MODEL",   "llama-3.1-8b-instant"))

    income    = st.session_state.get("income", 0)
    total_exp = sum(e["amount"] for e in st.session_state.get("expenses", []))
    total_sav = sum(s["amount"] for s in st.session_state.get("savings", []))
    total_debt= sum(d["total"]  for d in st.session_state.get("debts", []))
    total_inv = sum(i["amount"] for i in st.session_state.get("investments", []))
    c         = st.session_state.get("currency", "€")
    name      = st.session_state.get("user_name", "المستخدم")

    ctx = f"""
اسم المستخدم: {name}
الدخل الشهري: {income:,.0f} {c}
إجمالي المصاريف: {total_exp:,.0f} {c}
الرصيد المتبقي: {income - total_exp:,.0f} {c}
المدخرات: {total_sav:,.0f} {c}
الديون: {total_debt:,.0f} {c}
الاستثمارات: {total_inv:,.0f} {c}
"""
    system_prompt = f"""أنت مستشار مالي شخصي ضمن تطبيق "مسار".
أجب بالعربية (أو بلغة السؤال إن كانت إنجليزية أو ألمانية).
استخدم الأرقام التالية لتخصيص النصيحة:
{ctx}
القواعد:
- اقترح خطوات عملية قصيرة قابلة للتنفيذ.
- لا تعد بعوائد استثمارية محددة.
- إذا كان السؤال عاماً، أعط 3 نصائح عملية فورية.
- كن مشجعاً وإيجابياً."""

    if not api_key:
        remaining = income - total_exp
        if lang == "ar":
            return (f"💡 نصيحة سريعة بناءً على أرقامك:\n\n"
                    f"رصيدك المتاح {remaining:,.0f} {c}. "
                    f"{'احرص على توزيعه: 50% ضروريات، 30% رغبات، 20% ادخار.' if remaining > 0 else 'مصاريفك تتجاوز دخلك — راجع بنود الإنفاق الكبيرة أولاً.'}\n\n"
                    f"لتفعيل المساعد الذكي الكامل، أضف مفتاح Groq في `.streamlit/secrets.toml`")
        return f"💡 Quick tip: Balance is {remaining:,.0f} {c}. To enable full AI, add Groq API key in `.streamlit/secrets.toml`"

    try:
        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": model, "temperature": 0.4,
                  "messages": [{"role": "system", "content": system_prompt},
                                {"role": "user",   "content": question}]},
            timeout=45
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ {'تعذر الاتصال' if lang=='ar' else 'Connection error'}: {e}"

def render_tips():
    lang = st.session_state.get("lang", "ar")
    c    = st.session_state.get("currency", "€")
    income    = st.session_state.get("income", 0)
    total_exp = sum(e["amount"] for e in st.session_state.get("expenses", []))
    total_sav = sum(s["amount"] for s in st.session_state.get("savings", []))
    total_debt= sum(d["total"]  for d in st.session_state.get("debts",   []))
    total_inv = sum(i["amount"] for i in st.session_state.get("investments", []))

    # ── AI Header ───────────────────────────────────────────────────
    st.markdown(f"""
    <div class="ai-header">
      <div class="ai-title">🤖 {T('ai_assistant', lang)}</div>
      <div class="ai-sub">{T('ai_no_key', lang)}</div>
    </div>""", unsafe_allow_html=True)

    # ── Chat ────────────────────────────────────────────────────────
    if "chat_messages" not in st.session_state:
        welcome = "مرحباً! أنا مساعدك المالي. اسألني عن ادخارك، مصاريفك، أو خطة استثمارية."
        st.session_state.chat_messages = [{"role": "assistant", "content": welcome}]

    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    prompt = st.chat_input(T("ai_placeholder", lang))
    if prompt:
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            with st.spinner(T("ai_thinking", lang)):
                answer = _ask_groq(prompt, lang)
            st.write(answer)
        st.session_state.chat_messages.append({"role": "assistant", "content": answer})

    # ── Smart Tips ──────────────────────────────────────────────────
    st.markdown(f'<div class="section-heading">{T("smart_tips", lang)}</div>', unsafe_allow_html=True)
    if income == 0:
        st.info(T("tip_no_income", lang))
    else:
        balance    = income - total_exp
        save_rate  = (total_sav / income * 100)
        debt_ratio = (total_debt / income * 100)
        if balance < 0:
            st.error(T("tip_balance_neg", lang))
        if save_rate < 10:
            st.warning(T("tip_saverate_low", lang))
        elif save_rate < 20:
            st.info(T("tip_saverate_ok", lang))
        else:
            st.success(T("tip_saverate_great", lang))
        if debt_ratio > 50:
            st.error(T("tip_debt_high", lang))
        elif debt_ratio > 30:
            st.warning(T("tip_debt_ok", lang))
        else:
            st.success(T("tip_debt_safe", lang))
        if total_inv == 0:
            st.info(T("tip_no_invest", lang))
        if balance >= 0 and save_rate >= 20 and debt_ratio <= 30:
            st.success(T("tip_great", lang))

    # ── 50/30/20 Budget Rule ────────────────────────────────────────
    st.markdown(f'<div class="section-heading">{T("budget_rule", lang)}</div>', unsafe_allow_html=True)
    if income > 0:
        n50 = income * 0.5; n30 = income * 0.3; n20 = income * 0.2
        for label, pct, val, col in [
            (T("budget_needs", lang), total_exp / n50 * 100 if n50 else 0, f"{total_exp:,.0f}/{n50:,.0f} {c}", "#e8fff3"),
            (T("budget_wants", lang), 50, f"{n30:,.0f} {c}", "#fff8e1"),
            (T("budget_save",  lang), total_sav / n20 * 100 if n20 else 0, f"{total_sav:,.0f}/{n20:,.0f} {c}", "#eef0ff"),
        ]:
            pct_clamped = min(pct, 100)
            st.markdown(f"""
            <div style="background:{col};border-radius:14px;padding:12px 14px;margin-bottom:8px;">
              <div style="display:flex;justify-content:space-between;font-weight:700;font-size:.95rem;margin-bottom:6px;">
                <span>{label}</span><span>{val}</span>
              </div>
              <div class="prog-bar-wrap">
                <div class="prog-bar-fill" style="width:{pct_clamped:.0f}%;"></div>
              </div>
            </div>""", unsafe_allow_html=True)

    # ── ETF Calculator ──────────────────────────────────────────────
    st.markdown(f'<div class="section-heading">{T("etf_calc", lang)}</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        monthly_etf = st.number_input(T("etf_monthly", lang), min_value=0.0, value=100.0, step=10.0)
        years       = st.slider(T("etf_years", lang), 1, 40, 10)
    with col2:
        rate        = st.slider(T("etf_rate", lang), 1.0, 15.0, 7.0, 0.1)

    n          = years * 12
    r          = rate / 100 / 12
    total_etf  = monthly_etf * ((pow(1 + r, n) - 1) / r) * (1 + r) if r > 0 else monthly_etf * n
    deposited  = monthly_etf * n
    profit     = total_etf - deposited
    st.markdown(f"""
    <div style="background:#dff3f1;border-radius:16px;padding:16px;margin-top:8px;">
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;text-align:center;">
        <div>
          <div style="font-size:.8rem;color:#7a8899;">{T('etf_deposited',lang)}</div>
          <div style="font-size:1.1rem;font-weight:800;color:#16202a;">{deposited:,.0f} {c}</div>
        </div>
        <div>
          <div style="font-size:.8rem;color:#7a8899;">{T('etf_profit',lang)}</div>
          <div style="font-size:1.1rem;font-weight:800;color:#27a765;">+{profit:,.0f} {c}</div>
        </div>
        <div>
          <div style="font-size:.8rem;color:#7a8899;">{T('etf_total',lang)}</div>
          <div style="font-size:1.1rem;font-weight:800;color:#0b7a7f;">{total_etf:,.0f} {c}</div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)
