
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from urllib.parse import quote
from collections import Counter

PROJECT_DIR = Path(__file__).resolve().parent
REPORTS_DIR = PROJECT_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

FEEDS = [
    ("Hacker News", "https://hnrss.org/frontpage"),
    ("GitHub Trending", "https://github.com/trending?since=daily"),
]


KEYWORDS = [
    "artificial intelligence",
    "ai",
    "llm",
    "llms",
    "large language model",
    "machine learning",
    "deep learning",
    "generative ai",
    "agent",
    "agents",
    "ai agent",
    "automation",
    "python",
    "javascript",
    "typescript",
    "react",
    "web development",
    "open source",
    "coding",
    "developer",
    "programming",
    "software",
    "github",
    "startup",
    "cybersecurity",
    "security",
    "malware",
    "robotics",
    "database",
    "postgres",
    "postgresql",
    "webassembly",
    "wasm",
    "browser",
    "cloud",
    "infrastructure",
    "technology",
]




import time

def fetch_url(url):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "AI-Trend-Radar/1.0"}
    )

    last_error = None

    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return response.read()
        except Exception as exc:
            last_error = exc
            print(f"Request attempt {attempt + 1}/3 failed: {exc}")

            if attempt < 2:
                time.sleep(2)

    raise last_error



def collect_hacker_news():
    items = []
    url = "https://hnrss.org/frontpage"

    try:
        root = ET.fromstring(fetch_url(url))
        for item in root.findall(".//item"):
            title = item.findtext("title", default="").strip()
            link = item.findtext("link", default="").strip()
            description = item.findtext("description", default="")
            if title and link:
                items.append({
                    "source": "Hacker News",
                    "title": title,
                    "url": link,
                    "description": re.sub(r"<[^>]+>", " ", description).strip(),
                })
    except Exception as exc:
        print(f"Hacker News fetch failed: {exc}")

    return items




HIGH_PRIORITY_KEYWORDS = {
    "ai agents",
    "llm",
    "llms",
    "malware",
    "vulnerability",
    "security vulnerability",
    "supply chain attack",
    "zero-day",
    "cve",
    "gpt",
    "claude",
    "open source ai",
}

MEDIUM_PRIORITY_KEYWORDS = {
    "artificial intelligence",
    "machine learning",
    "rag",
    "webassembly",
    "postgres",
    "postgresql",
    "react",
    "next.js",
    "typescript",
    "ai coding",
    "coding agents",
    "code generation",
}



def score_item(item):
    text = f"{item.get('title', '')} {item.get('description', '')}".lower()

    score = 0
    matched = []
    seen = set()

    high_priority = {
        keyword.strip().lower()
        for keyword in HIGH_PRIORITY_KEYWORDS
        if keyword.strip()
    }

    medium_priority = {
        keyword.strip().lower()
        for keyword in MEDIUM_PRIORITY_KEYWORDS
        if keyword.strip()
    }

    for keyword in KEYWORDS:
        clean_keyword = keyword.strip().lower()

        if not clean_keyword or clean_keyword in seen:
            continue

        seen.add(clean_keyword)

        pattern = (
            r"\bai\b"
            if clean_keyword == "ai"
            else r"\b" + re.escape(clean_keyword) + r"\b"
        )

        if re.search(pattern, text):
            if clean_keyword in high_priority:
                score += 3
            elif clean_keyword in medium_priority:
                score += 2
            else:
                score += 1

            matched.append(clean_keyword)

    item["score"] = score
    item["matched_keywords"] = sorted(matched)

    return item

    
def main():
    print("AI Trend Radar starting...")
    print("Collecting public Hacker News RSS feed...")

    items = collect_hacker_news()
    unique = {}

    for item in items:
        unique[item["url"]] = score_item(item)

   
    ranked = sorted(
        unique.values(),
        key=lambda item: (
            -item["score"],
            item["title"].lower()
        )
    )

  
    from collections import Counter

    TREND_KEYWORDS = {
        "ai", "llm", "llms", "gpt", "claude",
        "ai agents", "machine learning", 
        "malware", "vulnerability", "zero-day",
        "webassembly", "postgres", "postgresql",
        "react", "next.js", "typescript",
        "browser", "database performance",
        "open source ai", "coding agents",
    }

    trend_counts = Counter(
        keyword
        for item in ranked
        for keyword in set(item.get("matched_keywords", []))
        if keyword.lower() in TREND_KEYWORDS
    )

    timestamp = datetime.now().astimezone()
    date_label = timestamp.strftime("%Y-%m-%d")
    generated_label = timestamp.strftime("%Y-%m-%d %H:%M %Z")



    timestamp = datetime.now().astimezone()
    date_label = timestamp.strftime("%Y-%m-%d")
    generated_label = timestamp.strftime("%Y-%m-%d %H:%M %Z")

    report = [
        "# AI Trend Radar",
        "",
        f"- Generated: {generated_label}",
        f"- Stories collected: {len(ranked)}",
      
        "- Source: Hacker News public RSS",
        "",
        "## Top 5 Trends",
        "",
    ]

     
    display_names = {
        "ai": "AI",
        "llm": "LLM",
        "llms": "LLMs",
        "gpt": "GPT",
        "claude": "Claude",
        "webassembly": "WebAssembly",
        "next.js": "Next.js",
        "postgresql": "PostgreSQL",
    }

   
    for keyword, count in trend_counts.most_common(5):
        name = display_names.get(keyword.lower(), keyword.title())
        label = "story" if count == 1 else "stories"
        report.append(f"- **{name}** — {count} {label}")


    report.extend([
        "",
        "## Top stories",
        "",
    ])


    if not ranked:
        report.append(
            "No stories could be collected. Check your internet connection "
            "and run the script again."
        )

    for index, item in enumerate(ranked[:20], start=1):
       
        keywords = ", ".join(
            sorted(set(item.get("matched_keywords", [])))
        ) or "General technology"

        report.extend([
            f"### {index}. {item['title']}",
            f"- Relevance score: {item['score']}",
            f"- Topics: {keywords}",
            f"- Source: {item['source']}",
            f"- Link: {item['url']}",
            "",
        ])

    report_path = REPORTS_DIR / f"trend-report-{date_label}.md"
    json_path = REPORTS_DIR / f"trend-data-{date_label}.json"


    # Save daily trend history for dashboard comparisons
    history_path = REPORTS_DIR / "trend-history.json"

    if history_path.exists():
        try:
            history = json.loads(
                history_path.read_text(encoding="utf-8")
            )
        except (json.JSONDecodeError, OSError):
            history = {}
    else:

        history = {}

    history[date_label] = {
        "generated_at": timestamp.strftime(
            "%Y-%m-%d %H:%M Pakistan Standard Time"
        ),
        "stories_collected": len(ranked),
        "trend_counts": dict(trend_counts),
        "top_stories": [
            {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "score": item.get("score", 0),
                "matched_keywords": item.get(
                    "matched_keywords", []
                ),
            }
            for item in ranked[:20]
        ],
    }

    history_path.write_text(
        json.dumps(history, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    report_path.write_text("\n".join(report), encoding="utf-8")
    json_path.write_text(
        json.dumps(ranked, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    # Save daily trend history for comparisons
    history_path = REPORTS_DIR / "trend-history.json"

    history = {}

    if history_path.exists():
        try:
            history = json.loads(
                history_path.read_text(encoding="utf-8")
            )
        
        except (json.JSONDecodeError, OSError) as error:
            raise RuntimeError(
                f"Could not read trend history at {history_path}. "
                "Existing history was not overwritten."
            ) from error


    history[date_label] = {
        "generated_at": generated_label,
        "stories_collected": len(ranked),
        "trend_counts": dict(trend_counts),
        "top_stories": [
            {
                "title": item["title"],
                "url": item["url"],
                "score": item["score"],
                "matched_keywords": item.get("matched_keywords", []),
            }
            for item in ranked[:20]
        ],
    }

    history_path.write_text(
        json.dumps(history, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"Trend history: {history_path}")


    print(f"\nStories collected: {len(ranked)}")
    print(f"Markdown report: {report_path}")
    print(f"JSON data: {json_path}")
    print("\nAI Trend Radar finished.")


if __name__ == "__main__":
    main()
