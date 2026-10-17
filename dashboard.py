
import json
from pathlib import Path

import pandas as pd
import streamlit as st






# ---------- Professional Curated Feed Styling ----------
st.markdown("""
<style>
/* Feed container spacing */
.feed-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin: 24px 0 18px 0;
    flex-wrap: wrap;
}

.feed-title {
    font-size: 1.65rem;
    font-weight: 750;
    color: #f1f5f9;
    margin: 0;
}

.feed-subtitle {
    color: #94a3b8;
    font-size: 0.9rem;
    margin-top: 5px;
}

.feed-card {
    background: linear-gradient(135deg, #111c31 0%, #0c1729 100%);
    border: 1px solid #263750;
    border-left: 4px solid #3288f5;
    border-radius: 12px;
    padding: 16px 18px;
    margin: 10px 0;
    transition: border-color 0.2s ease;
}

.feed-card:hover {
    border-color: #398bff;
    border-left-color: #60a5fa;
}

.feed-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 10px;
}

.feed-badge {
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 750;
    letter-spacing: 0.35px;
    padding: 5px 10px;
    border-radius: 20px;
}

.badge-trending {
    background: #48202b;
    color: #ff9aa8;
    border: 1px solid #853749;
}

.badge-potential {
    background: #34245b;
    color: #c7b5ff;
    border: 1px solid #6245a1;
}

.badge-discovery {
    background: #12375b;
    color: #8bc9ff;
    border: 1px solid #205b8b;
}

.feed-score {
    color: #cbd5e1;
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 5px 9px;
    font-size: 0.78rem;
    font-weight: 700;
    white-space: nowrap;
}

.feed-story-title {
    font-size: 1.02rem;
    font-weight: 650;
    line-height: 1.6;
    margin: 0;
    overflow-wrap: anywhere;
}

.feed-story-title a {
    color: #e2e8f0 !important;
    text-decoration: none !important;
}

.feed-story-title a:hover {
    color: #60a5fa !important;
    text-decoration: underline !important;
}

.feed-meta {
    color: #94a3b8;
    font-size: 0.8rem;
    margin-top: 8px;
}

@media (max-width: 640px) {
    .feed-card {
        padding: 13px;
    }

    .feed-title {
        font-size: 1.35rem;
    }

    .feed-story-title {
        font-size: 0.95rem;
    }
}
</style>
""", unsafe_allow_html=True)


PROJECT_DIR = Path(__file__).resolve().parent
REPORTS_DIR = PROJECT_DIR / "reports"
HISTORY_FILE = REPORTS_DIR / "trend-history.json"

st.set_page_config(
    page_title="AI Trend Radar | CEO Intelligence",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Styling ----------
st.markdown("""
<style>
    .stApp {
        background: #0b1020;
        color: #edf2ff;
    }
    [data-testid="stSidebar"] {
        background: #111a2e;
        border-right: 1px solid #26334d;
    }
    .hero {
        padding: 24px 28px;
        border: 1px solid #293957;
        border-radius: 18px;
        background: linear-gradient(120deg, #172747, #111827);
        margin-bottom: 24px;
    }
    .hero-label {
        color: #8ea8d8;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
    }
    .hero h1 {
        color: #ffffff;
        font-size: 34px;
        margin: 8px 0;
    }
    .hero p {
        color: #b7c6df;
        margin-bottom: 0;
    }
    div[data-testid="stMetric"] {
        background: #121d33;
        border: 1px solid #293957;
        padding: 18px;
        border-radius: 14px;
    }
    div[data-testid="stMetricLabel"] {
        color: #a8bbdc;
    }
    div[data-testid="stMetricValue"] {
        color: #ffffff;
    }
    h2, h3 {
        color: #f1f5ff;
    }
    .section-note {
        color: #9eafcc;
        font-size: 13px;
    }
    div[data-testid="stExpander"] {
        border: 1px solid #293957;
        border-radius: 10px;
    }
    
   /* CEO-ready polish */
   .block-container {
       max-width: 1500px;
       padding-top: 2rem;
       padding-bottom: 3rem;
   }

   .hero {
       padding: 32px;
       border: 1px solid #304568;
       border-radius: 20px;
       background:
           radial-gradient(ellipse at top right, #263d66 0%, transparent 55%),
           linear-gradient(120deg, #172747, #101727);
       box-shadow: 0 12px 35px rgba(0, 0, 0, 0.18);
   }

   .hero h1 {
       font-size: clamp(30px, 3vw, 42px);
       font-weight: 750;
       letter-spacing: -1px;
   }

   .section-note {
       line-height: 1.7;
   }

   .tool-card {
       background: linear-gradient(145deg, #15233b, #101827);
       border: 1px solid #2b3d5c;
       border-radius: 15px;
       padding: 20px;
       min-height: 190px;
       margin-bottom: 14px;
       transition: border-color 0.2s ease, transform 0.2s ease;
   }

   .tool-card:hover {
       border-color: #7298d8;
       transform: translateY(-2px);
   }

   .tool-category {
       color: #9bb9ee;
       font-size: 11px;
       font-weight: 700;
       letter-spacing: 1.4px;
       text-transform: uppercase;
       margin-bottom: 10px;
   }

   .tool-card h4 {
       color: #f5f8ff;
       font-size: 19px;
       margin: 0 0 9px 0;
   }

   .tool-card p {
       color: #b7c6df;
       font-size: 13px;
       line-height: 1.65;
       min-height: 42px;
   }

   .tool-card a {
       color: #9dc2ff;
       font-size: 13px;
       font-weight: 650;
       text-decoration: none;
   }

   .tool-card a:hover {
       text-decoration: underline;
   }

   div[data-testid="stDataFrame"] {
       border: 1px solid #293957;
       border-radius: 12px;
       overflow: hidden;
   }

   div[data-testid="stExpander"] {
       background: #101827;
       border: 1px solid #293957;
       border-radius: 12px;
       margin-bottom: 8px;
   }

   /* ---------- Final CEO dashboard polish ---------- */

   .block-container {
       max-width: 1500px;
       padding-top: 2rem;
       padding-bottom: 3rem;
   }

   div[data-testid="stMetric"] {
       min-height: 132px;
       display: flex;
       flex-direction: column;
       justify-content: center;
       background: linear-gradient(145deg, #15223a, #111a2d);
       border: 1px solid #2b3d5c;
       padding: 20px;
       border-radius: 16px;
       box-shadow: 0 5px 18px rgba(0, 0, 0, 0.12);
   }

   div[data-testid="stMetricLabel"] {
       font-size: 14px;
       font-weight: 600;
       color: #b8c9e5;
   }

   div[data-testid="stMetricValue"] {
       font-size: 30px;
       font-weight: 700;
       color: #ffffff;
   }

   h2, h3 {
       letter-spacing: -0.3px;
       font-weight: 700;
   }

   div[data-testid="stDataFrame"] {
       border: 1px solid #293957;
       border-radius: 12px;
       overflow: hidden;
   }

   div[data-testid="stExpander"] {
       border: 1px solid #293957;
       border-radius: 12px;
       margin-bottom: 8px;
   }

   .section-note {
       color: #a9bddb;
       font-size: 14px;
       line-height: 1.7;
   }

</style>
""", unsafe_allow_html=True)


# ---------- Load historical data ----------
@st.cache_data
def load_history(file_path, modified_time):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


st.sidebar.title("📡 Trend Radar")
st.sidebar.caption("Executive Intelligence")
st.sidebar.divider()

if not HISTORY_FILE.exists():
    st.warnin("Trend history not found. Run ai_trend_radar.py first.")
    st.stop()

history = load_history(
    str(HISTORY_FILE),
    HISTORY_FILE.stat().st_mtime,
)

if not history:
    st.warning("Trend history is empty.")
    st.stop()

dates = sorted(history.keys())

st.sidebar.subheader("Report Controls")
selected_date = st.sidebar.selectbox(
    "Report date",
    dates,
    index=len(dates) - 1,
)

if st.sidebar.button("↻ Refresh data", use_container_width=True):
    st.cache_data.clear()
    st.rerun()

selected_index = dates.index(selected_date)
previous_date = dates[selected_index - 1] if selected_index > 0 else None

current = history[selected_date]
previous = history.get(previous_date, {}) if previous_date else {}

current_trends = current.get("trend_counts", {})
previous_trends = previous.get("trend_counts", {})

stories = current.get("top_stories", [])
total_stories = current.get("stories_collected", 0)
generated_at = current.get("generated_at", "Unknown")


import streamlit as st
import pandas as pd


def show_executive_summary(stories):
    """
    Display executive metric tiles for today's AI stories.

    stories: pandas DataFrame or list of story dictionaries.
    Required fields: score and descendants (comment count).
    """

    # Convert input into a DataFrame
    if isinstance(stories, pd.DataFrame):
        df = stories.copy()
    else:
        df = pd.DataFrame(stories)

    # Handle empty data safely
    if df.empty:
        st.info("No AI stories found for today.")
        return

    # Ensure expected numeric columns exist
    if "score" not in df.columns:
        df["score"] = 0

    if "descendants" not in df.columns:
        df["descendants"] = 0

    df["score"] = pd.to_numeric(
        df["score"], errors="coerce"
    ).fillna(0)

    df["descendants"] = pd.to_numeric(
        df["descendants"], errors="coerce"
    ).fillna(0)

    # Calculate metrics
    total_stories = len(df)

    high_hype_signals = int(
        (df["score"] > 200).sum()
    )

    # Define high comment count as 100+ comments
    potential_breakthroughs = int(
        (df["descendants"] >= 100).sum()
    )

    # Executive section
    st.markdown("## Executive Summary")
    st.caption(
        "Daily AI intelligence snapshot · Updated from collected stories"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="AI Stories Today",
            value=total_stories,
            help="Total AI-related stories collected for this report."
        )

    with col2:
        st.metric(
            label="High-Hype Signals",
            value=high_hype_signals,
            help="Stories with a Hacker News score above 200."
        )

    with col3:
        st.metric(
            label="Potential Breakthroughs",
            value=potential_breakthroughs,
            help="Stories with at least 100 comments."
        )

    st.divider()

# ---------- Header ----------
st.markdown(f"""
<div class="hero">
    <div class="hero-label">EXECUTIVE INTELLIGENCE PLATFORM</div>
    <h1>AI Trend Radar</h1>
    <p>Technology signals, emerging trends and daily intelligence.</p>
    <p>Report date: {selected_date} &nbsp; | &nbsp; Generated: {generated_at}</p>
</div>
""", unsafe_allow_html=True)


# ---------- Executive Summary Metric Tiles ----------
st.subheader("Executive Summary")
st.caption(
    f"Daily intelligence snapshot for {selected_date}"
)

# Total stories collected for the selected report
executive_total = int(total_stories or 0)

# Analyze stories saved in the selected report
executive_stories = pd.DataFrame(stories or [])

if not executive_stories.empty:
    # High-Hype Signals: score greater than 200
    if "score" in executive_stories.columns:
        scores = pd.to_numeric(
            executive_stories["score"],
            errors="coerce"
        ).fillna(0)

        high_hype = int((scores > 200).sum())
    else:
        high_hype = 0

    # Potential Breakthroughs: 100 or more comments
    comment_column = next(
        (
            col for col in ["descendants", "comment_count", "comments"]
            if col in executive_stories.columns
        ),
        None
    )

    if comment_column:
        comments = pd.to_numeric(
            executive_stories[comment_column],
            errors="coerce"
        ).fillna(0)

        breakthroughs = int((comments >= 100).sum())
        breakthrough_value = breakthroughs
    else:
        breakthrough_value = "N/A"
else:
    high_hype = 0
    breakthrough_value = "N/A"

tile1, tile2, tile3 = st.columns(3)

with tile1:
    st.metric(
        "AI Stories Today",
        executive_total
    )

with tile2:
    st.metric(
        "High-Hype Signals",
        high_hype
    )

with tile3:
    st.metric(
        "Potential Breakthroughs",
        breakthrough_value
    )

if breakthrough_value == "N/A":
    st.caption(
        "Comment counts are not available in the saved story data."
    )

st.divider()
# ---------- End Executive Summary ----------

# ---------- KPI cards ----------
total_trends = len(current_trends)
top_trend = (
    max(current_trends, key=current_trends.get)
    if current_trends else None
)
top_count = current_trends.get(top_trend, 0) if top_trend else 0

previous_total = previous.get("stories_collected") if previous else None

k1, k2, k3, k4 = st.columns(4)


k1.metric(
    "Stories Collected",
    total_stories,
    delta=(
        total_stories - previous_total
        if previous_total is not None else None
    ),
    delta_description="vs previous report",
)


k2.metric("Tracked Trends", total_trends)

k3.metric(
    "Leading Trend",
    top_trend.upper() if top_trend else "N/A",
)

k4.metric("Leading Trend Count", top_count)

st.divider()


# ---------- Trend analysis ----------
st.subheader("📊 Trend Intelligence")
st.markdown(
    '<p class="section-note">Tracked keyword frequency in collected stories.</p>',
    unsafe_allow_html=True,
)

if current_trends:
    trend_rows = []

    for trend in set(current_trends) | set(previous_trends):
        today_count = current_trends.get(trend, 0)
        previous_count = previous_trends.get(trend, 0)

        trend_rows.append({
            "Trend": trend.upper(),
            "Selected date": today_count,
            "Previous recorded date": previous_count if previous_date else 0,
            "Change": today_count - previous_count if previous_date else None,
        })

    comparison = pd.DataFrame(trend_rows).sort_values(
        "Selected date", ascending=False
    )

    left, right = st.columns([1.2, 1])

    with left:
        st.markdown("#### Trend frequency")
        chart = comparison.set_index("Trend")[["Selected date"]]
        st.bar_chart(chart, height=340)

    with right:
        st.markdown("#### Trend movement")
        if previous_date:
            movement = comparison[
                ["Trend", "Selected date", "Previous recorded date", "Change"]
            ].copy()
            st.dataframe(
                movement,
                hide_index=True,
                use_container_width=True,
            )
        else:
            st.info(
                "Daily movement will appear after a second date is recorded."
            )
            st.dataframe(
                comparison[["Trend", "Selected date"]],
                hide_index=True,
                use_container_width=True,
            )
else:
    st.info("No tracked trends found for this report.")

st.divider()



# ---------- Executive summary ----------
st.subheader("🧠 Executive Brief")
st.markdown(
    '<p class="section-note">'
    'A concise view of the latest recorded technology signals '
    'and how they compare with the previous report.'
    '</p>',
    unsafe_allow_html=True,
)

if not current_trends:
    st.info("No tracked trends were detected in this report.")
else:
    st.markdown(
        f"**Leading trend:** {top_trend.upper()} — "
        f"mentioned in **{top_count} tracked story matches**."
    )

    if previous_date:
        increases = [
            trend.upper()
            for trend in current_trends
            if current_trends.get(trend, 0)
            > previous_trends.get(trend, 0)
        ]

        decreases = [
            trend.upper()
            for trend in previous_trends
            if previous_trends.get(trend, 0)
            > current_trends.get(trend, 0)
        ]

        new_trends = [
            trend.upper()
            for trend in current_trends
            if trend not in previous_trends
        ]

        s1, s2, s3 = st.columns(3)

        s1.metric("Trends Increasing", len(increases))
        s2.metric("Trends Decreasing", len(decreases))
        s3.metric("Newly Detected Trends", len(new_trends))

        with st.container(border=True):
            st.markdown("**Key changes since previous report**")

            st.write(
                "**Increasing:** "
                + (", ".join(increases) or "No increases recorded")
            )
            st.write(
                "**Decreasing:** "
                + (", ".join(decreases) or "No decreases recorded")
            )
            st.write(
                "**New:** "
                + (", ".join(new_trends) or "No newly detected trends")
            )

            st.caption(
                f"Comparison: {previous_date} → {selected_date}. "
                "Changes reflect tracked keyword counts, not necessarily "
                "changes in real-world market adoption."
            )
    else:
        st.info(
            "A previous report is needed to calculate daily trend movement."
        )


# ---------- Top stories ----------
st.subheader("📰 Top Stories")
st.markdown(
    '<p class="section-note">Ranked by the current relevance score.</p>',
    unsafe_allow_html=True,
)

if not stories:
    st.info("No stories saved for this date.")
else:
    for index, story in enumerate(stories, start=1):
        title = story.get("title", "Untitled")
        url = story.get("url", "")
        score = story.get("score", 0)
        keywords = story.get("matched_keywords", [])

        with st.expander(f"{index}. {title}  |  Score: {score}"):
            st.write("**Matched topics:** " + (
                ", ".join(keywords) if keywords else "General technology"
            ))
       

# ---------- Professional Curated AI Feed ----------
st.markdown("""
<div class="feed-header">
    <div>
        <div class="feed-title">📡 Curated AI Feed</div>
        <div class="feed-subtitle">
            Latest stories from Hacker News, classified by score
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

if not stories:
    st.info("No stories available for this report.")
else:
    for story in stories:
        title = story.get("title", "Untitled")
        url = story.get("url", "#")

        try:
            score = int(float(story.get("score", 0) or 0))
        except (ValueError, TypeError):
            score = 0

        if score > 300:
            badge_text = "🔥 TRENDING"
            badge_class = "badge-trending"
            border_color = "#f97316"
        elif score >= 150:
            badge_text = "💎 HIGH POTENTIAL"
            badge_class = "badge-potential"
            border_color = "#8b5cf6"
        else:
            badge_text = "📚 MARKET DISCOVERY"
            badge_class = "badge-discovery"
            border_color = "#3288f5"

        # Prevent story text from being interpreted as HTML
        safe_title = (str(title)
                      .replace("&", "&amp;")
                      .replace("<", "&lt;")
                      .replace(">", "&gt;")
                      .replace('"', "&quot;"))

        # Only create a clickable link for HTTP(S) URLs
        safe_url = str(url)
        if safe_url.startswith(("https://", "http://")):
            import html
            safe_url = html.escape(safe_url, quote=True)
            title_html = (
                f'<a href="{safe_url}" target="_blank" '
                f'rel="noopener noreferrer">{safe_title} ↗</a>'
            )
        else:
            title_html = safe_title

        st.markdown(f"""
        <div class="feed-card" style="border-left-color: {border_color};">
            <div class="feed-top">
                <span class="feed-badge {badge_class}">
                    {badge_text}
                </span>
                <span class="feed-score">HN Score: {score}</span>
            </div>
            <p class="feed-story-title">{title_html}</p>
            <div class="feed-meta">
                Hacker News &nbsp; • &nbsp; AI &amp; Technology
            </div>
        </div>
        """, unsafe_allow_html=True)



# ---------- Popular AI Tools ----------
st.divider()

st.subheader("🚀 Popular AI Tools")
st.markdown(
    '<p class="section-note">'
    'A curated directory of widely used AI platforms, '
    'organized by practical use case. This is not a live popularity ranking.'
    '</p>',
    unsafe_allow_html=True,
)

ai_tools = [
    {
        "name": "ChatGPT",
        "category": "AI ASSISTANT",
        "description": "Writing, brainstorming, analysis, and everyday productivity.",
        "url": "https://chatgpt.com/",
    },
    {
        "name": "Claude",
        "category": "REASONING & WRITING",
        "description": "Long-form writing, document analysis, and coding assistance.",
        "url": "https://claude.ai/",
    },
    {
        "name": "Google Gemini",
        "category": "AI ASSISTANT",
        "description": "Multimodal assistance and workflows across Google's ecosystem.",
        "url": "https://gemini.google.com/",
    },
    {
        "name": "Perplexity",
        "category": "AI RESEARCH",
        "description": "Web research and answers with linked sources.",
        "url": "https://www.perplexity.ai/",
    },
    {
        "name": "GitHub Copilot",
        "category": "AI CODING",
        "description": "Coding assistance, code completion, and developer workflows.",
        "url": "https://github.com/features/copilot",
    },
    {
        "name": "Cursor",
        "category": "AI CODE EDITOR",
        "description": "AI-assisted coding, codebase understanding, and development.",
        "url": "https://cursor.com/",
    },
    {
        "name": "NotebookLM",
        "category": "RESEARCH & NOTES",
        "description": "Research and summaries grounded in your provided sources.",
        "url": "https://notebooklm.google.com/",
    },
    {
        "name": "Midjourney",
        "category": "IMAGE GENERATION",
        "description": "Create visual concepts and images from text prompts.",
        "url": "https://www.midjourney.com/",
    },
    {
        "name": "Runway",
        "category": "AI VIDEO",
        "description": "AI-powered video creation and visual editing workflows.",
        "url": "https://runwayml.com/",
    },
    {
        "name": "ElevenLabs",
        "category": "AI AUDIO",
        "description": "Voice generation, text-to-speech, and audio tools.",
        "url": "https://elevenlabs.io/",
    },
    {
        "name": "Canva AI",
        "category": "DESIGN",
        "description": "Design, presentations, and AI-assisted creative content.",
        "url": "https://www.canva.com/",
    },
    {
        "name": "Hugging Face",
        "category": "AI MODELS",
        "description": "Explore AI models, datasets, and machine-learning demos.",
        "url": "https://huggingface.co/",
    },
]

category_filter = st.selectbox(
    "Filter tools by category",
    ["All categories"] + sorted(
        {tool["category"] for tool in ai_tools}
    ),
    key="ai_tools_category",
)

filtered_tools = [
    tool for tool in ai_tools
    if category_filter == "All categories"
    or tool["category"] == category_filter
]

tool_columns = st.columns(3)

for index, tool in enumerate(filtered_tools):
    with tool_columns[index % 3]:
        st.markdown(
            f"""
            <div class="tool-card">
                <div class="tool-category">{tool["category"]}</div>
                <h4>{tool["name"]}</h4>
                <p>{tool["description"]}</p>
                <a href="{tool["url"]}" target="_blank"
                   rel="noopener noreferrer">
                    Visit official website ↗
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.caption(
    "AI Tools Directory · Curated reference list · "
    "Categories describe typical use cases, not an endorsement."
)

# ---------- Signal vs Hype: AI Reality Check ----------
st.divider()

st.subheader("🔎 Signal vs Hype — AI Reality Check")
st.markdown(
    '<p class="section-note">'
    'Explore which AI trends show practical evidence and which need '
    'more validation. Assessments are preliminary signals, not proof '
    'of commercial success or failure.'
    '</p>',
    unsafe_allow_html=True,
)

# These terms are clues in story titles, not definitive proof.
evidence_terms = (
    "production", "deployed", "deployment", "benchmark",
    "case study", "released", "launch", "open source",
    "users", "customer", "revenue", "performance",
    "real-world", "in production", "available now",
)

hype_terms = (
    "agi", "revolutionary", "will replace", "game changer",
    "the future of", "human-level", "singularity",
)

assessments = []

for trend in sorted(current_trends):
    trend_stories = [
        story for story in stories
        if trend.lower() in [
            str(keyword).lower()
            for keyword in story.get("matched_keywords", [])
        ]
    ]

    titles = [
        str(story.get("title", "")).lower()
        for story in trend_stories
    ]

    evidence_hits = sum(
        any(term in title for term in evidence_terms)
        for title in titles
    )

    hype_hits = sum(
        any(term in title for term in hype_terms)
        for title in titles
    )

    story_count = current_trends.get(trend, 0)

    if evidence_hits > hype_hits and evidence_hits > 0:
        status = "Practical signal"
        explanation = (
            "Story titles contain implementation or evidence-related "
            "clues. Verify the original sources before drawing conclusions."
        )
        status_color = "#7ee0b8"
    elif hype_hits > evidence_hits and hype_hits > 0:
        status = "Hype risk"
        explanation = (
            "Story titles contain ambitious or promotional language. "
            "Look for independent results and working deployments."
        )
        status_color = "#ffbd7a"
    else:
        status = "Needs validation"
        explanation = (
            "The available titles do not provide enough evidence to "
            "classify this trend confidently."
        )
        status_color = "#a9c4ff"

    assessments.append({
        "trend": trend.upper(),
        "mentions": story_count,
        "status": status,
        "evidence_hits": evidence_hits,
        "hype_hits": hype_hits,
        "explanation": explanation,
        "color": status_color,
    })

if assessments:
    signal_count = sum(
        item["status"] == "Practical signal"
        for item in assessments
    )
    hype_count = sum(
        item["status"] == "Hype risk"
        for item in assessments
    )
    validation_count = sum(
        item["status"] == "Needs validation"
        for item in assessments
    )

    s1, s2, s3 = st.columns(3)
    s1.metric("Practical Signals", signal_count)
    s2.metric("Hype Risks", hype_count)
    s3.metric("Needs Validation", validation_count)

    st.markdown("#### Trend assessment")

    for item in assessments:
        with st.container(border=True):
            left, right = st.columns([1.5, 3])

            with left:
                st.markdown(f"**{item['trend']}**")
                st.caption(
                    f"{item['mentions']} tracked mentions"
                )
                st.markdown(
                    f"<span style='color:{item['color']};"
                    f"font-weight:700'>{item['status']}</span>",
                    unsafe_allow_html=True,
                )

            with right:
                st.write(item["explanation"])
                st.caption(
                    "Title clues only — "
                    f"implementation clues: {item['evidence_hits']} · "
                    f"ambitious-claim clues: {item['hype_hits']}"
                )

    st.info(
        "Important: This first version uses keyword matches and story "
        "titles only. A 'Practical signal' is not proof of adoption, "
        "and a 'Hype risk' is not proof that a technology is useless. "
        "Review linked stories and independent evidence before making "
        "business decisions."
    )
else:
    st.info(
        "No tracked trends are available for this report date."
    )
