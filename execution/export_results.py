# PURPOSE:
# This script takes the final JSON data that the AI extracted and turns it 
# into a clean Markdown report that is easy for humans to read.
# It also generates DOCX and PDF files if requested by the configuration.

import json
import os
import sys

# Optional libraries for PDF/DOCX generation
try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    from fpdf import FPDF
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False


def create_markdown(data, topic, source_url):
    report_path = 'outputs/report.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        # Title & Topic
        f.write("# Executive Research Report\n\n")
        f.write(f"**Research Topic:** {topic}\n")
        f.write(f"**Source Used:** {source_url}\n\n")
        
        # Summary Section
        f.write("## 1. Executive Summary\n")
        f.write("This report contains automatically extracted facts and insights related to your research topic. ")
        f.write("The facts below were pulled directly from the source URL without human intervention.\n\n")
        
        # Findings Section
        f.write("## 2. Key Findings & Topics\n")
        if not data:
            f.write("*No exact facts were found for this topic in the source text.*\n\n")
        else:
            for item in data:
                fact_text = item.get('fact', 'Unknown fact')
                f.write(f"- {fact_text}\n")
        
        f.write("\n")
        # Limitations Section
        f.write("## 3. Notes & Limitations\n")
        f.write("- **MVP Notice:** This is a Version 1 AI Research Agent.\n")
        f.write("- **AI Context:** It extracts sentences matching keywords but does not yet summarize them natively.\n")
                
    return report_path


def create_docx(data, topic, source_url):
    if not DOCX_AVAILABLE:
        print("python-docx not installed. Skipping DOCX generation.")
        return None
        
    doc = Document()
    doc.add_heading('Executive Research Report', 0)
    
    doc.add_paragraph(f"Research Topic: {topic}", style='Strong')
    doc.add_paragraph(f"Source Used: {source_url}")
    
    doc.add_heading('1. Executive Summary', level=2)
    doc.add_paragraph(
        "This report contains automatically extracted facts and "
        "insights related to your research topic."
    )
    
    doc.add_heading('2. Key Findings & Topics', level=2)
    if not data:
         doc.add_paragraph("No exact facts were found for this topic.", style='Italic')
    else:
        for item in data:
            doc.add_paragraph(item.get('fact', ''), style='List Bullet')
            
    doc.add_heading('3. Notes & Limitations', level=2)
    doc.add_paragraph("MVP Notice: This is a Version 1 AI Research Agent.", style='List Bullet')
    
    out_path = 'outputs/report.docx'
    doc.save(out_path)
    return out_path


def create_pdf(data, topic, source_url):
    if not PDF_AVAILABLE:
        print("fpdf2 not installed. Skipping PDF generation.")
        return None

    class CustomPDF(FPDF):
        def header(self):
            # We skip custom font loading for safety due to cross-platform issues
            self.set_font('helvetica', 'B', 15)
            self.cell(0, 10, 'Executive Research Report', border=False, ln=1, align='C')
            self.ln(5)

    pdf = CustomPDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=12)
    
    # Topic and Source
    pdf.set_font(style="B")
    pdf.cell(0, 8, f"Topic: {str(topic)[:80]}", ln=1)
    pdf.cell(0, 8, f"Source: {str(source_url)[:80]}", ln=1)
    pdf.ln(5)
    
    # Summary
    pdf.set_font(style="B", size=14)
    pdf.cell(0, 8, "1. Executive Summary", ln=1)
    pdf.set_font(style="", size=11)
    pdf.multi_cell(0, 6, "This report contains automatically extracted facts and insights related to your research topic.")
    pdf.ln(5)
    
    # Findings
    pdf.set_font(style="B", size=14)
    pdf.cell(0, 8, "2. Key Findings & Topics", ln=1)
    pdf.set_font(style="", size=11)
    if not data:
        pdf.cell(0, 8, "No exact facts were found.", ln=1)
    else:
        for item in data:
            fact_str = str(item.get('fact', '')).replace('\n', ' ')
            # Fix unicode characters easily throwing errors in fpdf built-in fonts
            fact_str = fact_str.encode('ascii', 'ignore').decode('ascii')
            pdf.multi_cell(0, 7, f"- {fact_str}")

    # Save
    out_path = 'outputs/report.pdf'
    pdf.output(out_path)
    return out_path


def export_reports(topic, source_url):
    try:
        with open('.tmp/extracted_facts.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: No data found.")
        return

    os.makedirs('outputs', exist_ok=True)
    
    # Check what formats the UI requested
    gen_docx = False
    gen_pdf = False
    try:
        with open('.tmp/config.json', 'r', encoding='utf-8') as f:
            cfg = json.load(f)
            gen_docx = cfg.get("gen_docx", False)
            gen_pdf = cfg.get("gen_pdf", False)
    except FileNotFoundError:
        print("No UI config found. Defaulting to standard markdown only.")

    # 1. Always create the primary Markdown file for the UI to display
    md_path = create_markdown(data, topic, source_url)
    print(f"\nFinal report saved to: {md_path}")
    
    # 2. Optionally create Word Doc
    if gen_docx:
        path = create_docx(data, topic, source_url)
        if path: print(f"DOCX created: {path}")
        
    # 3. Optionally create PDF
    if gen_pdf:
        path = create_pdf(data, topic, source_url)
        if path: print(f"PDF created: {path}")


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else "Unknown Topic"
    u = sys.argv[2] if len(sys.argv) > 2 else "Unknown Source"
    
    export_reports(t, u)
