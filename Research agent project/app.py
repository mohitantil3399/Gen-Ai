import gradio as gr
from Agents import search_agent, scrape_url_agent, writer_sequence, critic_sequence
import re
from datetime import datetime
import tempfile
import os

# ── Custom CSS ────────────────────────────────────────────────────────────────
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root, body, .gradio-container {
    font-family: 'Inter', sans-serif !important;
    background: radial-gradient(ellipse at top, #0f0c29, #302b63, #24243e) !important;
    min-height: 100vh;
    color: #f1f5f9 !important;
    --body-text-color: #f1f5f9 !important;
    --body-text-color-subdued: #cbd5e1 !important;
    --block-background-fill: rgba(15, 12, 41, 0.6) !important;
    --block-border-color: rgba(108, 99, 255, 0.3) !important;
    --input-background-fill: #1e1b4b !important;
}

* { font-family: 'Inter', sans-serif !important; }

/* Reset default block white backgrounds */
.block, .form, fieldset, label, .gradio-container div, .gradio-container span, .gradio-container p {
    background-color: transparent !important;
    color: #e2e8ff;
}

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 2rem;
    background: linear-gradient(135deg, rgba(108,99,255,.25), rgba(255,99,165,.15)) !important;
    border: 1px solid rgba(108,99,255,.4) !important;
    border-radius: 22px;
    margin-bottom: 1.5rem;
}
.hero-title {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #c084fc, #f472b6, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    letter-spacing: -1px;
}
.hero-sub {
    color: #cbd5e1 !important;
    font-size: 1.05rem;
    margin-top: .5rem;
}

/* ── Input box ── */
.input-row, .input-row .block, .input-row label, .input-row fieldset, .input-row div {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

.input-row textarea, .input-row input {
    background: #1e1b4b !important;
    border: 2px solid rgba(167,139,250,.6) !important;
    border-radius: 14px !important;
    color: #ffffff !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
    padding: .75rem 1rem !important;
    transition: all .3s ease !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
}
.input-row textarea::placeholder, .input-row input::placeholder {
    color: #94a3b8 !important;
}
.input-row textarea:focus, .input-row input:focus {
    border-color: #f472b6 !important;
    box-shadow: 0 0 0 3px rgba(244,114,182,.3) !important;
}

/* ── Research button ── */
#run-btn {
    background: linear-gradient(135deg, #7c3aed, #db2777) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 14px !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    height: 52px !important;
    transition: all .3s ease !important;
    box-shadow: 0 4px 20px rgba(124,58,237,.4) !important;
}
#run-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(124,58,237,.6) !important;
}

/* ── Stage cards ── */
.stage-row {
    display: flex;
    gap: .75rem;
    margin: 1.2rem 0;
}
.stage {
    flex: 1;
    background: rgba(15,12,41,.7) !important;
    border: 1px solid rgba(108,99,255,.3) !important;
    border-radius: 14px;
    padding: .9rem 1rem;
    text-align: center;
    transition: all .4s ease;
}
.stage.active {
    border-color: #a78bfa !important;
    background: rgba(167,139,250,.2) !important;
    box-shadow: 0 0 20px rgba(167,139,250,.4) !important;
    animation: pulse 1.5s infinite;
}
.stage.done {
    border-color: #34d399 !important;
    background: rgba(52,211,153,.15) !important;
}
.stage-icon { font-size: 1.5rem; }
.stage-label {
    font-size: .75rem;
    font-weight: 800;
    color: #f1f5f9 !important;
    text-transform: uppercase;
    letter-spacing: .8px;
    margin-top: .3rem;
}

@keyframes pulse {
    0%, 100% { box-shadow: 0 0 15px rgba(167,139,250,.3); }
    50%       { box-shadow: 0 0 30px rgba(167,139,250,.6); }
}

/* ── Status bar ── */
.status-bar {
    background: rgba(15,12,41,.8) !important;
    border: 1px solid rgba(108,99,255,.35) !important;
    border-radius: 12px;
    padding: .75rem 1.25rem;
    color: #f1f5f9 !important;
    font-size: .95rem;
    font-weight: 500;
    margin-bottom: .5rem;
    min-height: 42px;
}

/* ── Tabs ── */
.tabs, .tab-nav {
    background: transparent !important;
    border-bottom: 1px solid rgba(108,99,255,.3) !important;
}
.tab-nav button, .tab-nav button *, .tabs button, .tabs button * {
    background: transparent !important;
    color: #94a3b8 !important;
    border: none !important;
    font-weight: 600 !important;
    font-size: .95rem !important;
}
.tab-nav button.selected, .tab-nav button.selected *, .tabs button.selected, .tabs button.selected * {
    color: #c084fc !important;
    border-bottom: 2px solid #c084fc !important;
    font-weight: 700 !important;
}

/* ── Report & Review output markdown ── */
.report-box, .review-box {
    background: rgba(15,12,41,.85) !important;
    border: 1px solid rgba(108,99,255,.35) !important;
    border-radius: 16px !important;
    padding: 1.5rem 2rem !important;
    min-height: 120px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4) !important;
}

/* Specific text color targets inside markdown to override Gradio theme defaults */
.report-box *, .review-box * {
    color: #f1f5f9 !important;
}
.report-box h1, .report-box h2, .report-box h3,
.review-box h1, .review-box h2, .review-box h3 {
    color: #c084fc !important;
    font-weight: 700 !important;
    margin-top: 1rem !important;
    margin-bottom: 0.5rem !important;
}
.report-box h4, .report-box h5,
.review-box h4, .review-box h5 {
    color: #34d399 !important;
    font-weight: 600 !important;
}
.report-box p, .review-box p,
.report-box li, .review-box li,
.report-box td, .review-box td,
.report-box th, .review-box th,
.report-box span, .review-box span {
    color: #e2e8ff !important;
    line-height: 1.7 !important;
    font-size: 1rem !important;
}
.report-box strong, .review-box strong,
.report-box b, .review-box b {
    color: #f472b6 !important;
    font-weight: 700 !important;
}
.report-box code, .review-box code {
    background: rgba(255, 255, 255, 0.1) !important;
    color: #f472b6 !important;
    padding: 2px 6px !important;
    border-radius: 4px !important;
}
.report-box blockquote, .review-box blockquote {
    border-left: 4px solid #a78bfa !important;
    background: rgba(167,139,250,.1) !important;
    padding: 0.5rem 1rem !important;
    color: #e2e8ff !important;
}

/* ── Score badge ── */
.score-badge {
    display: inline-block;
    background: linear-gradient(135deg, #a78bfa, #f472b6);
    color: white !important;
    padding: .3rem 1.1rem;
    border-radius: 30px;
    font-weight: 700;
    font-size: 1.1rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 15px rgba(167,139,250,.4);
}
/* ── Download button ── */
.download-btn {
    background: linear-gradient(135deg, #059669, #10b981) !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    border: none !important;
    padding: 0.75rem 1.5rem !important;
    margin-top: 1rem !important;
    transition: all .3s ease !important;
}
.download-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(16,185,129,.5) !important;
}

/* ── Sidebar info cards ── */
.info-card {
    background: rgba(15,12,41,.7) !important;
    border: 1px solid rgba(108,99,255,.3) !important;
    border-radius: 12px;
    padding: 1.1rem;
    margin-bottom: .85rem;
    color: #e2e8ff !important;
    font-size: .9rem;
    line-height: 1.65;
}
.info-card b, .info-card strong {
    color: #c084fc !important;
    font-size: 0.95rem;
}

footer { display: none !important; }
"""

# ── Stage HTML helper ─────────────────────────────────────────────────────────
def stages_html(active: int) -> str:
    icons  = ["🔍", "🕸️", "✍️", "🧐"]
    labels = ["Searching", "Scraping", "Writing", "Reviewing"]
    cards  = ""
    for i, (icon, label) in enumerate(zip(icons, labels)):
        if i < active:
            cls, icon = "stage done", "✅"
        elif i == active:
            cls = "stage active"
        else:
            cls = "stage"
        cards += f'<div class="{cls}"><div class="stage-icon">{icon}</div><div class="stage-label">{label}</div></div>'
    return f'<div class="stage-row">{cards}</div>'

# ── Core pipeline (generator — yields UI updates after each stage) ─────────────
def run_pipeline(topic: str):
    if not topic.strip():
        yield (
            stages_html(-1),
            '<div class="status-bar">⚠️ Please enter a research topic.</div>',
            "", "", None
        )
        return

    state = {}

    # ── Stage 1: Search ───────────────────────────────────────────────────────
    yield stages_html(0), '<div class="status-bar">🔍 Searching the web for diverse sources…</div>', "", "", None
    try:
        searcher = search_agent()
        result = searcher.invoke({
            "messages": [("user", f"Search for comprehensive and diverse sources (at least 3-4 distinct perspectives) on the topic: {topic}.")]
        })
        state["search_results"] = result["messages"][-1].content
    except Exception as e:
        yield stages_html(0), f'<div class="status-bar">❌ Search failed: {e}</div>', "", "", None
        return

    # ── Stage 2: Scrape ───────────────────────────────────────────────────────
    yield stages_html(1), '<div class="status-bar">🕸️ Scraping URLs for deep content…</div>', "", "", None
    try:
        scraper = scrape_url_agent()
        web = scraper.invoke({
            "messages": [("user", f"""
            Based on the following results about the topic: {topic}.
            Pick the most relevant urls and extract deep details respectively.
            Search results are:\n {state['search_results']}""")]
        })
        state["scraped_content"] = web["messages"][-1].content
    except Exception as e:
        yield stages_html(1), f'<div class="status-bar">❌ Scraping failed: {e}</div>', "", "", None
        return

    # ── Stage 3: Write ────────────────────────────────────────────────────────
    yield stages_html(2), '<div class="status-bar">✍️ Writing research report…</div>', "", "", None
    try:
        combined = (
            f"Search Results: {state['search_results']}\n\n"
            f"Scraped Content: {state['scraped_content']}"
        )
        state["report"] = writer_sequence.invoke({
            "topic": topic,
            "gathered_data": combined,
        })
    except Exception as e:
        yield stages_html(2), f'<div class="status-bar">❌ Writing failed: {e}</div>', "", "", None
        return

    # ── Stage 4: Review ───────────────────────────────────────────────────────
    yield stages_html(3), '<div class="status-bar">🧐 Peer-reviewing the report…</div>', state["report"], "", None
    try:
        state["feedback"] = critic_sequence.invoke({
            "topic": topic,
            "report": state["report"],
        })
    except Exception as e:
        yield stages_html(3), f'<div class="status-bar">❌ Review failed: {e}</div>', state["report"], "", None
        return

    # ── Build download file ───────────────────────────────────────────────────
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    fname     = f"research_{topic[:25].strip().replace(' ', '_')}_{timestamp}.md"
    tmp_path  = os.path.join(tempfile.gettempdir(), fname)
    with open(tmp_path, "w", encoding="utf-8") as f:
        full_content = f"# Research Report\n\n{state['report']}\n\n---\n\n# Peer Review\n\n{state['feedback']}"
        f.write(full_content)

    # ── Extract score ─────────────────────────────────────────────────────────
    m = re.search(r"(\d+(?:\.\d+)?)\s*/\s*10", state["feedback"])
    score_html = ""
    if m:
        score = float(m.group(1))
        color = "#34d399" if score >= 7 else "#fbbf24" if score >= 5 else "#f87171"
        score_html = f'<div style="margin-bottom:1rem"><span class="score-badge" style="background:{color}">⭐ {m.group(1)} / 10</span></div>'

    yield (
        stages_html(4),
        '<div class="status-bar">🎉 Research complete! See your report and review below.</div>',
        state["report"],
        score_html + state["feedback"],
        tmp_path,
    )

# ── Build UI ──────────────────────────────────────────────────────────────────
with gr.Blocks(css=CSS, title="Deep Research Agent", theme=gr.themes.Default(primary_hue="gray")) as app:

    # Hero
    gr.HTML("""
    <div class="hero">
        <div class="hero-title">🔬 Deep Research Agent</div>
        <div class="hero-sub">Multi-agent AI pipeline · Search · Scrape · Write · Review</div>
    </div>
    """)

    with gr.Row():
        with gr.Column(scale=3):
            # ── Main area ──────────────────────────────────────────────────
            with gr.Row(elem_classes="input-row"):
                topic_box = gr.Textbox(
                    placeholder="e.g. What is quantum computing and how will it change the world?",
                    label="",
                    lines=1,
                    scale=4,
                    show_label=False,
                )
                run_btn = gr.Button("🚀 Research", scale=1, elem_id="run-btn", variant="primary")

            stages_out = gr.HTML(stages_html(-1))
            status_out = gr.HTML('<div class="status-bar">Enter a topic above and hit Research to begin.</div>')

            with gr.Tabs():
                with gr.Tab("📄 Research Report"):
                    report_out  = gr.Markdown(elem_classes="report-box")
                    download_out = gr.DownloadButton(label="📥 Download Report + Review (.md)", elem_classes="download-btn")

                with gr.Tab("🧐 Peer Review"):
                    review_out = gr.Markdown(elem_classes="review-box")

        with gr.Column(scale=1):
            # ── Sidebar ────────────────────────────────────────────────────
            gr.HTML("""
            <div class="info-card">
                <b>🤖 How it works</b><br><br>
                A 4-stage AI pipeline autonomously searches, scrapes, writes,
                and critiques a full research report on any topic you provide.
            </div>
            <div class="info-card">
                <b>⚡ Models</b><br><br>
                🔍 <b>Search</b> — Groq · llama-3.3-70b<br>
                🕸️ <b>Scrape</b> — OpenRouter · NVIDIA Nemotron<br>
                ✍️ <b>Writer</b> — OpenRouter · NVIDIA Nemotron<br>
                🧐 <b>Critic</b> — Groq · llama-3.3-70b
            </div>
            <div class="info-card">
                <b>📋 Pipeline</b><br><br>
                1️⃣ Tavily web search (5 sources)<br>
                2️⃣ Deep URL scraping<br>
                3️⃣ Report generation<br>
                4️⃣ AI peer review & scoring
            </div>
            <div class="info-card" style="font-size:.75rem; color: #cbd5e1">
                Built with LangChain · LangGraph · Gradio
            </div>
            """)

    # ── Wire up button & Enter key ────────────────────────────────────────────
    run_event = dict(
        fn=run_pipeline,
        inputs=[topic_box],
        outputs=[stages_out, status_out, report_out, review_out, download_out],
    )
    run_btn.click(**run_event)
    topic_box.submit(**run_event)

if __name__ == "__main__":
    app.launch(share=False)
