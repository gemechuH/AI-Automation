import streamlit as st
from pathlib import Path

def render_sidebar():
    """
    Renders the advanced configuration sidebar and returns the user's settings.
    """
    st.sidebar.markdown("## ⚙️ Configuration")
    
    # Text Area for deeper context
    goal = st.sidebar.text_area("Research Goal", placeholder="e.g. Find the cheapest tools for a 2 person team")
    scope = st.sidebar.text_area("Scope & Exclusions", placeholder="e.g. Must have a free tier, avoid enterprise CRMs")
    
    st.sidebar.markdown("---")
    
    # Advanced Options
    depth = st.sidebar.selectbox("Research Depth", ["Short Overview", "Medium Detail", "Deep Technical Dive"])
    sources = st.sidebar.slider("Number of Target Sources", min_value=1, max_value=10, value=3)
    
    st.sidebar.markdown("---")
    
    # Output formats
    st.sidebar.markdown("### 📄 Output Formats")
    comp_table = st.sidebar.checkbox("Include Comparison Table", value=True)
    gen_docx = st.sidebar.checkbox("Generate DOCX file", value=True)
    gen_pdf = st.sidebar.checkbox("Generate PDF file", value=False)
    
    return {
        "goal": goal.strip(),
        "scope": scope.strip(),
        "depth": depth,
        "sources": sources,
        "comp_table": comp_table,
        "gen_docx": gen_docx,
        "gen_pdf": gen_pdf
    }

def render_download_buttons(paths: dict):
    """
    Given a dictionary of names and file paths, checks if they exist and renders Streamlit download buttons.
    """
    st.markdown("### 💾 Downloads")
    cols = st.columns(len(paths))
    
    for idx, (label, path) in enumerate(paths.items()):
        if path.exists():
            try:
                # Need to read the file entirely into memory to prevent Streamlit download button bugs on click
                with open(path, "rb") as f:
                    file_data = f.read()
                    
                cols[idx].download_button(
                    label=f"Download {label}",
                    data=file_data,
                    file_name=path.name,
                    mime="application/octet-stream"
                )
            except Exception as e:
                cols[idx].error(f"Failed to load {label}")

def render_url_cards(urls_file_path: Path):
    """
    Reads the URLs from the file and displays them as beautiful clickable cards.
    """
    if not urls_file_path.exists():
        st.info("No sources found. Run a research task to populate this section.")
        return
        
    with open(urls_file_path, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]
        
    if not urls:
        st.info("No URLs were collected during the search.")
        return
        
    for index, url in enumerate(urls, 1):
        # We use a custom HTML card for nice layout
        st.markdown(f"""
        <div class="url-card">
            <div><strong>Source {index}</strong></div>
            <a href="{url}" target="_blank">{url}</a>
        </div>
        """, unsafe_allow_html=True)
