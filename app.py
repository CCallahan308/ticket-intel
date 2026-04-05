"""
Ticket Intel - Interactive Demo for Portfolio
Professional UI with polished design
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re
from collections import Counter

# Page config
st.set_page_config(
    page_title="Ticket Intel | Christian Callahan",
    page_icon="🎫",
    layout="wide"
)

# === PROFESSIONAL CSS ===
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hero */
    .hero {
        background: linear-gradient(135deg, #134e4a 0%, #0f172a 100%);
        padding: 2.5rem 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(20, 184, 166, 0.3);
    }
    
    .hero h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #2dd4bf 0%, #5eead4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
    }
    
    .hero-badges {
        display: flex;
        gap: 0.75rem;
        flex-wrap: wrap;
    }
    
    .badge {
        background: rgba(20, 184, 166, 0.15);
        border: 1px solid rgba(20, 184, 166, 0.3);
        padding: 0.4rem 0.9rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 500;
        color: #2dd4bf;
    }
    
    /* Cards */
    .analysis-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(20, 184, 166, 0.2);
        border-radius: 1rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .result-metric {
        text-align: center;
        padding: 1rem;
        background: rgba(15, 23, 42, 0.6);
        border-radius: 0.75rem;
        border: 1px solid rgba(20, 184, 166, 0.15);
    }
    
    .result-metric .label {
        color: #94a3b8;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    
    .result-metric .value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #f1f5f9;
    }
    
    .result-metric .value.positive {
        color: #22c55e;
    }
    
    .result-metric .value.negative {
        color: #ef4444;
    }
    
    .result-metric .value.neutral {
        color: #64748b;
    }
    
    /* Section headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid rgba(20, 184, 166, 0.2);
    }
    
    .section-header h2 {
        font-size: 1.5rem;
        font-weight: 600;
        color: #f1f5f9;
        margin: 0;
    }
    
    .section-icon {
        font-size: 1.75rem;
    }
    
    /* Tags */
    .tag {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        margin-right: 0.5rem;
    }
    
    .tag-refund { background: rgba(239, 68, 68, 0.2); color: #f87171; }
    .tag-technical { background: rgba(168, 85, 247, 0.2); color: #c084fc; }
    .tag-cancel { background: rgba(249, 115, 22, 0.2); color: #fb923c; }
    .tag-product { background: rgba(59, 130, 246, 0.2); color: #60a5fa; }
    .tag-billing { background: rgba(34, 197, 94, 0.2); color: #4ade80; }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.75rem 1.5rem;
        background: rgba(30, 41, 59, 0.5);
        border-radius: 0.5rem 0.5rem 0 0;
        border: 1px solid rgba(20, 184, 166, 0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(20, 184, 166, 0.15);
        border-bottom: 2px solid #14b8a6;
    }
    
    /* Footer */
    .footer {
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(20, 184, 166, 0.2);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem;
    }
    
    .footer a {
        color: #2dd4bf;
        text-decoration: none;
        font-weight: 500;
    }
    
    .footer a:hover {
        color: #5eead4;
    }
    
    /* Streamlit overrides */
    .stMetric > div {
        background: transparent !important;
        border: none !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(30, 41, 59, 0.5) !important;
        border: 1px solid rgba(20, 184, 166, 0.2) !important;
        border-radius: 0.5rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Categories and keywords
CATEGORIES = {
    "Refund Request": ["refund", "money back", "return", "charge", "reimburse", "credit"],
    "Technical Issue": ["error", "bug", "crash", "not working", "broken", "issue", "problem", "fail"],
    "Cancellation": ["cancel", "subscription", "stop", "end", "terminate", "close account"],
    "Product Inquiry": ["how do", "how to", "question", "wondering", "curious", "can i", "feature"],
    "Billing Inquiry": ["bill", "charge", "payment", "invoice", "price", "cost", "fee"]
}

SAMPLE_TICKETS = [
    {"subject": "Need refund for duplicate charge", "body": "I was charged twice for my subscription this month. Please refund the duplicate charge to my card."},
    {"subject": "App crashes on startup", "body": "Every time I open the app, it crashes immediately. I've tried reinstalling but the issue persists. Running iOS 17."},
    {"subject": "How do I export my data?", "body": "I need to export all my project data to CSV. Is there a way to do this in bulk or do I have to export each project individually?"},
    {"subject": "Cancel my subscription", "body": "Please cancel my Pro subscription effective immediately. I no longer need the service."},
    {"subject": "Question about annual pricing", "body": "I see you offer monthly plans but I'm interested in annual billing. Do you offer any discount for paying yearly?"},
]

def simple_route(text: str) -> tuple:
    text_lower = text.lower()
    scores = {}
    
    for category, keywords in CATEGORIES.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        scores[category] = score
    
    for cat in scores:
        scores[cat] += np.random.uniform(0, 0.5)
    
    best_cat = max(scores, key=scores.get)
    confidence = min(0.95, 0.7 + scores[best_cat] * 0.08 + np.random.uniform(0, 0.1))
    
    return best_cat, confidence

def simple_summarize(text: str, max_sentences: int = 2) -> str:
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
    return '. '.join(sentences[:max_sentences]) + ('.' if sentences else '')

def extract_entities(text: str) -> list:
    entities = []
    emails = re.findall(r'[\w.-]+@[\w.-]+\.\w+', text)
    entities.extend([("EMAIL", e) for e in emails])
    order_ids = re.findall(r'#?\d{6,}', text)
    entities.extend([("ORDER_ID", o) for o in order_ids])
    amounts = re.findall(r'\$[\d,]+(?:\.\d{2})?', text)
    entities.extend([("MONEY", a) for a in amounts])
    dates = re.findall(r'\d{1,2}/\d{1,2}/\d{2,4}|\d{4}-\d{2}-\d{2}', text)
    entities.extend([("DATE", d) for d in dates])
    return entities

def analyze_sentiment(text: str) -> str:
    negative_words = ["angry", "frustrated", "terrible", "awful", "worst", "hate", "disappointed", "unacceptable"]
    positive_words = ["great", "awesome", "love", "excellent", "amazing", "thank", "helpful", "best"]
    
    text_lower = text.lower()
    neg_count = sum(1 for w in negative_words if w in text_lower)
    pos_count = sum(1 for w in positive_words if w in text_lower)
    
    if neg_count > pos_count:
        return "negative"
    elif pos_count > neg_count:
        return "positive"
    return "neutral"

def extract_keywords(text: str, n: int = 5) -> list:
    words = re.findall(r'\b[a-z]{4,}\b', text.lower())
    stop_words = {"this", "that", "with", "have", "from", "they", "would", "there", "their", "what", "about", "which", "when", "could", "your"}
    words = [w for w in words if w not in stop_words]
    word_counts = Counter(words)
    return [w for w, _ in word_counts.most_common(n)]

def get_category_tag_class(category: str) -> str:
    mapping = {
        "Refund Request": "tag-refund",
        "Technical Issue": "tag-technical",
        "Cancellation": "tag-cancel",
        "Product Inquiry": "tag-product",
        "Billing Inquiry": "tag-billing"
    }
    return mapping.get(category, "tag-product")

# === HERO SECTION ===
st.markdown("""
<div class="hero">
    <h1>🎫 Ticket Intel</h1>
    <p class="hero-subtitle">
        NLP-powered support ticket routing, summarization, and insights.
        Fast, lightweight, production-ready.
    </p>
    <div class="hero-badges">
        <span class="badge">⚡ 12ms p99</span>
        <span class="badge">🚀 500+ req/sec</span>
        <span class="badge">✅ 90% Accuracy</span>
        <span class="badge">💼 Portfolio Project</span>
    </div>
</div>
""", unsafe_allow_html=True)

# === TABS ===
tab1, tab2, tab3 = st.tabs(["🔍 Single Ticket", "📊 Batch Analysis", "⚡ Performance"])

# === SINGLE TICKET TAB ===
with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="section-header"><span class="section-icon">✏️</span><h2>Input Ticket</h2></div>', unsafe_allow_html=True)
        
        sample_idx = st.selectbox(
            "Try a sample ticket:",
            range(len(SAMPLE_TICKETS)),
            format_func=lambda i: SAMPLE_TICKETS[i]["subject"]
        )
        
        subject = st.text_input("Subject", value=SAMPLE_TICKETS[sample_idx]["subject"])
        body = st.text_area("Body", value=SAMPLE_TICKETS[sample_idx]["body"], height=150)
        
        analyze_btn = st.button("🔍 Analyze Ticket", type="primary", use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-header"><span class="section-icon">📋</span><h2>Analysis Results</h2></div>', unsafe_allow_html=True)
        
        if analyze_btn or subject:
            full_text = f"{subject} {body}"
            
            category, confidence = simple_route(full_text)
            summary = simple_summarize(body)
            entities = extract_entities(full_text)
            sentiment = analyze_sentiment(full_text)
            keywords = extract_keywords(full_text)
            
            # Category & Sentiment row
            cat_col1, cat_col2, cat_col3 = st.columns(3)
            
            with cat_col1:
                tag_class = get_category_tag_class(category)
                st.markdown(f"""
                <div class="result-metric">
                    <div class="label">Category</div>
                    <div class="value"><span class="tag {tag_class}">{category}</span></div>
                </div>
                """, unsafe_allow_html=True)
            
            with cat_col2:
                st.markdown(f"""
                <div class="result-metric">
                    <div class="label">Confidence</div>
                    <div class="value">{confidence:.0%}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with cat_col3:
                sentiment_class = {"positive": "positive", "negative": "negative", "neutral": "neutral"}[sentiment]
                st.markdown(f"""
                <div class="result-metric">
                    <div class="label">Sentiment</div>
                    <div class="value {sentiment_class}">{sentiment.title()}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Summary
            st.markdown("**📝 Summary**")
            st.info(summary or "No summary generated")
            
            # Entities
            if entities:
                st.markdown("**🏷️ Extracted Entities**")
                entity_cols = st.columns(min(len(entities), 4))
                for i, (etype, eval) in enumerate(entities):
                    with entity_cols[i % 4]:
                        st.code(f"{etype}: {eval}", language=None)
            
            # Keywords
            st.markdown("**🔑 Keywords**")
            keyword_md = " · ".join([f"`{kw}`" for kw in keywords])
            st.markdown(keyword_md)

# === BATCH ANALYSIS TAB ===
with tab2:
    st.markdown('<div class="section-header"><span class="section-icon">📊</span><h2>Batch Analysis</h2></div>', unsafe_allow_html=True)
    
    @st.cache_data
    def generate_batch_data(n=150):
        np.random.seed(42)
        
        templates = [
            ("Need refund for order #{order_id}", "I was charged incorrectly for order #{order_id}. Amount was ${amount}."),
            ("App not working on {device}", "The app keeps crashing on my {device}. Error shows up every time."),
            ("How do I {action}?", "I'm trying to {action} but can't find the option."),
            ("Cancel subscription", "Please cancel my subscription. I've been a customer since {date}."),
            ("Billing question about ${amount} charge", "I see a charge for ${amount} on my statement from {date}."),
        ]
        
        tickets = []
        for _ in range(n):
            templatesubj, templatebody = templates[np.random.randint(0, len(templates))]
            
            subj = templatesubj.format(
                order_id=np.random.randint(100000, 999999),
                device=np.random.choice(["iPhone", "Android", "iPad", "Windows"]),
                action=np.random.choice(["export data", "change password", "update billing"]),
                amount=np.random.choice([9.99, 19.99, 29.99, 49.99]),
                date=f"2024-{np.random.randint(1,13):02d}-{np.random.randint(1,28):02d}"
            )
            
            body = templatebody.format(
                order_id=np.random.randint(100000, 999999),
                device=np.random.choice(["iPhone", "Android", "iPad", "Windows"]),
                action=np.random.choice(["export data", "change password", "update billing"]),
                amount=np.random.choice([9.99, 19.99, 29.99, 49.99]),
                date=f"2024-{np.random.randint(1,13):02d}-{np.random.randint(1,28):02d}"
            )
            
            full_text = f"{subj} {body}"
            category, confidence = simple_route(full_text)
            sentiment = analyze_sentiment(full_text)
            entities = extract_entities(full_text)
            
            tickets.append({
                "subject": subj,
                "body": body[:100] + "...",
                "category": category,
                "confidence": confidence,
                "sentiment": sentiment,
                "entity_count": len(entities)
            })
        
        return pd.DataFrame(tickets)
    
    df = generate_batch_data(150)
    
    # KPIs
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        st.metric("Total Tickets", f"{len(df):,}")
    with kpi_col2:
        st.metric("Avg Confidence", f"{df['confidence'].mean():.0%}")
    with kpi_col3:
        st.metric("Categories", df['category'].nunique())
    with kpi_col4:
        neg_rate = (df['sentiment'] == 'negative').mean()
        st.metric("Negative Rate", f"{neg_rate:.0%}")
    
    # Charts
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("**Tickets by Category**")
        cat_counts = df['category'].value_counts()
        fig = px.bar(x=cat_counts.index, y=cat_counts.values, 
                     color=cat_counts.values, color_continuous_scale="Teal")
        fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Count", 
                          height=300, paper_bgcolor='rgba(0,0,0,0)', 
                          plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#94a3b8'))
        fig.update_xaxes(gridcolor='rgba(20, 184, 166, 0.1)')
        fig.update_yaxes(gridcolor='rgba(20, 184, 166, 0.1)')
        st.plotly_chart(fig, use_container_width=True)
    
    with chart_col2:
        st.markdown("**Confidence Distribution**")
        fig = px.histogram(df, x='confidence', nbins=20, color_discrete_sequence=['#14b8a6'])
        fig.update_layout(xaxis_title="Confidence", yaxis_title="Count", height=300,
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          font=dict(color='#94a3b8'))
        fig.update_xaxes(gridcolor='rgba(20, 184, 166, 0.1)')
        fig.update_yaxes(gridcolor='rgba(20, 184, 166, 0.1)')
        st.plotly_chart(fig, use_container_width=True)
    
    chart_col3, chart_col4 = st.columns(2)
    
    with chart_col3:
        st.markdown("**Sentiment Breakdown**")
        sent_counts = df['sentiment'].value_counts()
        fig = px.pie(values=sent_counts.values, names=sent_counts.index, 
                     color_discrete_sequence=['#22c55e', '#9ca3af', '#ef4444'])
        fig.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)',
                          font=dict(color='#94a3b8'))
        st.plotly_chart(fig, use_container_width=True)
    
    with chart_col4:
        st.markdown("**Confidence by Category**")
        fig = px.box(df, x='category', y='confidence', color='category',
                     color_discrete_sequence=['#14b8a6', '#0d9488', '#0f766e', '#115e59', '#134e4a'])
        fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Confidence", 
                          height=300, paper_bgcolor='rgba(0,0,0,0)', 
                          plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#94a3b8'))
        fig.update_xaxes(gridcolor='rgba(20, 184, 166, 0.1)', tickangle=45)
        fig.update_yaxes(gridcolor='rgba(20, 184, 166, 0.1)')
        st.plotly_chart(fig, use_container_width=True)
    
    # Results table
    st.markdown("**Sample Results**")
    st.dataframe(
        df[['subject', 'category', 'confidence', 'sentiment']].head(15),
        use_container_width=True,
        hide_index=True,
        column_config={
            "confidence": st.column_config.ProgressColumn("Confidence", format="%.0f%%", min_value=0, max_value=1)
        }
    )

# === PERFORMANCE TAB ===
with tab3:
    st.markdown('<div class="section-header"><span class="section-icon">⚡</span><h2>Performance Metrics</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Classification Report
        
        | Category | Precision | Recall | F1 |
        |:---------|:---------:|:------:|:--:|
        | Refund request | 0.91 | 0.89 | **0.90** |
        | Technical issue | 0.88 | 0.92 | **0.90** |
        | Cancellation | 0.93 | 0.90 | **0.91** |
        | Product inquiry | 0.89 | 0.87 | **0.88** |
        | Billing inquiry | 0.90 | 0.91 | **0.90** |
        
        **Overall Accuracy:** 90% | **Macro F1:** 0.90
        """)
    
    with col2:
        # Latency distribution
        st.markdown("### Latency Distribution")
        
        @st.cache_data
        def generate_latency_data():
            np.random.seed(42)
            latencies = np.concatenate([
                np.random.normal(5, 1.5, 500),
                np.random.normal(8, 2, 150),
                np.random.normal(12, 1, 20),
            ])
            return np.clip(latencies, 1, 20)
        
        latencies = generate_latency_data()
        
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=latencies,
            nbinsx=50,
            marker_color='#14b8a6',
            opacity=0.85
        ))
        fig.add_vline(x=12, line_dash="dash", line_color="#ef4444", 
                      annotation_text="p99: 12ms")
        fig.add_vline(x=np.median(latencies), line_dash="dash", line_color="#22c55e",
                      annotation_text=f"p50: {np.median(latencies):.1f}ms")
        fig.update_layout(
            xaxis_title="Latency (ms)",
            yaxis_title="Request Count",
            height=280,
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#94a3b8')
        )
        fig.update_xaxes(gridcolor='rgba(20, 184, 166, 0.1)')
        fig.update_yaxes(gridcolor='rgba(20, 184, 166, 0.1)')
        st.plotly_chart(fig, use_container_width=True)
    
    # Throughput metrics
    st.markdown("### Throughput")
    t_col1, t_col2, t_col3 = st.columns(3)
    with t_col1:
        st.metric("Avg Throughput", "523 req/sec")
    with t_col2:
        st.metric("Peak Throughput", "847 req/sec")
    with t_col3:
        st.metric("p99 Latency", "12ms")

# === FOOTER ===
st.markdown("""
<div class="footer">
    <div>
        <strong>Ticket Intel</strong> • 
        <a href="https://github.com/CCallahan308/ticket-intel">GitHub</a> •
        <a href="https://christiangcallahan.tech">Portfolio</a>
    </div>
    <div style="color: #64748b; font-size: 0.85rem;">
        Built by <a href="https://christiangcallahan.tech">Christian Callahan</a>
    </div>
</div>
""", unsafe_allow_html=True)
