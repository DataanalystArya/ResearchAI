"""
Streamlit UI for the multi-agent research pipeline defined in pipeline.py

Drop this file into your RESEARCHAI/ project root (next to pipeline.py, agents.py)
and run:
    streamlit run app.py
"""

import streamlit as st
import threading
import queue
import time
import html as html_lib

from pipeline import run_research_pipeline

# ----------------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Research Pipeline",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# Design tokens
# ----------------------------------------------------------------------------
BG = "#082567"               # Dark Sapphire
SURFACE = "#12357F"
SURFACE_RAISED = "#284E9A"
BORDER = "#5F84C7"

TEXT_PRIMARY = "#FFFFFF"
TEXT_SECONDARY = "#E5EEFF"
TEXT_MUTED = "#B6C8F0"

STAGES = [
    {
        "key": "search",
        "label": "Search Agent",
        "desc": "Scanning the web for recent, reliable sources",
        "color": "#4F9DDE",
        "marker": "step 1",
    },
    {
        "key": "reader",
        "label": "Reader Agent",
        "desc": "Opening the best source and extracting depth",
        "color": "#3FBF9F",
        "marker": "step 2",
    },
    {
        "key": "writer",
        "label": "Writer Chain",
        "desc": "Drafting a structured report from the research",
        "color": "#E0A94D",
        "marker": "step 3",
    },
    {
        "key": "critic",
        "label": "Critic Chain",
        "desc": "Reviewing the draft for gaps and weak claims",
        "color": "#D96C6C",
        "marker": "step 4",
    },
]

# ----------------------------------------------------------------------------
# Global styling
# ----------------------------------------------------------------------------
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    .stApp {{
        background: {BG};
        color: {TEXT_PRIMARY};
    }}

    section[data-testid="stSidebar"] {{
        background: {SURFACE};
        border-right: 1px solid {BORDER};
    }}

    section[data-testid="stSidebar"] * {{
        color: {TEXT_PRIMARY};
    }}

    h1, h2, h3 {{
        font-family: 'Space Grotesk', sans-serif;
        letter-spacing: -0.01em;
    }}

    /* Hide default streamlit chrome that clutters a product-feel UI */
    #MainMenu, footer {{ visibility: hidden; }}
    header[data-testid="stHeader"] {{
      background: transparent;
      visibility: visible;
}}
    div[data-testid="collapsedControl"] {{
      visibility: visible !important;
      display: flex !important;
}}

    /* Text input / textarea restyle */
    .stTextInput input, .stTextArea textarea {{
        background: {SURFACE_RAISED} !important;
        color: {TEXT_PRIMARY} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif;
    }}
    .stTextInput input:focus, .stTextArea textarea:focus {{
        border-color: #4F9DDE !important;
        box-shadow: none !important;
    }}

    /* Buttons */
    /* Buttons */
.stButton > button {{
    background: #D9534F !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px;
    font-weight: 600;
    padding: 0.55rem 1.2rem;
    transition: opacity 0.15s ease;
    width: 100%;
}}
.stButton > button:hover,
.stButton > button:active,
.stButton > button:focus {{
    background: #C4433F !important;
    color: #FFFFFF !important;
    opacity: 1;
}}

    /* Secondary / reset button variant */
    .reset-btn button {{
        background: transparent !important;
        color: {TEXT_SECONDARY} !important;
        border: 1px solid {BORDER} !important;
    }}

    /* Expander restyle */
    .streamlit-expanderHeader {{
        background: {SURFACE_RAISED} !important;
        color: {TEXT_PRIMARY} !important;
        border-radius: 8px !important;
        border: 1px solid {BORDER} !important;
        font-family: 'Space Grotesk', sans-serif;
    }}
    .streamlit-expanderContent {{
        background: {SURFACE} !important;
        border: 1px solid {BORDER} !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
    }}

    /* Divider */
    hr {{ border-color: {BORDER}; }}

    /* Header block */
    .app-eyebrow {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: {TEXT_MUTED};
        margin-bottom: 0.3rem;
    }}
    .app-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.1rem;
        font-weight: 700;
        margin: 0 0 0.35rem 0;
        color: {TEXT_PRIMARY};
    }}
    .app-subtitle {{
        color: {TEXT_SECONDARY};
        font-size: 0.98rem;
        margin-bottom: 1.6rem;
        max-width: 640px;
        line-height: 1.5;
    }}

    /* Pipeline rail */
    .rail {{
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        background: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 28px 32px;
        margin-bottom: 28px;
    }}
    .rail-node {{
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        flex: 1;
        position: relative;
    }}
    .rail-dot {{
        width: 16px;
        height: 16px;
        border-radius: 50%;
        margin-bottom: 12px;
        border: 2px solid {BORDER};
        background: {SURFACE_RAISED};
        transition: all 0.3s ease;
        z-index: 2;
    }}
    .rail-line {{
        position: absolute;
        top: 7px;
        left: 50%;
        width: 100%;
        height: 2px;
        background: {BORDER};
        z-index: 1;
    }}
    .rail-label {{
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        font-size: 0.88rem;
        margin-bottom: 4px;
    }}
    .rail-desc {{
        font-size: 0.76rem;
        color: {TEXT_MUTED};
        max-width: 150px;
        line-height: 1.35;
    }}
    .rail-status {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 6px;
    }}

    /* Terminal / log console */
    .terminal {{
        background: #0D0F12;
        border: 1px solid {BORDER};
        border-radius: 10px;
        padding: 18px 20px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        line-height: 1.55;
        color: #A9E8C8;
        max-height: 320px;
        overflow-y: auto;
        white-space: pre-wrap;
        word-break: break-word;
    }}

    /* Result cards */
    .card {{
        background: {SURFACE};
        border: 1px solid {BORDER};
        border-left: 3px solid var(--accent, #4F9DDE);
        border-radius: 10px;
        padding: 20px 22px;
        margin-bottom: 18px;
    }}
    .card-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 4px;
    }}
    .card-body {{
        color: {TEXT_SECONDARY};
        font-size: 0.88rem;
        line-height: 1.6;
        white-space: pre-wrap;
    }}

    .report-card {{
        background: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 12px;
        padding: 30px 34px;
        line-height: 1.7;
        font-size: 0.96rem;
        color: {TEXT_PRIMARY};
    }}

    .empty-state {{
        border: 1px dashed {BORDER};
        border-radius: 14px;
        padding: 60px 40px;
        text-align: center;
        color: {TEXT_MUTED};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Session state
# ----------------------------------------------------------------------------
if "result" not in st.session_state:
    st.session_state.result = None
if "ran_topic" not in st.session_state:
    st.session_state.ran_topic = ""

# ----------------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ◆ Research Pipeline")
    st.markdown(
        f"<div style='color:{TEXT_SECONDARY}; font-size:0.85rem; margin-bottom:1.4rem;'>"
        "A four-agent chain that searches, reads, writes, and critiques a report "
        "on any topic you give it."
        "</div>",
        unsafe_allow_html=True,
    )

    topic_input = st.text_area(
        "Research topic",
        placeholder="e.g. The current state of solid-state batteries",
        height=100,
        key="topic_input",
    )

    run_clicked = st.button("Run pipeline", type="primary")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='font-family:JetBrains Mono, monospace; font-size:0.7rem; "
        f"text-transform:uppercase; letter-spacing:0.08em; color:{TEXT_MUTED}; margin-bottom:10px;'>"
        "The four agents</div>",
        unsafe_allow_html=True,
    )
    for s in STAGES:
        st.markdown(
            f"""
            <div style="display:flex; align-items:flex-start; gap:10px; margin-bottom:14px;">
                <div style="width:9px; height:9px; border-radius:50%; background:{s['color']}; margin-top:5px; flex-shrink:0;"></div>
                <div>
                    <div style="font-weight:600; font-size:0.83rem; color:{TEXT_PRIMARY};">{s['label']}</div>
                    <div style="font-size:0.76rem; color:{TEXT_MUTED}; line-height:1.4;">{s['desc']}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.session_state.result is not None:
        st.markdown("<div class='reset-btn'>", unsafe_allow_html=True)
        if st.button("Clear results"):
            st.session_state.result = None
            st.session_state.ran_topic = ""
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------------
st.markdown("<div class='app-eyebrow'>Multi-agent research system</div>", unsafe_allow_html=True)
st.markdown("<div class='app-title'>Ask it something. Watch it work.</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='app-subtitle'>Each run passes your topic through four agents in sequence — "
    "search, read, write, critique — and shows the reasoning behind the final report.</div>",
    unsafe_allow_html=True,
)


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def detect_active_stage(log_text: str) -> int:
    """Return the index of the furthest stage mentioned so far in the logs."""
    lowered = log_text.lower()
    idx = -1
    for i, s in enumerate(STAGES):
        if s["marker"] in lowered:
            idx = i
    return idx


def render_rail(active_idx: int, finished: bool = False) -> str:
    nodes = []
    for i, s in enumerate(STAGES):
        if finished:
            dot_style = f"background:{s['color']}; border-color:{s['color']};"
            status_text = "Done"
            status_color = s["color"]
        elif i < active_idx:
            dot_style = f"background:{s['color']}; border-color:{s['color']};"
            status_text = "Done"
            status_color = s["color"]
        elif i == active_idx:
            dot_style = f"background:{s['color']}; border-color:{s['color']}; box-shadow:0 0 0 4px {s['color']}33;"
            status_text = "Working..."
            status_color = s["color"]
        else:
            dot_style = ""
            status_text = "Pending"
            status_color = TEXT_MUTED

        line = f"<div class='rail-line'></div>" if i < len(STAGES) - 1 else ""
        nodes.append(
            f"""
            <div class="rail-node">
                {line}
                <div class="rail-dot" style="{dot_style}"></div>
                <div class="rail-label">{s['label']}</div>
                <div class="rail-desc">{s['desc']}</div>
                <div class="rail-status" style="color:{status_color};">{status_text}</div>
            </div>
            """
        )
    return f"<div class='rail'>{''.join(nodes)}</div>"


class _QueueWriter:
    """Redirect target so print() calls inside the pipeline stream into the UI."""

    def __init__(self, q: queue.Queue):
        self.q = q

    def write(self, msg):
        if msg:
            self.q.put(msg)

    def flush(self):
        pass


def _run_pipeline_in_thread(topic: str, q: queue.Queue, result_holder: dict):
    import sys

    original_stdout = sys.stdout
    sys.stdout = _QueueWriter(q)
    try:
        result_holder["data"] = run_research_pipeline(topic)
    except Exception as exc:  # surface pipeline errors in the UI instead of crashing
        result_holder["error"] = str(exc)
    finally:
        sys.stdout = original_stdout
        result_holder["done"] = True


def render_result_card(title: str, body: str, color: str):
    safe_body = html_lib.escape(body or "No content returned.")
    st.markdown(
        f"""
        <div class="card" style="--accent:{color};">
            <div class="card-title" style="color:{color};">{title}</div>
            <div class="card-body">{safe_body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------------
# Run pipeline
# ----------------------------------------------------------------------------
if run_clicked:
    if not topic_input or not topic_input.strip():
        st.warning("Enter a topic before running the pipeline.")
    else:
        topic = topic_input.strip()
        q: queue.Queue = queue.Queue()
        result_holder: dict = {}

        thread = threading.Thread(
            target=_run_pipeline_in_thread, args=(topic, q, result_holder), daemon=True
        )
        thread.start()

        rail_placeholder = st.empty()
        log_placeholder = st.empty()

        log_text = ""
        active_idx = -1

        while thread.is_alive() or not q.empty():
            drained = False
            while True:
                try:
                    log_text += q.get_nowait()
                    drained = True
                except queue.Empty:
                    break
            if drained:
                active_idx = detect_active_stage(log_text)

            rail_placeholder.markdown(render_rail(active_idx), unsafe_allow_html=True)
            log_placeholder.markdown(
                f"<div class='terminal'>{html_lib.escape(log_text) or 'Waking up the agents...'}</div>",
                unsafe_allow_html=True,
            )
            time.sleep(0.2)

        thread.join()
        rail_placeholder.markdown(render_rail(len(STAGES), finished=True), unsafe_allow_html=True)

        if "error" in result_holder:
            st.error(f"The pipeline hit an error: {result_holder['error']}")
        else:
            st.session_state.result = result_holder.get("data")
            st.session_state.ran_topic = topic

# ----------------------------------------------------------------------------
# Results
# ----------------------------------------------------------------------------
if st.session_state.result:
    state = st.session_state.result

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='app-eyebrow'>Report on</div>"
        f"<div class='app-title' style='font-size:1.5rem;'>{html_lib.escape(st.session_state.ran_topic)}</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
    st.markdown("##### Final report")
    st.markdown(
        f"<div class='report-card'>{html_lib.escape(state.get('report', 'No report generated.'))}</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:22px;'></div>", unsafe_allow_html=True)
    render_result_card("Critic feedback", state.get("feedback", ""), STAGES[3]["color"])

    st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
    with st.expander("Search results (raw agent output)"):
        st.markdown(
            f"<div class='card-body' style='color:{TEXT_SECONDARY};'>"
            f"{html_lib.escape(state.get('search_results', ''))}</div>",
            unsafe_allow_html=True,
        )
    with st.expander("Scraped content (raw agent output)"):
        st.markdown(
            f"<div class='card-body' style='color:{TEXT_SECONDARY};'>"
            f"{html_lib.escape(state.get('scraped_content', ''))}</div>",
            unsafe_allow_html=True,
        )

elif not run_clicked:
    st.markdown(
        """
        <div class="empty-state">
            <div style="font-size:1.4rem; margin-bottom:8px;">◆</div>
            <div style="font-weight:600; color:#EAE7E1; margin-bottom:4px;">No report yet</div>
            <div style="font-size:0.85rem;">Enter a topic in the sidebar and run the pipeline to see it work.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )