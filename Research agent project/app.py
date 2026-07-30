import streamlit as st
import re
from datetime import datetime
from Agents import search_agent, scrape_url_agent, writer_sequence, critic_sequence

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Deep Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ---- background ---- */
.stApp {
    background: radial-gradient(ellipse at top, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

/* ---- hero header ---- */
.hero-wrap {
    text-align: center;
    padding: 2.5rem 1rem 2rem;
    background: linear-gradient(135deg, rgba(108,99,255,.15), rgba(255,99,165,.08));
    border: 1px solid rgba(108,99,255,.35);
    border-radius: 22px;
    margin-bottom: 2rem;
}
.hero-title {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #f472b6, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    letter-spacing: -1px;
}
.hero-sub {
    color: rgba(200,200,255,.6);
    font-size: 1.05rem;
    margin-top: .5rem;
}

/* ---- pipeline stages ---- */
.pipeline-row {
    display: flex;
    gap: .75rem;
    margin: 1.5rem 0;
    flex-wrap: wrap;
}
.stage {
    flex: 1;
    min-width: 130px;
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(108,99,255,.2);
    border-radius: 14px;
    padding: .85rem 1rem;
    text-align: center;
    transition: all .4s ease;
    position: relative;
    overflow: hidden;
}
.stage::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(108,99,255,.08), rgba(255,99,165,.05));
    opacity: 0;
    transition: opacity .4s;
}
.stage.active::before { opacity: 1; }
.stage.active {
    border-color: #a78bfa;
    box-shadow: 0 0 22px rgba(167,139,250,.35);
}
.stage.done {
    border-color: #34d399;
    background: rgba(52,211,153,.06);
}
.stage-icon { font-size: 1.6rem; margin-bottom: .25rem; }
.stage-label { font-size: .78rem; font-weight: 600; color: rgba(200,200,255,.75); text-transform: uppercase; letter-spacing: .8px; }

/* ---- report box ---- */
.report-box {
    background: rgba(15,12,41,.6);
    border: 1px solid rgba(108,99,255,.28);
    border-radius: 18px;
    padding: 2rem 2.5rem;
    margin-top: 1.5rem;
    backdrop-filter: blur(8px);
}
.report-box h2 { color: #a78bfa; }
.report-box h3 { color: #f472b6; }
.report-box h4 { color: #34d399; }

/* ---- critic box ---- */
.critic-box {
    background: linear-gradient(135deg, rgba(251,191,36,.06), rgba(244,114,182,.05));
    border: 1px solid rgba(251,191,36,.3);
    border-radius: 18px;
    padding: 1.5rem 2rem;
    margin-top: 1rem;
}

/* ---- score badge ---- */
.score-badge {
    display: inline-block;
    background: linear-gradient(135deg, #a78bfa, #f472b6);
    color: white;
    padding: .35rem 1.2rem;
    border-radius: 30px;
    font-weight: 700;
    font-size: 1.15rem;
    margin-left: .5rem;
    box-shadow: 0 4px 15px rgba(167,139,250,.4);
}

/* ---- sidebar cards ---- */
.sb-card {
    background: rgba(255,255,255,.03);
    border: 1px solid rgba(108,99,255,.18);
    border-radius: 12px;
    padding: .9rem 1rem;
    margin: .5rem 0;
    font-size: .85rem;
}
.sb-card b { color: #a78bfa; }

/* ---- buttons ---- */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #db2777) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: .65rem 1rem !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    width: 100% !important;
    transition: all .3s ease !important;
    box-shadow: 0 4px 20px rgba(124,58,237,.35) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(124,58,237,.55) !important;
}

/* ---- input ---- */
.stTextInput > div > div > input {
    background: rgba(255,255,255,.06) !important;
    border: 1px solid rgba(108,99,255,.45) !important;
    border-radius: 12px !important;
    color: #e2e8ff !important;
    font-size: 1rem !important;
    padding: .65rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #a78bfa !important;
    box-shadow: 0 0 0 3px rgba(167,139,250,.25) !important;
}
.stTextInput label { color: rgba(200,200,255,.7) !important; font-weight: 600 !important; }

/* ---- download button ---- */
.stDownloadButton > button {
    background: linear-gradient(135deg, #065f46, #047857) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all .3s ease !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(4,120,87,.5) !important;
}

/* ---- misc ---- */
#MainMenu, footer { visibility: hidden; }
hr { border-color: rgba(108,99,255,.2); }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔬 Deep Research Agent")
    st.markdown("---")
    st.markdown("""
    <div class="sb-card">
    <b>🤖 How it works</b><br><br>
    A 4-stage AI pipeline autonomously searches, scrapes, writes, and critiques a full research report on any topic.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="sb-card">
    <b>⚡ Models in use</b><br><br>
    🔍 <b>Search Agent</b> — Groq · llama-3.3-70b<br>
    🕸️ <b>Scrape Agent</b> — OpenRouter · NVIDIA Nemotron Ultra<br>
    ✍️ <b>Writer</b> — OpenRouter · NVIDIA Nemotron Ultra<br>
    🧐 <b>Critic</b> — Groq · llama-3.3-70b
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="sb-card">
    <b>📋 Pipeline Stages</b><br><br>
    1️⃣ Tavily web search (5 sources)<br>
    2️⃣ URL scraping for deep content<br>
    3️⃣ Report generation<br>
    4️⃣ AI-powered peer review
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<small style='color:rgba(200,200,255,.4)'>Built with LangChain · LangGraph · Streamlit</small>", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-title">🔬 Deep Research Agent</div>
    <div class="hero-sub">Multi-agent AI pipeline that searches, scrapes, writes & critiques research reports autonomously</div>
</div>
""", unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([4, 1])
with col1:
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. What is quantum computing and how will it change the world?",
        label_visibility="collapsed",
    )
with col2:
    run_btn = st.button("🚀 Research", use_container_width=True)

st.markdown("---")

# ── Pipeline stages display ────────────────────────────────────────────────────
stages_placeholder = st.empty()

def render_stages(active: int):
    """Render the 4 pipeline stage indicators. active=0-3 during, 4=all done."""
    icons  = ["🔍", "🕸️", "✍️", "🧐"]
    labels = ["Searching", "Scraping", "Writing", "Reviewing"]
    html = '<div class="pipeline-row">'
    for i, (icon, label) in enumerate(zip(icons, labels)):
        if i < active:
            cls = "stage done"
            icon = "✅"
        elif i == active:
            cls = "stage active"
        else:
            cls = "stage"
        html += f'<div class="{cls}"><div class="stage-icon">{icon}</div><div class="stage-label">{label}</div></div>'
    html += "</div>"
    stages_placeholder.markdown(html, unsafe_allow_html=True)

render_stages(-1)  # all idle on load

# ── Main logic ────────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("⚠️ Please enter a research topic first.")
        st.stop()

    state = {}
    report_placeholder = st.empty()
    critic_placeholder = st.empty()

    # ── Stage 1: Search ──────────────────────────────────────────────────────
    render_stages(0)
    with st.status("🔍 Searching the web for relevant sources...", expanded=False) as search_status:
        try:
            searcher = search_agent()
            result = searcher.invoke({
                "messages": [("user", f"Search for comprehensive and diverse sources (at least 3-4 distinct perspectives) on the topic: {topic}.")]
            })
            state["search_results"] = result["messages"][-1].content
            st.write(f"✅ Found search results ({len(state['search_results'])} chars)")
            search_status.update(label="✅ Web search complete!", state="complete")
        except Exception as e:
            search_status.update(label=f"❌ Search failed: {e}", state="error")
            st.error(f"Search agent error: {e}")
            st.stop()

    # ── Stage 2: Scrape ──────────────────────────────────────────────────────
    render_stages(1)
    with st.status("🕸️ Scraping URLs for deep content...", expanded=False) as scrape_status:
        try:
            scraper = scrape_url_agent()
            web_results = scraper.invoke({
                "messages": [("user", f"""
                Based on the following results about the topic: {topic}.
                Pick the most relevant urls and extract deep details respectively.
                Search results are:\n {state['search_results']}""")]
            })
            state["scraped_content"] = web_results["messages"][-1].content
            st.write(f"✅ Scraped content ({len(state['scraped_content'])} chars)")
            scrape_status.update(label="✅ URL scraping complete!", state="complete")
        except Exception as e:
            scrape_status.update(label=f"❌ Scraping failed: {e}", state="error")
            st.error(f"Scrape agent error: {e}")
            st.stop()

    # ── Stage 3: Write ───────────────────────────────────────────────────────
    render_stages(2)
    with st.status("✍️ Writing research report...", expanded=False) as write_status:
        try:
            combined = (
                f"Search Results: {state['search_results']}\n\n"
                f"Scraped Content: {state['scraped_content']}"
            )
            state["report"] = writer_sequence.invoke({
                "topic": topic,
                "gathered_data": combined,
            })
            st.write(f"✅ Report generated ({len(state['report'])} chars)")
            write_status.update(label="✅ Report written!", state="complete")
        except Exception as e:
            write_status.update(label=f"❌ Writing failed: {e}", state="error")
            st.error(f"Writer error: {e}")
            st.stop()

    # ── Stage 4: Review ──────────────────────────────────────────────────────
    render_stages(3)
    with st.status("🧐 Reviewing and scoring the report...", expanded=False) as review_status:
        try:
            state["feedback"] = critic_sequence.invoke({
                "topic": topic,
                "report": state["report"],
            })
            review_status.update(label="✅ Review complete!", state="complete")
        except Exception as e:
            review_status.update(label=f"❌ Review failed: {e}", state="error")
            st.error(f"Critic error: {e}")
            st.stop()

    # all stages done
    render_stages(4)

    st.success("🎉 Research complete! Your report is ready below.")

    # ── Report display ────────────────────────────────────────────────────────
    st.markdown("---")
    tab1, tab2 = st.tabs(["📄 Research Report", "🧐 Peer Review"])

    with tab1:
        # Download button
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename  = f"research_{topic[:30].strip().replace(' ', '_')}_{timestamp}.md"
        dl_col, _ = st.columns([1, 3])
        with dl_col:
            st.download_button(
                label="📥 Download Report (.md)",
                data=state["report"],
                file_name=filename,
                mime="text/markdown",
                use_container_width=True,
            )
        st.markdown('<div class="report-box">', unsafe_allow_html=True)
        st.markdown(state["report"])
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        # Extract score with regex
        score_match = re.search(r"(\d+(?:\.\d+)?)\s*/\s*10", state["feedback"])
        if score_match:
            score = score_match.group(1)
            color = "#34d399" if float(score) >= 7 else "#fbbf24" if float(score) >= 5 else "#f87171"
            st.markdown(
                f"**Final Score:** <span class='score-badge' style='background:linear-gradient(135deg,{color},{color}99)'>{score} / 10</span>",
                unsafe_allow_html=True,
            )
        st.markdown('<div class="critic-box">', unsafe_allow_html=True)
        st.markdown(state["feedback"])
        st.markdown("</div>", unsafe_allow_html=True)

        # Download critique too
        dl_col2, _ = st.columns([1, 3])
        with dl_col2:
            st.download_button(
                label="📥 Download Critique (.md)",
                data=state["feedback"],
                file_name=f"critique_{timestamp}.md",
                mime="text/markdown",
                use_container_width=True,
            )
