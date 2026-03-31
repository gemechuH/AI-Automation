import streamlit as st
import subprocess
import json
from pathlib import Path
import components

# --- PATH SETUP ---
BASE_DIR = Path(__file__).resolve().parent.parent
TMP_DIR = BASE_DIR / ".tmp"
OUTPUTS_DIR = BASE_DIR / "outputs"

CONFIG_FILE = TMP_DIR / "config.json"
REPORT_FILE = OUTPUTS_DIR / "report.md"
DOCX_FILE = OUTPUTS_DIR / "report.docx"
PDF_FILE = OUTPUTS_DIR / "report.pdf"
URLS_FILE = TMP_DIR / "urls.txt"

# --- PAGE CONFIGURATION & CSS ---
st.set_page_config(page_title="AI Research Agent (Pro)", page_icon="🕵️‍♂️", layout="wide")

css_file = Path(__file__).parent / "styles.css"
if css_file.exists():
    with open(css_file, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# --- STATE INITIALIZATION ---
if "research_done" not in st.session_state:
    st.session_state.research_done = False
if "stdout_log" not in st.session_state:
    st.session_state.stdout_log = ""
if "follow_up_history" not in st.session_state:
    st.session_state.follow_up_history = []


def run_pipeline(topic_string: str, config: dict):
    """Executes the backend pipeline and returns the stdout and status."""
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f)
        
    # We only pass the clean topic_string to the backend so the web search succeeds.
    result = subprocess.run(
        ["python", "run_agent.py", topic_string],
        cwd=str(BASE_DIR),
        capture_output=True,
        text=True
    )
    return result.returncode == 0, result.stdout + "\n" + result.stderr


# --- SIDEBAR ---
config = components.render_sidebar()

# --- MAIN PAGE ---
st.title("🕵️‍♂️ Advanced AI Research Agent")
st.markdown("Automate your deep-dive research with our 3-Layer Architecture. Enter a topic to begin.")

# Top Input
main_topic = st.text_input("Primary Research Topic", placeholder="e.g. Find businesses in Addis Ababa that need mobile apps", value="Find businesses in Addis Ababa that need mobile apps")

# Action Button
if st.button("🚀 Run Research", type="primary", use_container_width=True):
    if not main_topic.strip():
        st.error("Please enter a research topic!")
    else:
        with st.spinner(f"Agents deployed for Depth: {config['depth']}..."):
            # Only pass the exact main_topic so DuckDuckGo works.
            # In Version 2, the Goal/Scope would be passed to an LLM explicitly.
            success, logs = run_pipeline(main_topic, config)
            
            st.session_state.stdout_log = logs
            if success:
                st.session_state.research_done = True
                st.session_state.follow_up_history = [] # Reset history on new master search
                st.success("Research completed successfully!")
            else:
                st.error("The agent encountered an error during research.")


# --- RESULTS DISPLAY ---
if st.session_state.research_done:
    st.markdown("---")
    
    # Check if the extraction actually found anything before rendering downloads
    found_facts = False
    try:
        with open(TMP_DIR / 'extracted_facts.json', 'r') as f:
            if len(json.load(f)) > 0:
                found_facts = True
    except:
        pass

    if not found_facts:
        st.warning("⚠️ The agent scanned multiple websites but couldn't find exact matches for your long sentence. Try using shorter, more generic keywords in the 'Primary Research Topic' box!")
    else:
        # Render Download Buttons First 
        files_to_check = {
            "Markdown (.md)": REPORT_FILE,
            "Word (.docx)": DOCX_FILE,
            "PDF (.pdf)": PDF_FILE
        }
        components.render_download_buttons(files_to_check)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Interactive Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📄 Final Report", "🔗 Web Sources Found", "💬 Follow-ups", "⚙️ Raw Logs"])
    
    with tab1:
        st.markdown("<div class='results-card'>", unsafe_allow_html=True)
        if REPORT_FILE.exists():
            with open(REPORT_FILE, "r", encoding="utf-8") as f:
                st.markdown(f.read())
        else:
            st.warning("Report file missing. Check logs.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with tab2:
        st.markdown("### 🌐 Sources Extracted from your Search")
        st.info("The agent found these links. You can click them to do a manual deep dive if needed.")
        components.render_url_cards(URLS_FILE)

    with tab3:
        st.markdown("### 🤔 Ask a follow-up question")
        st.info("The agent will use your original research as context to dive deeper.")
        
        follow_up_q = st.text_input("What else would you like to know?", placeholder="e.g. Find specific mobile app developers instead")
        
        if st.button("Run Follow-up Research"):
            if follow_up_q:
                follow_up_prompt = f"{main_topic} {follow_up_q}"
                
                with st.spinner("Agents researching your new context..."):
                    sucess, logs = run_pipeline(follow_up_prompt, config)
                    
                    if sucess:
                        st.session_state.follow_up_history.append({"q": follow_up_q, "status": "Done. Check the updated Final Report tab!"})
                        st.rerun()
                    else:
                        st.error("Follow up failed. Check logs.")

        for item in reversed(st.session_state.follow_up_history):
            st.markdown(f"**Q:** {item['q']} \n**Update:** {item['status']}")
            st.markdown("---")

    with tab4:
        st.code(st.session_state.stdout_log)

elif st.session_state.stdout_log: # Failed start
    st.error("Execution failed. Review logs:")
    st.code(st.session_state.stdout_log)
