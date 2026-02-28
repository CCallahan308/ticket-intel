"""Plotly chart builders for Ticket Intel dashboard"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from collections import Counter

from styles import COLORS, PLOTLY_TEMPLATE, SENTIMENT_COLORS


def _apply_template(fig):
    fig.update_layout(**PLOTLY_TEMPLATE["layout"])
    return fig


def category_bar_chart(
    data: pd.Series, title: str = "Category Distribution"
) -> go.Figure:
    fig = go.Figure()

    categories = data.index.astype(str).tolist()
    values = data.values.tolist()

    # highlight the biggest bar
    colors = [COLORS["accent"] if v == max(values) else "#99F6E4" for v in values]

    fig.add_trace(
        go.Bar(
            y=categories,
            x=values,
            orientation="h",
            marker=dict(color=colors, line=dict(color=COLORS["border"], width=1)),
            text=values,
            textposition="outside",
            textfont=dict(color=COLORS["text_secondary"], size=11),
            hovertemplate="<b>%{y}</b><br>Count: %{x}<extra></extra>",
        )
    )

    fig.update_layout(
        title=dict(text=title, font=dict(size=14, color=COLORS["text_primary"])),
        xaxis=dict(title="Count", gridcolor=COLORS["border"]),
        yaxis=dict(title="", autorange="reversed"),
        height=max(300, len(categories) * 35),
        margin=dict(l=120, r=40, t=50, b=40),
    )

    return _apply_template(fig)


def confidence_histogram(data: pd.Series, bins: int = 20) -> go.Figure:
    fig = go.Figure()

    values = data.values
    mean_val = data.mean()

    fig.add_trace(
        go.Histogram(
            x=values,
            nbinsx=bins,
            marker=dict(color=COLORS["accent"], line=dict(color="white", width=1)),
            opacity=0.85,
            hovertemplate="Confidence: %{x:.2f}<br>Count: %{y}<extra></extra>",
        )
    )

    # mean marker
    fig.add_vline(
        x=mean_val,
        line=dict(color=COLORS["warning"], width=2, dash="dash"),
        annotation=dict(
            text=f"Mean: {mean_val:.1%}",
            font=dict(color=COLORS["warning"], size=11),
            xanchor="left",
            yanchor="top",
        ),
    )

    fig.update_layout(
        title=dict(text="Confidence Distribution", font=dict(size=14)),
        xaxis=dict(
            title="Confidence Score", tickformat=".0%", gridcolor=COLORS["border"]
        ),
        yaxis=dict(title="Count", gridcolor=COLORS["border"]),
        bargap=0.05,
        showlegend=False,
        height=300,
    )

    return _apply_template(fig)


def sentiment_donut(data: pd.Series) -> go.Figure:
    fig = go.Figure()

    labels = data.index.tolist()
    values = data.values.tolist()
    colors = [SENTIMENT_COLORS.get(l, COLORS["neutral"]) for l in labels]

    fig.add_trace(
        go.Pie(
            labels=labels,
            values=values,
            hole=0.55,
            marker=dict(colors=colors, line=dict(color="white", width=2)),
            textinfo="percent",
            textfont=dict(size=11, color=COLORS["text_primary"]),
            hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percent: %{percent}<extra></extra>",
            sort=False,
        )
    )

    # show total in the middle
    total = sum(values)
    fig.add_annotation(
        text=f"<b>{total:,}</b><br><span style='font-size:10px;color:#64748B'>Total</span>",
        x=0.5,
        y=0.5,
        font=dict(size=16, color=COLORS["text_primary"]),
        showarrow=False,
    )

    fig.update_layout(
        title=dict(text="Sentiment Breakdown", font=dict(size=14)),
        showlegend=True,
        legend=dict(orientation="h", y=-0.1, x=0.5, xanchor="center"),
        height=320,
        margin=dict(t=50, b=50),
    )

    return _apply_template(fig)


def keyword_barchart(keywords: list, title: str = "Top Keywords") -> go.Figure:
    # TODO: accept a max_keywords param to customize
    if not keywords:
        fig = go.Figure()
        fig.add_annotation(text="No keywords found", x=0.5, y=0.5)
        return _apply_template(fig)

    kw_counts = Counter(keywords).most_common(15)

    fig = go.Figure()

    words = [k[0] for k in kw_counts][::-1]
    counts = [k[1] for k in kw_counts][::-1]

    fig.add_trace(
        go.Bar(
            y=words,
            x=counts,
            orientation="h",
            marker=dict(
                color=counts,
                colorscale=[[0, "#99F6E4"], [0.5, COLORS["accent"]], [1, "#0F766E"]],
                line=dict(color=COLORS["border"], width=1),
            ),
            text=counts,
            textposition="outside",
            textfont=dict(color=COLORS["text_secondary"], size=10),
            hovertemplate="<b>%{y}</b><br>Count: %{x}<extra></extra>",
        )
    )

    fig.update_layout(
        title=dict(text=title, font=dict(size=14)),
        xaxis=dict(title="Count", gridcolor=COLORS["border"]),
        yaxis=dict(title=""),
        height=350,
        margin=dict(l=100, r=40, t=50, b=40),
        showlegend=False,
    )

    return _apply_template(fig)


def confidence_gauge(value: float, title: str = "Confidence") -> go.Figure:
    fig = go.Figure()

    # thresholds: <50% red, 50-70% yellow, >70% green
    if value >= 0.7:
        bar_color = COLORS["success"]
    elif value >= 0.5:
        bar_color = COLORS["warning"]
    else:
        bar_color = COLORS["error"]

    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=value * 100,
            title=dict(text=title, font=dict(size=12, color=COLORS["text_secondary"])),
            number=dict(suffix="%", font=dict(size=28, color=COLORS["text_primary"])),
            gauge=dict(
                axis=dict(
                    range=[0, 100], tickwidth=1, tickcolor=COLORS["text_secondary"]
                ),
                bar=dict(color=bar_color, thickness=0.4),
                bgcolor=COLORS["neutral_light"],
                borderwidth=1,
                bordercolor=COLORS["border"],
                steps=[
                    dict(range=[0, 50], color="#FEE2E2"),
                    dict(range=[50, 70], color="#FEF3C7"),
                    dict(range=[70, 100], color="#D1FAE5"),
                ],
            ),
        )
    )

    fig.update_layout(
        height=200,
        margin=dict(l=20, r=20, t=40, b=20),
    )

    return fig


def category_scatter(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    agg = (
        df.groupby("category")
        .agg(avg_conf=("confidence", "mean"), count=("category", "count"))
        .reset_index()
    )

    fig.add_trace(
        go.Scatter(
            x=agg["count"],
            y=agg["avg_conf"],
            mode="markers",
            marker=dict(
                size=agg["count"],
                sizemode="area",
                sizeref=2.0 * max(agg["count"]) / (40.0**2),
                color=agg["avg_conf"],
                colorscale=[
                    [0, "#FEE2E2"],
                    [0.5, COLORS["accent"]],
                    [1, COLORS["success"]],
                ],
                line=dict(color="white", width=1),
                showscale=True,
                colorbar=dict(title="Avg Conf", len=0.7),
            ),
            text=agg["category"],
            hovertemplate="<b>%{text}</b><br>Tickets: %{x}<br>Avg Confidence: %{y:.1%}<extra></extra>",
        )
    )

    fig.update_layout(
        title=dict(text="Confidence vs Volume", font=dict(size=14)),
        xaxis=dict(title="Ticket Count", gridcolor=COLORS["border"]),
        yaxis=dict(
            title="Avg Confidence",
            tickformat=".0%",
            gridcolor=COLORS["border"],
            range=[0, 1],
        ),
        height=350,
        showlegend=False,
    )

    return _apply_template(fig)


def sentiment_by_category(df: pd.DataFrame) -> go.Figure:
    agg = df.groupby(["category", "sentiment"]).size().reset_index(name="count")

    fig = px.bar(
        agg,
        x="category",
        y="count",
        color="sentiment",
        barmode="stack",
        color_discrete_map=SENTIMENT_COLORS,
        category_orders={"sentiment": ["positive", "neutral", "negative"]},
    )

    fig.update_traces(
        marker=dict(line=dict(color="white", width=0.5)),
        hovertemplate="<b>%{x}</b><br>Count: %{y}<extra></extra>",
    )

    fig.update_layout(
        title=dict(text="Sentiment by Category", font=dict(size=14)),
        xaxis=dict(title="", tickangle=-45, gridcolor=COLORS["border"]),
        yaxis=dict(title="Count", gridcolor=COLORS["border"]),
        legend=dict(title="", orientation="h", y=-0.3, x=0.5, xanchor="center"),
        height=380,
        margin=dict(b=100),
    )

    return _apply_template(fig)


def probability_bar(
    probs: dict, title: str = "Classification Probabilities"
) -> go.Figure:
    sorted_probs = sorted(probs.items(), key=lambda x: x[1], reverse=True)

    categories = [p[0] for p in sorted_probs]
    values = [p[1] * 100 for p in sorted_probs]

    # winner gets accent, rest fade based on score
    colors = []
    for i, v in enumerate(values):
        if i == 0:
            colors.append(COLORS["accent"])
        elif v > 20:
            colors.append("#5EEAD4")
        elif v > 10:
            colors.append("#99F6E4")
        else:
            colors.append(COLORS["neutral_light"])

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y=categories,
            x=values,
            orientation="h",
            marker=dict(color=colors, line=dict(color=COLORS["border"], width=1)),
            text=[f"{v:.1f}%" for v in values],
            textposition="outside",
            textfont=dict(size=10, color=COLORS["text_secondary"]),
            hovertemplate="<b>%{y}</b><br>Probability: %{x:.1f}%<extra></extra>",
        )
    )

    fig.update_layout(
        title=dict(text=title, font=dict(size=12)),
        xaxis=dict(
            title="",
            tickformat=".0f",
            range=[0, max(values) * 1.2],
            gridcolor=COLORS["border"],
        ),
        yaxis=dict(title=""),
        height=max(200, len(categories) * 30),
        margin=dict(l=100, r=60, t=40, b=30),
        showlegend=False,
    )

    return _apply_template(fig)


def entity_count_histogram(data: pd.Series) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=data.values,
            nbinsx=15,
            marker=dict(color=COLORS["accent"], line=dict(color="white", width=1)),
            opacity=0.85,
            hovertemplate="Entities: %{x}<br>Tickets: %{y}<extra></extra>",
        )
    )

    fig.update_layout(
        title=dict(text="Entities per Ticket", font=dict(size=14)),
        xaxis=dict(title="Entity Count", gridcolor=COLORS["border"]),
        yaxis=dict(title="Tickets", gridcolor=COLORS["border"]),
        bargap=0.1,
        height=300,
    )

    return _apply_template(fig)
