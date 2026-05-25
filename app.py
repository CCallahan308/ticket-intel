"""
Ticket Intel - Production-Grade Portfolio Demo
Design System: Clean, professional, business-intelligence aesthetic
"""

import time

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from src.models.router import load_router, route
from src.models.summarizer import summarize
from src.models.insights import extract_entities, extract_keywords, detect_sentiment
from src.models.evaluate import evaluate

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Ticket Intel | Christian Callahan", page_icon="🎫", layout="wide"
)

# ═══════════════════════════════════════════════════════════════════════════
# DESIGN SYSTEM
# ═══════════════════════════════════════════════════════════════════════════

st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --color-bg-primary: #0a0a0b;
        --color-bg-secondary: #111113;
        --color-bg-tertiary: #18181b;
        --color-border: #27272a;
        --color-border-subtle: #1f1f23;
        --color-text-primary: #fafafa;
        --color-text-secondary: #a1a1aa;
        --color-text-tertiary: #71717a;
        --color-accent-primary: #14b8a6;
        --color-accent-secondary: #2dd4bf;
        --color-success: #10b981;
        --color-warning: #f59e0b;
        --color-danger: #ef4444;
        --color-info: #3b82f6;
        --font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        --radius-sm: 6px;
        --radius-md: 10px;
        --radius-lg: 14px;
    }
    
    html, body, [class*="css"] {
        font-family: var(--font-family);
        color: var(--color-text-primary);
        background: var(--color-bg-primary);
    }
    
    .main { padding: 0; }
    .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
    }
    
    /* Header */
    .app-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 3rem;
        padding-bottom: 2rem;
        border-bottom: 1px solid var(--color-border-subtle);
    }
    
    .app-title {
        font-size: 1.875rem;
        font-weight: 600;
        letter-spacing: -0.025em;
        margin: 0 0 0.5rem 0;
    }
    
    .app-subtitle {
        font-size: 1rem;
        color: var(--color-text-secondary);
        margin: 0 0 1.25rem 0;
        line-height: 1.6;
    }
    
    .app-meta {
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    
    .meta-item {
        display: flex;
        align-items: center;
        gap: 0.375rem;
        font-size: 0.8125rem;
        color: var(--color-text-tertiary);
    }
    
    .meta-item a {
        color: var(--color-accent-secondary);
        text-decoration: none;
        font-weight: 500;
    }
    
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.375rem;
        padding: 0.375rem 0.875rem;
        background: rgba(20, 184, 166, 0.1);
        border: 1px solid rgba(20, 184, 166, 0.2);
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 500;
        color: var(--color-accent-primary);
    }
    
    /* Metrics Grid */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 2.5rem;
    }
    
    .metric-card {
        background: var(--color-bg-secondary);
        border: 1px solid var(--color-border-subtle);
        border-radius: var(--radius-md);
        padding: 1.5rem;
        transition: border-color 250ms ease;
    }
    
    .metric-card:hover {
        border-color: var(--color-border);
    }
    
    .metric-label {
        font-size: 0.75rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--color-text-tertiary);
        margin-bottom: 0.75rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 600;
        color: var(--color-text-primary);
        margin-bottom: 0.375rem;
    }
    
    .metric-change {
        font-size: 0.8125rem;
        color: var(--color-text-tertiary);
    }
    
    /* Sections */
    .section {
        margin-bottom: 2.5rem;
    }
    
    .section-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1.5rem;
    }
    
    .section-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: var(--color-text-primary);
        margin: 0;
    }
    
    .section-subtitle {
        font-size: 0.875rem;
        color: var(--color-text-tertiary);
        margin-top: 0.25rem;
    }
    
    .section-divider {
        height: 1px;
        background: var(--color-border-subtle);
        margin: 2.5rem 0;
    }
    
    /* Cards */
    .card {
        background: var(--color-bg-secondary);
        border: 1px solid var(--color-border-subtle);
        border-radius: var(--radius-md);
        padding: 1.5rem;
    }
    
    .card-header {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--color-text-primary);
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid var(--color-border-subtle);
    }
    
    /* Result Tags */
    .result-tag {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .tag-refund { background: rgba(239, 68, 68, 0.1); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.2); }
    .tag-technical { background: rgba(168, 85, 247, 0.1); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.2); }
    .tag-cancellation { background: rgba(249, 115, 22, 0.1); color: #fb923c; border: 1px solid rgba(249, 115, 22, 0.2); }
    .tag-product { background: rgba(59, 130, 246, 0.1); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.2); }
    .tag-billing { background: rgba(16, 185, 129, 0.1); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.2); }
    
    /* Analysis Results */
    .result-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .result-metric {
        text-align: center;
        padding: 1.25rem;
        background: var(--color-bg-tertiary);
        border-radius: var(--radius-sm);
        border: 1px solid var(--color-border-subtle);
    }
    
    .result-metric .label {
        font-size: 0.6875rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--color-text-tertiary);
        margin-bottom: 0.5rem;
    }
    
    .result-metric .value {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--color-text-primary);
    }
    
    /* Entity Pills */
    .entity-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.375rem;
        padding: 0.375rem 0.75rem;
        background: var(--color-bg-tertiary);
        border: 1px solid var(--color-border-subtle);
        border-radius: var(--radius-sm);
        font-size: 0.75rem;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .entity-type {
        color: var(--color-accent-secondary);
        font-weight: 500;
    }
    
    /* Footer */
    .app-footer {
        margin-top: 4rem;
        padding-top: 2rem;
        border-top: 1px solid var(--color-border-subtle);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .footer-left {
        font-size: 0.8125rem;
        color: var(--color-text-tertiary);
    }
    
    .footer-links {
        display: flex;
        gap: 1.5rem;
    }
    
    .footer-links a {
        font-size: 0.8125rem;
        color: var(--color-text-secondary);
        text-decoration: none;
        font-weight: 500;
    }
    
    .footer-links a:hover {
        color: var(--color-accent-secondary);
    }
    
    /* Streamlit Overrides */
    .stMetric { background: transparent !important; }
    .stMetric > div { padding: 0 !important; background: transparent !important; border: none !important; }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.75rem 1.5rem;
        background: var(--color-bg-secondary);
        border: 1px solid var(--color-border-subtle);
        border-radius: var(--radius-sm) var(--radius-sm) 0 0;
        color: var(--color-text-secondary);
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--color-bg-tertiary);
        border-bottom: 2px solid var(--color-accent-primary);
        color: var(--color-text-primary);
    }
    
    .stButton > button {
        background: var(--color-accent-primary) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 500 !important;
        width: 100%;
    }
    
    .stDataFrame {
        border: 1px solid var(--color-border-subtle);
        border-radius: var(--radius-sm);
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""",
    unsafe_allow_html=True,
)

# ═══════════════════════════════════════════════════════════════════════════
# DATA & MODELS
# ═══════════════════════════════════════════════════════════════════════════


@st.cache_resource
def load_model():
    """Load (or train, on first run) the real TF-IDF + Naive Bayes router."""
    return load_router()


@st.cache_data
def load_metrics():
    """Real cross-validated metrics on the synthetic demo data."""
    return evaluate()


pipe, _l2i, i2l = load_model()

SAMPLE_TICKETS = [
    {
        "subject": "Need refund for duplicate charge",
        "body": "I was charged twice for my subscription this month. Please refund the duplicate charge to my card.",
    },
    {
        "subject": "App crashes on startup",
        "body": "Every time I open the app, it crashes immediately. I've tried reinstalling but the issue persists. Running iOS 17.",
    },
    {
        "subject": "How do I export my data?",
        "body": "I need to export all my project data to CSV. Is there a way to do this in bulk or do I have to export each project individually?",
    },
    {
        "subject": "Cancel my subscription",
        "body": "Please cancel my Pro subscription effective immediately. I no longer need the service.",
    },
    {
        "subject": "Question about annual pricing",
        "body": "I see you offer monthly plans but I'm interested in annual billing. Do you offer any discount for paying yearly?",
    },
]

# Map the model's real category labels to the CSS tag styles.
_TAG_CLASSES = {
    "Bug": "tag-technical",
    "Performance": "tag-cancellation",
    "Billing": "tag-billing",
    "Account": "tag-product",
    "Feature Request": "tag-refund",
    "General": "tag-product",
}


def classify_ticket(text: str) -> tuple[str, float]:
    """Route a ticket with the real trained pipeline."""
    category, confidence, _ = route(text, pipe, i2l)
    return category, confidence


def analyze_entities(text: str) -> list[tuple[str, str]]:
    """Adapt the model's entity dicts to (type, value) tuples for rendering."""
    return [(e["type"], e["text"]) for e in extract_entities(text)]


def get_tag_class(category: str) -> str:
    return _TAG_CLASSES.get(category, "tag-product")


# ═══════════════════════════════════════════════════════════════════════════
# UI COMPONENTS
# ═══════════════════════════════════════════════════════════════════════════


def render_header():
    metrics = load_metrics()
    acc = metrics["model"]["accuracy"]
    st.markdown(
        f"""
    <div class="app-header">
        <div>
            <h1 class="app-title">Ticket Intelligence System</h1>
            <p class="app-subtitle">
                Ticket classification, extractive summarization, and entity
                extraction powered by a TF-IDF + Naive Bayes pipeline.
            </p>
            <div class="app-meta">
                <div class="meta-item">
                    <a href="https://github.com/CCallahan308/ticket-intel">View Source</a>
                </div>
                <div class="meta-item">•</div>
                <div class="meta-item">TF-IDF + Naive Bayes</div>
                <div class="meta-item">•</div>
                <div class="meta-item">{acc:.0%} CV accuracy on synthetic demo data</div>
            </div>
        </div>
        <div class="status-badge">Demo · synthetic data</div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_tabs():
    tab1, tab2, tab3 = st.tabs(["Single Ticket", "Batch Analysis", "Performance"])

    with tab1:
        render_single_ticket()

    with tab2:
        render_batch_analysis()

    with tab3:
        render_performance()


def render_single_ticket():
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(
            """
        <div class="section">
            <h3 class="section-title">Input</h3>
            <p class="section-subtitle">Enter a support ticket to analyze</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        sample_idx = st.selectbox(
            "Sample tickets",
            range(len(SAMPLE_TICKETS)),
            format_func=lambda i: SAMPLE_TICKETS[i]["subject"],
            label_visibility="collapsed",
        )

        subject = st.text_input("Subject", value=SAMPLE_TICKETS[sample_idx]["subject"])
        body = st.text_area(
            "Body", value=SAMPLE_TICKETS[sample_idx]["body"], height=150
        )

        analyze = st.button("Analyze Ticket", type="primary")

    with col2:
        st.markdown(
            """
        <div class="section">
            <h3 class="section-title">Results</h3>
            <p class="section-subtitle">Classification and extraction</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if analyze or subject:
            full_text = f"{subject} {body}"
            category, confidence = classify_ticket(full_text)
            summary, _ = summarize(body)
            entities = analyze_entities(full_text)
            sentiment = detect_sentiment(full_text)
            keywords = extract_keywords(full_text)

            # Classification results
            st.markdown(
                f"""
            <div class="result-grid">
                <div class="result-metric">
                    <div class="label">Category</div>
                    <div class="value"><span class="result-tag {get_tag_class(category)}">{category}</span></div>
                </div>
                <div class="result-metric">
                    <div class="label">Confidence</div>
                    <div class="value">{confidence:.0%}</div>
                </div>
                <div class="result-metric">
                    <div class="label">Sentiment</div>
                    <div class="value" style="color: {"#ef4444" if sentiment == "negative" else "#10b981" if sentiment == "positive" else "#71717a"};">{sentiment.title()}</div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

            # Summary
            st.markdown("**Summary**")
            st.info(summary or "No summary generated")

            # Entities
            if entities:
                st.markdown("**Entities**")
                entity_html = "".join(
                    [
                        f'<span class="entity-pill"><span class="entity-type">{t}:</span> {v}</span>'
                        for t, v in entities
                    ]
                )
                st.markdown(entity_html, unsafe_allow_html=True)

            # Keywords
            st.markdown("**Keywords**")
            st.markdown(" · ".join([f"`{kw}`" for kw in keywords]))


@st.cache_data
def generate_batch_data(n=150):
    np.random.seed(42)

    templates = [
        (
            "Refund for order #{order_id}",
            "Charged incorrectly for order #{order_id}. Amount was ${amount}.",
        ),
        ("App crashes on {device}", "The app keeps crashing on my {device}."),
        ("How to {action}?", "Trying to {action} but can't find option."),
        ("Cancel subscription", "Cancel my subscription effective immediately."),
        (
            "Billing question ${amount}",
            "Question about ${amount} charge on my statement.",
        ),
    ]

    tickets = []
    for _ in range(n):
        subj_tpl, body_tpl = templates[np.random.randint(0, len(templates))]

        subj = subj_tpl.format(
            order_id=np.random.randint(100000, 999999),
            device=np.random.choice(["iPhone", "Android", "Windows"]),
            action=np.random.choice(
                ["export data", "change password", "update billing"]
            ),
            amount=np.random.choice([9.99, 19.99, 29.99, 49.99]),
        )

        body = body_tpl.format(
            order_id=np.random.randint(100000, 999999),
            device=np.random.choice(["iPhone", "Android", "Windows"]),
            action=np.random.choice(
                ["export data", "change password", "update billing"]
            ),
            amount=np.random.choice([9.99, 19.99, 29.99, 49.99]),
        )

        full = f"{subj} {body}"
        cat, conf = classify_ticket(full)
        sent = detect_sentiment(full)

        tickets.append(
            {
                "subject": subj,
                "category": cat,
                "confidence": conf,
                "sentiment": sent,
                "body": body[:80] + "...",
            }
        )

    return pd.DataFrame(tickets)


def render_batch_analysis():
    df = generate_batch_data()

    # KPIs
    st.markdown('<div class="metrics-grid">', unsafe_allow_html=True)

    kpis = [
        ("Total Tickets", f"{len(df):,}"),
        ("Avg Confidence", f"{df['confidence'].mean():.0%}"),
        ("Categories", str(df["category"].nunique())),
        ("Negative Rate", f"{(df['sentiment'] == 'negative').mean():.0%}"),
    ]

    for label, value in kpis:
        st.markdown(
            f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Tickets by Category**")
        cat_counts = df["category"].value_counts()
        fig = px.bar(
            x=cat_counts.index,
            y=cat_counts.values,
            color=cat_counts.values,
            color_continuous_scale="Teal",
        )
        fig.update_layout(
            height=280,
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#a1a1aa", size=11),
            xaxis_title="",
            yaxis_title="Count",
        )
        fig.update_xaxes(gridcolor="rgba(39, 39, 42, 0.5)", tickangle=45)
        fig.update_yaxes(gridcolor="rgba(39, 39, 42, 0.5)")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col2:
        st.markdown("**Sentiment Distribution**")
        sent_counts = df["sentiment"].value_counts()
        fig = px.pie(
            values=sent_counts.values,
            names=sent_counts.index,
            color_discrete_sequence=["#10b981", "#71717a", "#ef4444"],
        )
        fig.update_layout(
            height=280,
            showlegend=True,
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#a1a1aa", size=11),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Data table
    st.markdown("**Sample Results**")
    st.dataframe(
        df[["subject", "category", "confidence", "sentiment"]].head(15),
        use_container_width=True,
        hide_index=True,
        column_config={
            "confidence": st.column_config.ProgressColumn(
                "Confidence", format="%.0f%%", min_value=0, max_value=1
            )
        },
    )


@st.cache_data
def measure_latency(n: int = 500) -> np.ndarray:
    """Measure REAL single-ticket routing latency on this instance (milliseconds)."""
    sample = "App crashes on login and I cannot reset my password or get a refund"
    route(sample, pipe, i2l)  # warm up
    times = []
    for _ in range(n):
        t0 = time.perf_counter()
        route(sample, pipe, i2l)
        times.append((time.perf_counter() - t0) * 1000.0)
    return np.array(times)


def _report_row(name: str, m: dict) -> str:
    return (
        f'<tr><td style="padding: 0.5rem 0;">{name}</td>'
        f'<td align="center">{m["precision"]:.2f}</td>'
        f'<td align="center">{m["recall"]:.2f}</td>'
        f'<td align="center"><strong>{m["f1-score"]:.2f}</strong></td></tr>'
    )


def render_performance():
    metrics = load_metrics()
    latencies = measure_latency()
    p50 = float(np.median(latencies))
    p99 = float(np.percentile(latencies, 99))

    st.markdown(
        f"""
        <div style="background: rgba(20,184,166,0.08); border: 1px solid rgba(20,184,166,0.2);
                    border-radius: 10px; padding: 1rem; margin-bottom: 1.5rem;
                    font-size: 0.8125rem; color: #a1a1aa;">
            Metrics below come from <strong>{metrics["evaluation"]}</strong> on
            <strong>{metrics["data_source"]} ({metrics["n_samples"]} examples)</strong>.
            They show the pipeline working on a small synthetic set and are
            <strong>not</strong> a benchmark on real-world data. Latency is measured
            live on this instance.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        rows = "".join(
            _report_row(name, metrics["per_class"][name])
            for name in metrics["categories"]
        )
        st.markdown(
            f"""
        <div class="card">
            <div class="card-header">Classification Report (cross-validated)</div>
            <table style="width: 100%; font-size: 0.8125rem; color: var(--color-text-secondary);">
                <tr style="border-bottom: 1px solid var(--color-border-subtle);">
                    <th style="text-align: left; padding: 0.5rem 0;">Category</th>
                    <th style="text-align: center;">Precision</th>
                    <th style="text-align: center;">Recall</th>
                    <th style="text-align: center;">F1</th>
                </tr>
                {rows}
            </table>
            <p style="margin-top: 1rem; font-size: 0.8125rem; color: var(--color-text-tertiary);">
                <strong>Overall:</strong> {metrics["model"]["accuracy"]:.0%} accuracy &bull;
                {metrics["model"]["macro_f1"]:.2f} macro F1 &bull;
                vs {metrics["baseline_most_frequent"]["accuracy"]:.0%} most-frequent baseline
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown("**Routing Latency (measured on this instance)**")
        fig = go.Figure()
        fig.add_trace(
            go.Histogram(x=latencies, nbinsx=45, marker_color="#14b8a6", opacity=0.85)
        )
        fig.add_vline(
            x=p99,
            line_dash="dot",
            line_color="#ef4444",
            line_width=1.5,
            annotation_text=f"p99: {p99:.2f}ms",
            annotation_font_size=10,
        )
        fig.add_vline(
            x=p50,
            line_dash="dot",
            line_color="#10b981",
            line_width=1.5,
            annotation_text=f"p50: {p50:.2f}ms",
            annotation_font_size=10,
        )
        fig.update_layout(
            height=280,
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#a1a1aa", size=11),
            xaxis_title="Latency (ms)",
            yaxis_title="Requests",
        )
        fig.update_xaxes(gridcolor="rgba(39, 39, 42, 0.5)")
        fig.update_yaxes(gridcolor="rgba(39, 39, 42, 0.5)")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="metrics-grid" style="grid-template-columns: repeat(3, 1fr);">',
        unsafe_allow_html=True,
    )

    measured = [
        ("p50 Latency", f"{p50:.2f} ms"),
        ("p99 Latency", f"{p99:.2f} ms"),
        ("Throughput (1 core)", f"{1000.0 / p50:,.0f} req/sec"),
    ]
    for label, value in measured:
        st.markdown(
            f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


def render_footer():
    st.markdown(
        """
    <div class="app-footer">
        <div class="footer-left">
            Built by <a href="https://christiangcallahan.tech" style="color: var(--color-accent-secondary); text-decoration: none;">Christian Callahan</a>
        </div>
        <div class="footer-links">
            <a href="https://github.com/CCallahan308/ticket-intel">GitHub</a>
            <a href="https://christiangcallahan.tech">Portfolio</a>
            <a href="mailto:contact@christiangcallahan.tech">Contact</a>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════


def main():
    render_header()
    render_tabs()
    render_footer()


if __name__ == "__main__":
    main()
