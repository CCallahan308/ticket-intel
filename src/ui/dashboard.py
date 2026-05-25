"""
Ticket Intel Dashboard

NOTE: There's also a simpler run_dashboard() in main.py. This file is the
fancy version with custom CSS/components. Keeping both around since the
simple one is easier to debug when something breaks here.
"""


import streamlit as st
import pandas as pd

from src.ui.styles import CSS, COLORS, header, metric_card, status_badge
from src.ui.styles import section_header
from src.ui.charts import (
    category_bar_chart,
    confidence_histogram,
    sentiment_donut,
    keyword_barchart,
)
from src.ui.charts import (
    category_scatter,
    sentiment_by_category,
)
from src.ui.charts import entity_count_histogram
from src.models.router import load_router, route
from src.models.summarizer import summarize
from src.models.insights import insights
from src.data.loader import find_column

# Page config
st.set_page_config(
    page_title="Ticket Intel",
    page_icon="static/icon.svg",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None,
)

# Load styles
st.markdown(CSS, unsafe_allow_html=True)

# header
st.markdown(
    header("Ticket Intel", "NLP-powered support ticket analysis"),
    unsafe_allow_html=True,
)


# Model loading
@st.cache_resource
def load_model():
    return load_router()


with st.spinner("Loading model..."):
    pipe, l2i, i2l = load_model()

# Layout
main_col, side_col = st.columns([3, 1], gap="large")

with side_col:
    st.markdown(status_badge("active", "Model Ready"), unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.markdown("**Configuration**")
    n_sentences = st.slider(
        "Summary length", 1, 7, 3, help="Sentences in extractive summary"
    )

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.markdown("**Model Info**")
    st.markdown(
        f'<div class="card" style="padding: 0.75rem;"><div style="font-size: 0.75rem; color: {COLORS["text_secondary"]}; margin-bottom: 0.25rem;">Categories</div><div style="font-size: 1.25rem; font-weight: 600; color: {COLORS["text_primary"]}">{len(i2l)}</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="card" style="padding: 0.75rem; margin-top: 0.5rem;"><div style="font-size: 0.75rem; color: {COLORS["text_secondary"]}; margin-bottom: 0.25rem;">Algorithm</div><div style="font-size: 0.875rem; font-weight: 500; color: {COLORS["text_primary"]}">TF-IDF + Naive Bayes</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.markdown("**API Endpoint**")
    st.code("http://localhost:8000", language=None)

with main_col:
    # Main tabs
    tab_batch, tab_stats = st.tabs(["Dataset Analysis", "Statistics"])

    # === BATCH TAB ===
    with tab_batch:
        st.markdown(section_header("Dataset Analysis", "📁"), unsafe_allow_html=True)

        @st.cache_data
        def get_dataset():
            from src.data.loader import load_tickets

            try:
                return load_tickets()
            except FileNotFoundError:
                return None

        df = get_dataset()

        if df is not None:
            # File info
            st.markdown(
                f"""
            <div class="info-box teal" style="margin: 1rem 0;">
                <strong>Loaded {len(df):,} rows</strong> with {len(df.columns)} columns
            </div>
            """,
                unsafe_allow_html=True,
            )

            with st.expander("Preview Data", expanded=False):
                st.dataframe(df.head(5), use_container_width=True, hide_index=True)

            # Column detection
            subj_col = find_column(df, "subj")
            body_col = find_column(df, "body")

            if not subj_col or not body_col:
                st.markdown(
                    """
                <div class="info-box red">
                    <strong>Column Detection Failed</strong><br>
                    Could not find subject/body columns. Expected: Subject, Body, Ticket Subject, Ticket Description
                </div>
                """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                <div style="display: flex; gap: 1rem; margin: 1rem 0;">
                    <div class="tag teal">Subject: {subj_col}</div>
                    <div class="tag teal">Body: {body_col}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                do_analysis = False

                if "batch_results" not in st.session_state:
                    if st.button(
                        "Analyze All Tickets", type="primary", use_container_width=True
                    ):
                        do_analysis = True
                else:
                    if st.button("Re-analyze Tickets", use_container_width=True):
                        del st.session_state["batch_results"]
                        do_analysis = True

                if do_analysis:
                    progress_bar = st.progress(0, text="Initializing...")
                    status_text = st.empty()

                    results = []
                    total = len(df)

                    for i, (_, row) in enumerate(df.iterrows()):
                        txt = f"{row.get(subj_col, '')} {row.get(body_col, '')}"

                        cat, conf, _ = route(txt, pipe, i2l)
                        summ, _ = summarize(txt, n_sentences)
                        ents, kws, sent = insights(txt)

                        results.append(
                            {
                                "category": cat,
                                "confidence": round(conf, 4),
                                "summary": summ[:150] + "..."
                                if len(summ) > 150
                                else summ,
                                "entity_count": len(ents),
                                "keywords": ", ".join(kws[:3]),
                                "sentiment": sent,
                            }
                        )

                        pct = (i + 1) / total
                        progress_bar.progress(
                            pct, text=f"Processing {i + 1:,} / {total:,}"
                        )

                    progress_bar.empty()
                    status_text.empty()

                    # Combine results
                    result_df = pd.DataFrame(results)
                    output_df = pd.concat(
                        [df.reset_index(drop=True), result_df], axis=1
                    )
                    st.session_state["batch_results"] = output_df

                if "batch_results" in st.session_state:
                    output_df = st.session_state["batch_results"]

                    # Success toast
                    st.markdown(
                        f"""
                    <div class="info-box green" style="margin: 1rem 0;">
                        <strong>Analysis Complete</strong> - Processed {len(output_df):,} tickets
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                    # KPI Row
                    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

                    with kpi_col1:
                        st.markdown(
                            metric_card(
                                "Total Tickets",
                                f"{len(output_df):,}",
                                icon="📊",
                                color="teal",
                            ),
                            unsafe_allow_html=True,
                        )

                    with kpi_col2:
                        st.markdown(
                            metric_card(
                                "Avg Confidence",
                                f"{output_df['confidence'].mean():.1%}",
                                icon="🎯",
                                color="green",
                            ),
                            unsafe_allow_html=True,
                        )

                    with kpi_col3:
                        st.markdown(
                            metric_card(
                                "Categories",
                                f"{output_df['category'].nunique()}",
                                icon="📁",
                                color="amber",
                            ),
                            unsafe_allow_html=True,
                        )

                    with kpi_col4:
                        neg_pct = (output_df["sentiment"] == "negative").mean()
                        st.markdown(
                            metric_card(
                                "Negative Rate", f"{neg_pct:.1%}", icon="⚠", color="red"
                            ),
                            unsafe_allow_html=True,
                        )

                    st.markdown(
                        "<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True
                    )

                    # Results table
                    st.markdown(
                        section_header("Results Preview", "📋"), unsafe_allow_html=True
                    )
                    st.dataframe(
                        output_df.head(25),
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "confidence": st.column_config.ProgressColumn(
                                "Confidence", format="%.0f%%", min_value=0, max_value=1
                            ),
                            "sentiment": st.column_config.TextColumn("Sentiment"),
                            "category": st.column_config.TextColumn("Category"),
                        },
                    )

                    st.markdown(
                        "<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True
                    )

                    # Visualizations
                    st.markdown(
                        section_header("Visualizations", "📈"), unsafe_allow_html=True
                    )

                    viz_row1_col1, viz_row1_col2 = st.columns(2)

                    with viz_row1_col1:
                        st.plotly_chart(
                            category_bar_chart(output_df["category"].value_counts()),
                            use_container_width=True,
                        )

                    with viz_row1_col2:
                        st.plotly_chart(
                            confidence_histogram(output_df["confidence"]),
                            use_container_width=True,
                        )

                    viz_row2_col1, viz_row2_col2 = st.columns(2)

                    with viz_row2_col1:
                        st.plotly_chart(
                            sentiment_donut(output_df["sentiment"].value_counts()),
                            use_container_width=True,
                        )

                    with viz_row2_col2:
                        all_keywords = []
                        for kw_str in output_df["keywords"]:
                            all_keywords.extend(
                                [k.strip() for k in str(kw_str).split(",") if k.strip()]
                            )
                        st.plotly_chart(
                            keyword_barchart(all_keywords), use_container_width=True
                        )

                    st.markdown(
                        "<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True
                    )

                    # Export
                    st.markdown(
                        section_header("Export Results", "💾"), unsafe_allow_html=True
                    )

                    col_export1, col_export2 = st.columns([1, 3])
                    with col_export1:
                        csv_data = output_df.to_csv(index=False).encode()
                        st.download_button(
                            "Download CSV",
                            csv_data,
                            "analyzed_tickets.csv",
                            "text/csv",
                            type="primary",
                            use_container_width=True,
                        )

        else:
            # Empty state
            st.markdown(
                """
            <div class="card" style="text-align: center; padding: 3rem; margin-top: 2rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;">📁</div>
                <div style="font-size: 1.1rem; font-weight: 500; color: #1A1D21; margin-bottom: 0.5rem;">
                    Dataset Not Found
                </div>
                <div style="font-size: 0.875rem; color: #64748B;">
                    Could not find tickets.csv or any alternative dataset file in the project directory.<br>
                    Please ensure the dataset is downloaded.
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    # === STATISTICS TAB ===
    with tab_stats:
        st.markdown(section_header("Batch Statistics", "📊"), unsafe_allow_html=True)

        if "batch_results" in st.session_state:
            results = st.session_state["batch_results"]

            # Summary
            st.markdown(
                f"""
            <div class="info-box teal" style="margin-bottom: 1.5rem;">
                Analyzing <strong>{len(results):,} tickets</strong> from current batch
            </div>
            """,
                unsafe_allow_html=True,
            )

            # Detailed stats
            stat_col1, stat_col2 = st.columns(2)

            with stat_col1:
                st.plotly_chart(category_scatter(results), use_container_width=True)

            with stat_col2:
                st.plotly_chart(
                    sentiment_by_category(results), use_container_width=True
                )

            # Entity stats
            st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

            stat_col3, stat_col4 = st.columns(2)

            with stat_col3:
                st.plotly_chart(
                    entity_count_histogram(results["entity_count"]),
                    use_container_width=True,
                )

            with stat_col4:
                import plotly.express as px
                from src.ui.styles import PLOTLY_TEMPLATE

                # Use a box plot for better distribution visualization
                fig = px.box(
                    results,
                    x="confidence",
                    y="category",
                    color="category",
                    color_discrete_sequence=[
                        COLORS["accent"],
                        "#5EEAD4",
                        "#0F766E",
                        "#99F6E4",
                        "#115E59",
                    ],
                )

                fig.update_layout(
                    title=dict(text="Confidence by Category", font=dict(size=14)),
                    xaxis=dict(
                        title="Confidence Score",
                        tickformat=".0%",
                        gridcolor=COLORS["border"],
                    ),
                    yaxis=dict(title=""),
                    showlegend=False,
                    height=300,
                    margin=dict(l=100),
                )
                fig.update_layout(**PLOTLY_TEMPLATE["layout"])
                st.plotly_chart(fig, use_container_width=True)

        else:
            st.markdown(
                """
            <div class="card" style="text-align: center; padding: 3rem; margin-top: 2rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;">📊</div>
                <div style="font-size: 1.1rem; font-weight: 500; color: #1A1D21; margin-bottom: 0.5rem;">
                    No batch data available
                </div>
                <div style="font-size: 0.875rem; color: #64748B;">
                    Analyze the dataset in the Dataset Analysis tab<br>
                    to see detailed statistics here
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

# Footer
st.markdown(
    """
<div style="margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid #E2E8F0; text-align: center;">
    <span style="font-size: 0.75rem; color: #94A3B8;">
        Ticket Intel v1.0 · Built with TF-IDF + Naive Bayes ·
        <a href="http://localhost:8000/docs" style="color: #0D9488; text-decoration: none;">API Docs</a>
    </span>
</div>
""",
    unsafe_allow_html=True,
)
