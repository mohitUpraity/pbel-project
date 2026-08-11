import os
import streamlit as st
import plotly.graph_objects as go
from dotenv import load_dotenv

from app.ocr import extract_text_from_pdf, check_tesseract
from app.analyzer import analyze_legal_text, DEFAULT_MODEL, FALLBACK_MODELS
from app.sample_data import SAMPLE_ANALYSIS_DATA

load_dotenv()

st.set_page_config(
    page_title="LexAI — Legal Document Analyzer",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────────
# CLEAN PROFESSIONAL CSS (PROTECTS STREAMLIT ICON FONTS)
# ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background-color: #f8fafc !important;
    color: #0f172a !important;
}

/* IMPORTANT: Preserve Streamlit Material Icon Fonts to prevent text overlap (uploUpload, visibili) */
[data-testid="stIconMaterial"], 
[class*="stIcon"], 
.material-symbols-outlined, 
.material-icons {
    font-family: 'Material Symbols Outlined', 'Material Icons' !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
}
[data-testid="stSidebar"] hr {
    border-color: #e2e8f0 !important;
    margin: 14px 0 !important;
}

/* ── MAIN CONTAINER ── */
.block-container {
    background-color: #f8fafc !important;
    padding: 2rem 2.5rem !important;
    max-width: 1300px !important;
}

/* ── METRICS STRIP ── */
.metric-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 18px 20px 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.metric-label {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #64748b;
    margin-bottom: 6px;
}
.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.1;
}
.metric-sub {
    font-size: 0.78rem;
    color: #94a3b8;
    margin-top: 4px;
}

/* ── SECTION TITLE ── */
.section-title {
    font-size: 1rem;
    font-weight: 600;
    color: #0f172a;
    margin: 24px 0 12px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid #e2e8f0;
}

/* ── DOCUMENT OVERVIEW CARD ── */
.overview-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 20px 24px;
    margin-bottom: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.meta-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 12px;
    margin-bottom: 16px;
}
.meta-item {
    background: #f8fafc;
    border: 1px solid #f1f5f9;
    border-radius: 8px;
    padding: 10px 14px;
}
.meta-label {
    font-size: 0.67rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #94a3b8;
    margin-bottom: 3px;
}
.meta-value {
    font-size: 0.9rem;
    font-weight: 600;
    color: #0f172a;
    word-break: break-word;
}
.summary-box {
    background: #f8fafc;
    border-left: 3px solid #1d4ed8;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    font-size: 0.9rem;
    color: #334155;
    line-height: 1.65;
}
.parties-text {
    font-size: 0.88rem;
    color: #334155;
    margin-bottom: 12px;
}

/* ── SEVERITY PILLS ── */
.pill {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 50px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.4px;
    margin-right: 5px;
}
.pill-critical { background: #fef2f2; color: #dc2626; border: 1px solid #fca5a5; }
.pill-high     { background: #fff7ed; color: #ea580c; border: 1px solid #fdba74; }
.pill-medium   { background: #fefce8; color: #ca8a04; border: 1px solid #fde047; }
.pill-low      { background: #f0fdf4; color: #16a34a; border: 1px solid #86efac; }
.pill-category { background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; }
.pill-priority-immediate { background: #fef2f2; color: #dc2626; border: 1px solid #fca5a5; padding: 3px 10px; border-radius: 50px; font-size: 0.72rem; font-weight: 700; display: inline-block; }
.pill-priority-high      { background: #fff7ed; color: #ea580c; border: 1px solid #fdba74; padding: 3px 10px; border-radius: 50px; font-size: 0.72rem; font-weight: 700; display: inline-block; }
.pill-priority-medium    { background: #fefce8; color: #ca8a04; border: 1px solid #fde047; padding: 3px 10px; border-radius: 50px; font-size: 0.72rem; font-weight: 700; display: inline-block; }
.pill-priority-routine   { background: #f0fdf4; color: #16a34a; border: 1px solid #86efac; padding: 3px 10px; border-radius: 50px; font-size: 0.72rem; font-weight: 700; display: inline-block; }

.risk-rating-very-high { background: #fef2f2; color: #dc2626; border: 1px solid #fca5a5; padding: 4px 12px; border-radius: 6px; font-size: 0.76rem; font-weight: 700; display: inline-block; }
.risk-rating-high      { background: #fff7ed; color: #ea580c; border: 1px solid #fdba74; padding: 4px 12px; border-radius: 6px; font-size: 0.76rem; font-weight: 700; display: inline-block; }
.risk-rating-moderate  { background: #fefce8; color: #ca8a04; border: 1px solid #fde047; padding: 4px 12px; border-radius: 6px; font-size: 0.76rem; font-weight: 700; display: inline-block; }
.risk-rating-low       { background: #f0fdf4; color: #16a34a; border: 1px solid #86efac; padding: 4px 12px; border-radius: 6px; font-size: 0.76rem; font-weight: 700; display: inline-block; }

/* ── KEY TERM CARD ── */
.term-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-left: 4px solid #1d4ed8;
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    margin-bottom: 10px;
}
.term-title  { font-size: 0.95rem; font-weight: 700; color: #1d4ed8; margin-bottom: 3px; }
.term-loc    { font-size: 0.72rem; color: #64748b; background: #f1f5f9; border-radius: 4px; padding: 2px 8px; display: inline-block; margin-bottom: 8px; }
.term-def    { font-size: 0.88rem; color: #334155; line-height: 1.6; margin-bottom: 8px; }
.term-sig    { font-size: 0.83rem; color: #1d4ed8; border-left: 2px solid #bfdbfe; padding-left: 10px; }

/* ── RISK DETAILS ── */
.risk-desc { font-size: 0.88rem; color: #334155; line-height: 1.65; margin-bottom: 12px; }
.risk-clause-box {
    background: #f8fafc;
    border-left: 3px solid #cbd5e1;
    padding: 10px 14px;
    border-radius: 0 6px 6px 0;
    font-size: 0.83rem;
    font-style: italic;
    color: #64748b;
    line-height: 1.5;
    margin-bottom: 10px;
    font-family: 'Georgia', serif;
}
.risk-impact-box {
    background: #fef2f2;
    border: 1px solid #fecaca;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 0.84rem;
    color: #b91c1c;
    margin-bottom: 8px;
}
.risk-mitigation-box {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 6px;
    padding: 10px 14px;
}
.risk-mitigation-label { font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.6px; color: #16a34a; margin-bottom: 3px; }
.risk-mitigation-text  { font-size: 0.86rem; color: #166534; line-height: 1.5; }

/* ── ACTION CARD ── */
.action-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 10px;
}
.action-row {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 10px;
}
.action-title { font-size: 0.93rem; font-weight: 600; color: #0f172a; flex: 1; }
.action-deadline { background: #f8fafc; color: #64748b; border: 1px solid #e2e8f0; font-size: 0.76rem; font-weight: 600; padding: 3px 8px; border-radius: 5px; white-space: nowrap; }
.action-meta-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 10px; }
.action-meta-cell { background: #f8fafc; border-radius: 6px; padding: 8px 12px; }
.action-meta-label { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.6px; color: #94a3b8; font-weight: 600; margin-bottom: 2px; }
.action-meta-val   { font-size: 0.86rem; color: #334155; }
.action-consequence { font-size: 0.84rem; color: #64748b; border-left: 2px solid #e2e8f0; padding-left: 10px; line-height: 1.5; }

/* ── UPLOAD PAGE ── */
.upload-header {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 32px 28px;
    text-align: center;
    margin-bottom: 24px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.upload-title { font-size: 1.6rem; font-weight: 700; color: #0f172a; margin-bottom: 8px; }
.upload-sub   { font-size: 0.92rem; color: #64748b; max-width: 540px; margin: 0 auto; line-height: 1.6; }
.how-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 16px;
}
.how-num   { font-size: 1.5rem; font-weight: 800; color: #1d4ed8; margin-bottom: 6px; opacity: 0.5; }
.how-title { font-size: 0.88rem; font-weight: 700; color: #0f172a; margin-bottom: 4px; }
.how-desc  { font-size: 0.82rem; color: #64748b; line-height: 1.5; }

/* ── TAB STYLING ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 2px solid #e2e8f0 !important;
    gap: 0 !important;
    margin-bottom: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #64748b !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
    border-bottom: 2px solid transparent !important;
    margin-bottom: -2px !important;
    border-radius: 0 !important;
}
.stTabs [aria-selected="true"] {
    color: #1d4ed8 !important;
    border-bottom: 2px solid #1d4ed8 !important;
}

/* ── DIVIDERS ── */
hr { border-color: #e2e8f0 !important; margin: 20px 0 !important; }

/* ── EXPANDER STYLING ── */
div[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
    margin-bottom: 8px !important;
    overflow: hidden !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.03) !important;
}
div[data-testid="stExpander"] details { background: #ffffff !important; border: none !important; }
div[data-testid="stExpander"] summary {
    background: #ffffff !important;
    color: #0f172a !important;
    font-size: 0.92rem !important;
    font-weight: 600 !important;
    padding: 13px 18px !important;
    border-radius: 10px !important;
    outline: none !important;
}
div[data-testid="stExpander"] summary:hover { background: #f8fafc !important; color: #1d4ed8 !important; }
div[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    background: #ffffff !important;
    border-top: 1px solid #f1f5f9 !important;
    padding: 14px 18px !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────
def rating_class(r: str) -> str:
    r = r.lower()
    if "very high" in r: return "risk-rating-very-high"
    if "high" in r:       return "risk-rating-high"
    if "moderate" in r or "medium" in r: return "risk-rating-moderate"
    return "risk-rating-low"

def priority_pill(p: str) -> str:
    p = p.lower()
    if "immediate" in p: return "pill-priority-immediate"
    if "high" in p:       return "pill-priority-high"
    if "medium" in p:     return "pill-priority-medium"
    return "pill-priority-routine"

def sev_pill(s: str) -> str:
    return f"pill pill-{s.lower()}"

SEV_COLORS = {
    "Critical": "#dc2626",
    "High":     "#ea580c",
    "Medium":   "#ca8a04",
    "Low":      "#16a34a"
}

# ─────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────
for k, v in [("analysis_result", None), ("doc_name", None), ("processed", False)]:
    if k not in st.session_state:
        st.session_state[k] = v

def reset_analysis():
    st.session_state.analysis_result = None
    st.session_state.doc_name = None
    st.session_state.processed = False

# ─────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="background:#1d4ed8; margin:-1rem -1rem 0 -1rem; padding:20px 20px 18px; margin-bottom:20px;">
        <div style="font-size:1.4rem; font-weight:800; color:#ffffff; letter-spacing:-0.5px;">⚖️ LexAI</div>
        <div style="font-size:0.76rem; color:rgba(255,255,255,0.7); margin-top:2px;">Legal Document Analyzer</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**API Configuration**")
    custom_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="AIzaSy...",
        help="Reads from .env if blank"
    )

    st.markdown("---")
    st.markdown("**Model**")
    api_key_for_list = custom_key or os.getenv("GEMINI_API_KEY")
    available_models = [DEFAULT_MODEL] + FALLBACK_MODELS

    if api_key_for_list:
        try:
            from google import genai as _genai
            _client = _genai.Client(api_key=api_key_for_list)
            dynamic = [m.name.split('/')[-1] for m in _client.models.list() if hasattr(m, 'name')]
            if dynamic:
                unique = []
                if DEFAULT_MODEL in dynamic:
                    unique.append(DEFAULT_MODEL)
                for m in dynamic:
                    if m not in unique:
                        unique.append(m)
                available_models = unique
        except Exception:
            pass

    default_idx = next((i for i, m in enumerate(available_models) if m == DEFAULT_MODEL), 0)
    selected_model = st.selectbox("Model", available_models, index=default_idx, label_visibility="collapsed")

    st.markdown("---")
    tesseract_ok = check_tesseract()
    if tesseract_ok:
        st.success("Tesseract OCR ✓")
    else:
        st.warning("Tesseract OCR not found")

    st.markdown("---")
    st.markdown("<div style='font-size:0.73rem; color:#9ca3af;'>v2.2 · Powered by Google Gemini</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
# RESULTS VIEW
# ─────────────────────────────────────────────────────────────────────
if st.session_state.analysis_result:
    res  = st.session_state.analysis_result
    meta = res.get("document_metadata", {})
    risk_scores = res.get("risk_scores", {})
    all_risks   = res.get("risks", [])
    all_actions = res.get("action_items", [])
    all_terms   = res.get("key_terms", [])

    # ── Top Bar ──
    col_title, col_btn = st.columns([6, 1])
    with col_title:
        rc = rating_class(meta.get("overall_risk_rating", "Moderate Risk"))
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap; padding-bottom:4px;">
            <span style="font-size:1.3rem; font-weight:700; color:#0f172a;">{st.session_state.doc_name}</span>
            <span class="{rc}">{meta.get("overall_risk_rating","—").upper()}</span>
            <span style="background:#f1f5f9; color:#64748b; font-size:0.75rem; font-weight:600; padding:4px 10px; border-radius:5px; border:1px solid #e2e8f0;">{meta.get("document_type","Legal Agreement")}</span>
        </div>
        """, unsafe_allow_html=True)
    with col_btn:
        st.button("↩ New Analysis", on_click=reset_analysis, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── KPI Strip ──
    total_risks = len(all_risks)
    crit_c  = sum(1 for r in all_risks if r.get("severity") == "Critical")
    high_c  = sum(1 for r in all_risks if r.get("severity") == "High")
    imm_c   = sum(1 for a in all_actions if "immediate" in a.get("priority","").lower())
    score   = risk_scores.get("overall_score", 0)
    sc_col  = "#dc2626" if score >= 70 else "#ea580c" if score >= 40 else "#ca8a04" if score >= 20 else "#16a34a"

    c1, c2, c3, c4 = st.columns(4)
    for col, label, val, sub, color in [
        (c1, "Total Risks",   total_risks, f"{crit_c} critical · {high_c} high", "#dc2626"),
        (c2, "Risk Score",    f"{score}/100", "Composite severity index",        sc_col),
        (c3, "Action Items",  len(all_actions), f"{imm_c} need immediate action","#1d4ed8"),
        (c4, "Key Terms",     len(all_terms), "Clauses & definitions identified","#334155"),
    ]:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value" style="color:{color};">{val}</div>
                <div class="metric-sub">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── TABS ──
    tab_dash, tab_terms, tab_risks, tab_actions = st.tabs([
        "📊 Dashboard",
        "🔍 Key Terms",
        "⚠️ Risk Assessment",
        "📋 Action Items"
    ])

    # ══ DASHBOARD TAB ══
    with tab_dash:
        # Document Overview
        st.markdown('<div class="section-title">Document Overview</div>', unsafe_allow_html=True)
        parties_str = " · ".join(meta.get("parties", ["—"]))
        st.markdown(f"""
        <div class="overview-card">
            <div class="meta-grid">
                <div class="meta-item"><div class="meta-label">Document Title</div><div class="meta-value">{meta.get("title","—")}</div></div>
                <div class="meta-item"><div class="meta-label">Type</div><div class="meta-value">{meta.get("document_type","—")}</div></div>
                <div class="meta-item"><div class="meta-label">Execution Date</div><div class="meta-value">{meta.get("date","Not Specified")}</div></div>
                <div class="meta-item"><div class="meta-label">Term / Duration</div><div class="meta-value">{meta.get("term_duration","Not Specified")}</div></div>
                <div class="meta-item"><div class="meta-label">Governing Law</div><div class="meta-value">{meta.get("governing_law","Not Specified")}</div></div>
                <div class="meta-item"><div class="meta-label">Risk Rating</div><div class="meta-value"><span class="{rating_class(meta.get('overall_risk_rating','Moderate Risk'))}">{meta.get("overall_risk_rating","—")}</span></div></div>
            </div>
            <div style="font-size:0.7rem; font-weight:600; text-transform:uppercase; letter-spacing:0.6px; color:#94a3b8; margin-bottom:5px;">Parties</div>
            <div class="parties-text">{parties_str}</div>
            <div style="font-size:0.7rem; font-weight:600; text-transform:uppercase; letter-spacing:0.6px; color:#94a3b8; margin-bottom:6px;">Executive Summary</div>
            <div class="summary-box">{meta.get("summary","—")}</div>
        </div>
        """, unsafe_allow_html=True)

        # Charts
        st.markdown('<div class="section-title">Risk Analytics</div>', unsafe_allow_html=True)
        cc1, cc2, cc3 = st.columns(3)

        # Donut
        with cc1:
            sev_counts = risk_scores.get("severity_counts", {})
            labels = [k for k in ["Critical","High","Medium","Low"] if sev_counts.get(k, 0) > 0]
            values = [sev_counts[l] for l in labels]
            colors = [SEV_COLORS[l] for l in labels]
            if not values:
                labels, values, colors = ["No Risks"], [1], ["#e2e8f0"]

            fig = go.Figure(go.Pie(
                labels=labels, values=values, hole=0.58,
                marker=dict(colors=colors, line=dict(color="#ffffff", width=2)),
                textinfo="value+label",
                hovertemplate="%{label}: %{value}<extra></extra>"
            ))
            fig.update_layout(
                title=dict(text="Severity Breakdown", font=dict(size=13, color="#334155", family="Inter")),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#334155", family="Inter"),
                margin=dict(t=40, b=10, l=10, r=10), height=250,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)

        # Bar
        with cc2:
            cat_counts = risk_scores.get("category_counts", {})
            items = sorted(cat_counts.items(), key=lambda x: x[1], reverse=True)[:8]
            cats  = [x[0] for x in items]
            cnts  = [x[1] for x in items]
            if not cats:
                cats, cnts = ["None"], [0]

            fig2 = go.Figure(go.Bar(
                x=cnts, y=cats, orientation="h",
                marker_color="#1d4ed8",
                opacity=0.8,
                hovertemplate="%{y}: %{x}<extra></extra>"
            ))
            fig2.update_layout(
                title=dict(text="Risks by Category", font=dict(size=13, color="#334155", family="Inter")),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#334155", family="Inter"),
                margin=dict(t=40, b=10, l=10, r=10), height=250,
                xaxis=dict(gridcolor="#f1f5f9", tickfont=dict(size=10)),
                yaxis=dict(tickfont=dict(size=10))
            )
            st.plotly_chart(fig2, use_container_width=True)

        # Gauge
        with cc3:
            gauge_color = "#dc2626" if score >= 70 else "#ea580c" if score >= 40 else "#ca8a04" if score >= 20 else "#16a34a"
            fig3 = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                domain={"x": [0,1], "y": [0,1]},
                number={"font": {"size": 32, "color": gauge_color, "family": "Inter"}},
                gauge={
                    "axis": {"range": [0,100], "tickcolor": "#94a3b8", "tickfont": {"size":9}},
                    "bar":  {"color": gauge_color, "thickness": 0.25},
                    "bgcolor": "#f1f5f9",
                    "borderwidth": 0,
                    "steps": [
                        {"range": [0,20],   "color": "rgba(22,163,74,0.1)"},
                        {"range": [20,40],  "color": "rgba(202,138,4,0.1)"},
                        {"range": [40,70],  "color": "rgba(234,88,12,0.1)"},
                        {"range": [70,100], "color": "rgba(220,38,38,0.1)"},
                    ]
                }
            ))
            fig3.update_layout(
                title=dict(text="Overall Risk Score", font=dict(size=13, color="#334155", family="Inter")),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#334155", family="Inter"),
                margin=dict(t=40, b=10, l=20, r=20), height=250
            )
            st.plotly_chart(fig3, use_container_width=True)

    # ══ KEY TERMS TAB ══
    with tab_terms:
        st.markdown(f'<div class="section-title">Key Terms & Definitions <span style="font-weight:400; color:#94a3b8; font-size:0.85rem;">— {len(all_terms)} clauses extracted</span></div>', unsafe_allow_html=True)
        q = st.text_input("Search…", placeholder="Filter by keyword e.g. 'indemnification', 'termination'…", label_visibility="collapsed")
        filtered = [t for t in all_terms if not q
                    or q.lower() in t.get("term","").lower()
                    or q.lower() in t.get("definition","").lower()
                    or q.lower() in t.get("significance","").lower()]
        if not filtered:
            st.info("No terms match your search.")
        for t in filtered:
            sig = t.get("significance","")
            st.markdown(f"""
            <div class="term-card">
                <div class="term-title">{t.get("term","—")}</div>
                <div><span class="term-loc">§ {t.get("location","—")}</span></div>
                <div class="term-def">{t.get("definition","—")}</div>
                {f'<div class="term-sig">↳ {sig}</div>' if sig else ''}
            </div>
            """, unsafe_allow_html=True)

    # ══ RISK ASSESSMENT TAB ══
    with tab_risks:
        st.markdown(f'<div class="section-title">Risk Audit <span style="font-weight:400; color:#94a3b8; font-size:0.85rem;">— {len(all_risks)} risks identified</span></div>', unsafe_allow_html=True)

        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            sev_filter = st.selectbox("Severity", ["All","Critical","High","Medium","Low"])
        with fc2:
            all_cats = list(dict.fromkeys([r.get("category","Other") for r in all_risks]))
            cat_filter = st.selectbox("Category", ["All"] + all_cats)
        with fc3:
            sort_by = st.selectbox("Sort", ["Severity (Critical first)","Category","Risk ID"])

        filtered_risks = [r for r in all_risks
                          if (sev_filter == "All" or r.get("severity") == sev_filter)
                          and (cat_filter == "All" or r.get("category") == cat_filter)]

        sev_ord = {"Critical":0,"High":1,"Medium":2,"Low":3}
        if sort_by == "Severity (Critical first)":
            filtered_risks.sort(key=lambda r: sev_ord.get(r.get("severity","Low"), 9))
        elif sort_by == "Category":
            filtered_risks.sort(key=lambda r: r.get("category",""))
        else:
            filtered_risks.sort(key=lambda r: r.get("risk_id","R-999"))

        if not filtered_risks:
            st.info("No risks match the selected filters.")
        for risk in filtered_risks:
            sev  = risk.get("severity","Medium")
            rid  = risk.get("risk_id","")
            title = risk.get("title", risk.get("description","")[:60])
            prob  = risk.get("probability","—")
            impact = risk.get("impact","")
            clause = risk.get("clause","—")
            mitigation = risk.get("mitigation","—")
            cat   = risk.get("category","General")

            label = f"{rid}  {title}  [{sev}]"
            with st.expander(label, expanded=False):
                st.markdown(f"""
                <div>
                    <div style="display:flex; align-items:center; gap:7px; flex-wrap:wrap; margin-bottom:12px;">
                        <span class="{sev_pill(sev)}">{sev.upper()}</span>
                        <span class="pill pill-category">{cat.upper()}</span>
                        <span style="font-size:0.75rem; color:#94a3b8; background:#f8fafc; border:1px solid #e2e8f0; padding:3px 8px; border-radius:4px;">🎲 {prob} probability</span>
                    </div>
                    <div class="risk-desc">{risk.get("description","—")}</div>
                    <div style="font-size:0.68rem; font-weight:700; text-transform:uppercase; letter-spacing:0.6px; color:#94a3b8; margin-bottom:4px;">Relevant Clause</div>
                    <div class="risk-clause-box">"{clause}"</div>
                    {f'<div class="risk-impact-box">⚠ <strong>Impact:</strong> {impact}</div>' if impact else ''}
                    <div class="risk-mitigation-box">
                        <div class="risk-mitigation-label">✓ Recommended Action / Counter-Proposal</div>
                        <div class="risk-mitigation-text">{mitigation}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ══ ACTION ITEMS TAB ══
    with tab_actions:
        st.markdown(f'<div class="section-title">Obligations & Action Items <span style="font-weight:400; color:#94a3b8; font-size:0.85rem;">— {len(all_actions)} deliverables</span></div>', unsafe_allow_html=True)
        prio_ord = {"Immediate":0,"High":1,"Medium":2,"Routine":3}
        sorted_actions = sorted(all_actions, key=lambda a: prio_ord.get(a.get("priority","Routine"), 9))

        for idx, action in enumerate(sorted_actions):
            cb_key = f"cb_{idx}"
            done = st.session_state.get(cb_key, False)
            op   = "0.5" if done else "1"
            dec  = "line-through" if done else "none"
            p    = action.get("priority","Routine")
            aid  = action.get("action_id", f"A-{idx+1:03d}")

            st.markdown(f"""
            <div class="action-card" style="opacity:{op};">
                <div class="action-row">
                    <div class="action-title" style="text-decoration:{dec};">{aid} — {action.get("action","—")}</div>
                    <div style="display:flex; gap:6px; align-items:center;">
                        <span class="{priority_pill(p)}">{p.upper()}</span>
                        <span class="action-deadline">📅 {action.get("deadline","—")}</span>
                    </div>
                </div>
                <div class="action-meta-grid">
                    <div class="action-meta-cell">
                        <div class="action-meta-label">Responsible Party</div>
                        <div class="action-meta-val">{action.get("responsible_party","—")}</div>
                    </div>
                    <div class="action-meta-cell">
                        <div class="action-meta-label">Reference Clause</div>
                        <div class="action-meta-val">{action.get("reference_clause","—")}</div>
                    </div>
                </div>
                <div class="action-consequence"><strong>Consequence if missed:</strong> {action.get("significance","—")}</div>
            </div>
            """, unsafe_allow_html=True)
            st.checkbox("Mark complete", key=cb_key)

# ─────────────────────────────────────────────────────────────────────
# UPLOAD / HOME PAGE
# ─────────────────────────────────────────────────────────────────────
else:
    st.markdown("""
    <div class="upload-header">
        <div class="upload-title">⚖️ LexAI — Legal Document Analyzer</div>
        <div class="upload-sub">Upload any contract or legal agreement. Our AI performs clause-by-clause extraction, risk profiling, and obligation tracking — powered by Google Gemini.</div>
    </div>
    """, unsafe_allow_html=True)

    col_u1, col_u2 = st.columns([3, 1])
    with col_u1:
        st.subheader("Upload Document")
        uploaded_file = st.file_uploader(
            "Drop a PDF here",
            type=["pdf"],
            help="Native-text and scanned PDFs supported."
        )
        if uploaded_file:
            api_key_use = custom_key or os.getenv("GEMINI_API_KEY")
            if not api_key_use:
                st.error("Please add your Gemini API key in the sidebar to run analysis.")
            else:
                st.success(f"Loaded: **{uploaded_file.name}** ({round(uploaded_file.size/1024, 1)} KB)")
                pbar = st.progress(0.0)
                status = st.empty()

                def progress_cb(p, msg):
                    pbar.progress(p)
                    status.text(msg)

                try:
                    raw = uploaded_file.read()
                    status.text("Extracting text from pages…")
                    text = extract_text_from_pdf(raw, progress_cb)

                    if not text or len(text.strip()) < 50:
                        st.error("Could not extract readable text from this PDF.")
                        st.stop()

                    words = len(text.split())
                    pbar.progress(0.85)
                    status.text(f"Extracted {words:,} words — analyzing with Gemini…")

                    with st.spinner(f"Analyzing with {selected_model}…"):
                        data = analyze_legal_text(text, api_key_use, selected_model)

                    st.session_state.analysis_result = data
                    st.session_state.doc_name = uploaded_file.name
                    st.session_state.processed = True
                    pbar.progress(1.0)
                    status.success("Analysis complete!")
                    st.rerun()

                except Exception as e:
                    pbar.empty()
                    status.empty()
                    st.error(f"Analysis failed: {e}")
                    st.info("Check your API key and that the PDF has readable content.")

    with col_u2:
        st.subheader("Quick Demo")
        st.caption("No API key required. Load a pre-analyzed lease agreement.")
        if st.button("Load Sample Lease →", use_container_width=True):
            st.session_state.analysis_result = SAMPLE_ANALYSIS_DATA
            st.session_state.doc_name = "Apex_Vanguard_Lease.pdf"
            st.session_state.processed = True
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("**How It Works**")
    cols = st.columns(4)
    steps = [
        ("01", "Text Extraction", "PyMuPDF extracts native text. For scanned pages, Tesseract OCR renders and reads each page."),
        ("02", "AI Analysis", "Document is sent to Gemini with a detailed legal prompt. Output is a structured validated schema."),
        ("03", "Risk Profiling", "Every clause is classified by severity, category, probability, and paired with a counter-proposal."),
        ("04", "Dashboard", "Results appear in 4 tabs: overview + charts, key terms, risk audit, and obligation checklist."),
    ]
    for col, (num, title, desc) in zip(cols, steps):
        with col:
            st.markdown(f"""
            <div class="how-card">
                <div class="how-num">{num}</div>
                <div class="how-title">{title}</div>
                <div class="how-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
