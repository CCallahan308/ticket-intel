"""Theme and CSS styles for Ticket Intel dashboard"""

# Color palette - "Obsidian Teal"
COLORS = {
    "bg": "#F8FAFB",
    "surface": "#FFFFFF",
    "text_primary": "#1A1D21",
    "text_secondary": "#64748B",
    "text_muted": "#94A3B8",
    "accent": "#0D9488",
    "accent_light": "#CCFBF1",
    "accent_dark": "#0F766E",
    "border": "#E2E8F0",
    "border_dark": "#CBD5E1",
    "success": "#059669",
    "success_light": "#D1FAE5",
    "warning": "#D97706",
    "warning_light": "#FEF3C7",
    "error": "#DC2626",
    "error_light": "#FEE2E2",
    "neutral": "#64748B",
    "neutral_light": "#F1F5F9",
}

# Sentiment colors
SENTIMENT_COLORS = {
    "positive": "#059669",
    "negative": "#DC2626",
    "neutral": "#64748B",
}

# Plotly template
PLOTLY_TEMPLATE = {
    "layout": {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {
            "family": "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
            "color": COLORS["text_primary"],
            "size": 12,
        },
        "title": {
            "font": {"size": 14, "color": COLORS["text_primary"]},
        },
        "xaxis": {
            "gridcolor": COLORS["border"],
            "linecolor": COLORS["border"],
            "tickfont": {"color": COLORS["text_secondary"]},
            "title": {"font": {"color": COLORS["text_secondary"]}},
        },
        "yaxis": {
            "gridcolor": COLORS["border"],
            "linecolor": COLORS["border"],
            "tickfont": {"color": COLORS["text_secondary"]},
            "title": {"font": {"color": COLORS["text_secondary"]}},
        },
        "legend": {
            "font": {"color": COLORS["text_secondary"]},
            "bgcolor": "rgba(0,0,0,0)",
        },
        "margin": {"l": 40, "r": 20, "t": 40, "b": 40},
    }
}

# Main CSS
CSS = """
<style>
    /* Reset and base */
    @import url('data:text/css,');

    :root {
        --bg: #F8FAFB;
        --surface: #FFFFFF;
        --text-primary: #1A1D21;
        --text-secondary: #64748B;
        --accent: #0D9488;
        --accent-light: #CCFBF1;
        --border: #E2E8F0;
        --success: #059669;
        --warning: #D97706;
        --error: #DC2626;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Global styles */
    .stApp {
        background-color: var(--bg);
    }

    /* Typography */
    html, body, .stApp {
        font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    /* Main container */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Cards */
    .card {
        background: var(--surface);
        border-radius: 8px;
        border: 1px solid var(--border);
        padding: 1.25rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }

    .card:hover {
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }

    .card-header {
        font-size: 0.75rem;
        font-weight: 500;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }

    .card-value {
        font-size: 1.75rem;
        font-weight: 600;
        color: var(--text-primary);
        line-height: 1.2;
    }

    .card-delta {
        font-size: 0.875rem;
        font-weight: 500;
        margin-top: 0.25rem;
    }

    .card-delta.positive { color: var(--success); }
    .card-delta.negative { color: var(--error); }
    .card-delta.neutral { color: var(--text-secondary); }

    /* Metric cards */
    .metric-card {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
    }

    .metric-icon {
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        flex-shrink: 0;
    }

    .metric-icon.teal { background: #CCFBF1; color: #0D9488; }
    .metric-icon.green { background: #D1FAE5; color: #059669; }
    .metric-icon.amber { background: #FEF3C7; color: #D97706; }
    .metric-icon.red { background: #FEE2E2; color: #DC2626; }
    .metric-icon.gray { background: #F1F5F9; color: #64748B; }

    /* Status badge */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.375rem;
        padding: 0.375rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 500;
    }

    .status-badge.active {
        background: #D1FAE5;
        color: #059669;
    }

    .status-badge.inactive {
        background: #FEE2E2;
        color: #DC2626;
    }

    .status-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: currentColor;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    /* Tags and pills */
    .tag {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.625rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 500;
        margin: 0.125rem;
        background: #F1F5F9;
        color: #475569;
        border: 1px solid #E2E8F0;
    }

    .tag.teal { background: #CCFBF1; color: #0F766E; border-color: #99F6E4; }
    .tag.green { background: #D1FAE5; color: #047857; border-color: #A7F3D0; }
    .tag.amber { background: #FEF3C7; color: #B45309; border-color: #FCD34D; }
    .tag.red { background: #FEE2E2; color: #B91C1C; border-color: #FCA5A5; }

    /* Sentiment badge */
    .sentiment-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.375rem;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 0.875rem;
        font-weight: 500;
    }

    .sentiment-badge.positive {
        background: #ECFDF5;
        color: #047857;
        border: 1px solid #A7F3D0;
    }

    .sentiment-badge.negative {
        background: #FEF2F2;
        color: #B91C1C;
        border: 1px solid #FECACA;
    }

    .sentiment-badge.neutral {
        background: #F8FAFC;
        color: #475569;
        border: 1px solid #E2E8F0;
    }

    /* File upload zone */
    .upload-zone {
        border: 2px dashed #CBD5E1;
        border-radius: 12px;
        padding: 2.5rem;
        text-align: center;
        background: #FAFBFC;
        transition: all 0.2s ease;
        cursor: pointer;
    }

    .upload-zone:hover {
        border-color: var(--accent);
        background: #F0FDFA;
    }

    .upload-zone-icon {
        font-size: 2.5rem;
        margin-bottom: 0.75rem;
        color: #94A3B8;
    }

    .upload-zone-text {
        color: var(--text-secondary);
        font-size: 0.875rem;
    }

    .upload-zone-text strong {
        color: var(--accent);
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
        border: none;
        transition: all 0.15s ease;
    }

    .stButton > button[kind="primary"] {
        background: #0D9488;
        color: white;
        border: 1px solid #0F766E;
    }

    .stButton > button[kind="primary"]:hover {
        background: #0F766E;
        color: white;
    }

    .stButton > button[kind="secondary"] {
        background: #F1F5F9;
        color: #475569;
        border: 1px solid #E2E8F0;
    }

    /* Progress bar */
    .stProgress > div > div > div {
        background: #0D9488;
    }

    /* Dataframes */
    .stDataFrame {
        border: 1px solid var(--border);
        border-radius: 8px;
        overflow: hidden;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.625rem 1.25rem;
        font-weight: 500;
        color: var(--text-secondary);
    }

    .stTabs [aria-selected="true"] {
        background: var(--accent);
        color: white;
    }

    .stTabs [data-baseweb="tab"]:hover:not([aria-selected="true"]) {
        background: #F1F5F9;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: var(--surface);
        border-right: 1px solid var(--border);
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem;
    }

    /* Info boxes */
    .info-box {
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid;
        margin: 0.5rem 0;
    }

    .info-box.teal {
        background: #F0FDFA;
        border-color: var(--accent);
        color: #0F766E;
    }

    .info-box.green {
        background: #ECFDF5;
        border-color: var(--success);
        color: #047857;
    }

    .info-box.amber {
        background: #FFFBEB;
        border-color: var(--warning);
        color: #92400E;
    }

    .info-box.red {
        background: #FEF2F2;
        border-color: var(--error);
        color: #991B1B;
    }

    /* Quote box for summaries */
    .quote-box {
        background: #F8FAFC;
        border-left: 3px solid var(--accent);
        padding: 1rem 1.25rem;
        border-radius: 0 8px 8px 0;
        font-style: italic;
        color: #475569;
    }

    /* Confidence gauge */
    .gauge-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 1rem;
    }

    /* Header */
    .app-header {
        background: #0D9488;
        margin: -1.5rem -1rem 1.5rem -1rem;
        padding: 1.25rem 2rem;
        border-bottom: 1px solid #0F766E;
        color: white;
    }

    .app-header h1 {
        margin: 0;
        font-size: 1.5rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .app-header p {
        margin: 0.375rem 0 0 0;
        opacity: 0.85;
        font-size: 0.875rem;
    }

    /* Divider */
    .divider {
        height: 1px;
        background: var(--border);
        margin: 1rem 0;
    }

    /* Section headers */
    .section-header {
        font-size: 0.8rem;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #F1F5F9;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb {
        background: #CBD5E1;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #94A3B8;
    }

    /* Charts container */
    .chart-container {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 1rem;
    }

    /* Animation */
    .fade-in {
        animation: fadeIn 0.3s ease-in;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Entity list */
    .entity-list {
        display: flex;
        flex-wrap: wrap;
        gap: 0.375rem;
    }

    .entity-item {
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
        padding: 0.25rem 0.5rem;
        background: #F0FDFA;
        border: 1px solid #99F6E4;
        border-radius: 6px;
        font-size: 0.75rem;
        color: #0F766E;
    }

    .entity-type {
        font-weight: 500;
        text-transform: uppercase;
        font-size: 0.625rem;
        color: #5EEAD4;
    }

    /* Loading skeleton */
    .skeleton {
        background: linear-gradient(90deg, #F1F5F9 25%, #E2E8F0 50%, #F1F5F9 75%);
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
        border-radius: 4px;
    }

    @keyframes shimmer {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
</style>
"""

# SVG Logo
LOGO_SVG = """
<svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="32" height="32" rx="8" fill="url(#grad)"/>
  <path d="M8 12L12 8L16 12L20 8L24 12" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M8 20L12 16L16 20L20 16L24 20" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" opacity="0.6"/>
  <defs>
    <linearGradient id="grad" x1="0" y1="0" x2="32" y2="32" gradientUnits="userSpaceOnUse">
      <stop stop-color="#0D9488"/>
      <stop offset="1" stop-color="#0F766E"/>
    </linearGradient>
  </defs>
</svg>
"""


def header(title: str = "Ticket Intel", subtitle: str = "") -> str:
    sub = f"<p>{subtitle}</p>" if subtitle else ""
    return f'<div class="app-header"><h1>{LOGO_SVG} {title}</h1>{sub}</div>'


def metric_card(
    label: str, value: str, delta: str = None, icon: str = "", color: str = "teal"
) -> str:
    delta_class = (
        "positive"
        if delta and delta.startswith("+")
        else "negative"
        if delta and delta.startswith("-")
        else "neutral"
    )
    delta_html = f'<div class="card-delta {delta_class}">{delta}</div>' if delta else ""
    icon_html = f'<div class="metric-icon {color}">{icon}</div>' if icon else ""
    return f'<div class="card"><div class="metric-card">{icon_html}<div><div class="card-header">{label}</div><div class="card-value">{value}</div>{delta_html}</div></div></div>'


def status_badge(status: str = "active", text: str = "Model Ready") -> str:
    return f'<div class="status-badge {status}"><span class="status-dot"></span>{text}</div>'


def sentiment_badge(sentiment: str) -> str:
    icons = {"positive": "↑", "negative": "↓", "neutral": "→"}
    return f'<div class="sentiment-badge {sentiment}"><span>{icons.get(sentiment, "→")}</span>{sentiment.title()}</div>'


def tag(text: str, color: str = "gray") -> str:
    return f'<span class="tag {color}">{text}</span>'


def entity_pill(text: str, entity_type: str) -> str:
    return f'<span class="entity-item"><span class="entity-type">{entity_type}</span>{text}</span>'


def quote_box(text: str) -> str:
    return f'<div class="quote-box">{text}</div>'


def section_header(text: str, icon: str = "") -> str:
    return f'<div class="section-header">{icon} {text}</div>'


def info_box(text: str, color: str = "teal") -> str:
    return f'<div class="info-box {color}">{text}</div>'
