import base64
import pandas as pd
import json
from datetime import datetime
from fpdf import FPDF

def export_to_pdf(analysis_results: dict):
    """
    Generates a PDF report of analysis results
    Args:
        analysis_results: Dictionary with "summary" and "sources" keys
    Returns:
        base64 encoded PDF content
    """
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'AI News Analysis Report', 0, 1, 'C')
    
    pdf = PDF()
    pdf.add_page()
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True)
    
    # Add summary
    pdf.cell(0, 10, "Analysis Summary", ln=True)
    pdf.multi_cell(0, 10, analysis_results["summary"] if analysis_results else "No analysis available")

    # Add sources
    pdf.set_font("Arial", "B", 12)
    pdf.ln(10)
    pdf.cell(0, 10, "Sources", ln=True)
    pdf.set_font("Arial", size=10)
    for source in analysis_results.get("sources", []):
        pdf.multi_cell(0, 10, f"• {source['title']} [{source.get('source', 'N/A')}]")
        
    # Output buffer
    output = io.BytesIO()
    pdf.output(output)
    output.seek(0)
    
    return base64.b64encode(output.read()).decode('utf-8')

def export_to_json(data: dict) -> str:
    """Generates JSON string of analysis"""
    return json.dumps(data, indent=2, ensure_ascii=False)

def export_to_csv(sources: list) -> bytes:
    """Exports sources to CSV bytes"""
    df = pd.DataFrame.from_records(sources)
    return df.to_csv(index=False).encode('utf-8')

def generate_downloader(
    filename: str,
    content_func,
    *args,
    button_text: str,
    file_type: str,
    **kwargs
):
    """Generic download button creator"""
    content = content_func(*args, **kwargs)
    b64 = base64.b64encode(content).decode()
    href = f'<a href="data:{file_type};base64,{b64}" download="{filename}">{button_text}</a>'
    return href
