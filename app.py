import streamlit as st
from pipeline import run_research_pipeline
 
st.set_page_config(
    page_title="ResearchAI",
    page_icon="🔎",
    layout="wide",
)
 
# ---------- Session state ----------
if "state" not in st.session_state:
    st.session_state.state = None
if "topic" not in st.session_state:
    st.session_state.topic = ""
 
# ---------- Sidebar ----------
with st.sidebar:
    st.title("🔎 ResearchAI")
    st.write(
        "Enter a topic and let the multi-agent pipeline "
        "search, read, write, and critique a report for you."
    )
    st.markdown("**Pipeline steps:**")
    st.markdown(
        "1. 🔍 Search Agent\n"
        "2. 📖 Reader Agent\n"
        "3. ✍️ Writer Chain\n"
        "4. 🧐 Critic Chain"
    )
 
# ---------- Main ----------
st.title("ResearchAI Pipeline")
 
topic = st.text_input(
    "Research topic",
    value=st.session_state.topic,
    placeholder="e.g. Latest advances in solid-state batteries",
)
 
run_clicked = st.button("🚀 Run Research", type="primary", use_container_width=False)
 
if run_clicked:
    if not topic.strip():
        st.warning("Please enter a topic before running the pipeline.")
    else:
        st.session_state.topic = topic
        progress_box = st.status("Running research pipeline...", expanded=True)
        try:
            with progress_box:
                st.write("🔍 Step 1/4 — Search agent gathering sources...")
                st.write("📖 Step 2/4 — Reader agent scraping content...")
                st.write("✍️ Step 3/4 — Writer drafting the report...")
                st.write("🧐 Step 4/4 — Critic reviewing the report...")
                result = run_research_pipeline(topic)
            progress_box.update(label="Pipeline complete ✅", state="complete", expanded=False)
            st.session_state.state = result
        except Exception as e:
            progress_box.update(label="Pipeline failed ❌", state="error", expanded=True)
            st.error(f"Something went wrong while running the pipeline:\n\n{e}")
 
# ---------- Results ----------
state = st.session_state.state
 
if state:
    st.divider()
    st.subheader(f"Results for: *{st.session_state.topic}*")
 
    tab_report, tab_feedback, tab_search, tab_scraped = st.tabs(
        ["📄 Final Report", "🧐 Critic Feedback", "🔍 Search Results", "📖 Scraped Content"]
    )
 
    with tab_report:
        report = state.get("report", "No report generated.")
        st.markdown(report if isinstance(report, str) else str(report))
        st.download_button(
            "⬇️ Download report as .md",
            data=report if isinstance(report, str) else str(report),
            file_name=f"{st.session_state.topic.replace(' ', '_')}_report.md",
            mime="text/markdown",
        )
 
    with tab_feedback:
        feedback = state.get("feedback", "No feedback generated.")
        st.markdown(feedback if isinstance(feedback, str) else str(feedback))
 
    with tab_search:
        st.text_area(
            "Raw search results",
            value=state.get("search_results", ""),
            height=300,
        )
 
    with tab_scraped:
        st.text_area(
            "Raw scraped content",
            value=state.get("scraped_content", ""),
            height=300,
        )
else:
    st.info("Enter a topic above and click **Run Research** to get started.")
 
