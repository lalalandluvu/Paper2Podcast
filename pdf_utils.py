from fpdf import FPDF
import tempfile
import re

class PDF(FPDF):
    def __init__(self, title="Podcast Study Guide"):
        super().__init__()
        self.doc_title = title

    def header(self):
        self.set_font('Arial', 'B', 15)
        # Use the dynamic title
        # Encode/decode to handle latin-1 characters safely
        safe_title = self.doc_title.encode('latin-1', 'replace').decode('latin-1')
        self.cell(0, 10, safe_title, 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

def clean_text(text):
    """
    Cleans text for FPDF (Latin-1 encoding) and strips Markdown bold markers.
    """
    # Strip bold markers (**text** -> text)
    text = text.replace('**', '')
    text = text.replace('__', '')
    
    # Handle common unicode chars that break FPDF
    replacements = {
        '\u2013': '-',  # en dash
        '\u2014': '--', # em dash
        '\u2018': "'",  # left quote
        '\u2019': "'",  # right quote
        '\u201c': '"',  # left double quote
        '\u201d': '"',  # right double quote
        '\u2022': '-',  # bullet
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
        
    return text.encode('latin-1', 'replace').decode('latin-1')

def create_study_guide_pdf(text, title="Podcast Study Guide"):
    """
    Creates a PDF file from the given text.
    
    Args:
        text (str): The content of the study guide.
        title (str): The title of the document.
        
    Returns:
        str: The path to the generated PDF file.
    """
    pdf = PDF(title=title)
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    lines = text.split('\n')
    for line in lines:
        line = clean_text(line)
        
        # Handle headers
        if line.startswith('# '):
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, line.replace('# ', ''), 0, 1)
            pdf.set_font("Arial", size=12)
        elif line.startswith('## '):
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, line.replace('## ', ''), 0, 1)
            pdf.set_font("Arial", size=12)
        elif line.startswith('### '):
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, line.replace('### ', ''), 0, 1)
            pdf.set_font("Arial", size=12)
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            # Handle list items
            pdf.set_x(15) # Indent
            content = line.strip()[2:] # Remove bullet
            pdf.multi_cell(0, 6, f"\x95 {content}") # Use bullet character
            pdf.ln(2)
        else:
            # Handle standard text
            if line.strip():
                pdf.multi_cell(0, 6, line)
                pdf.ln(2)
            else:
                # Empty line
                pdf.ln(4)
            
    # Save to a temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdf.output(tmp_file.name)
        return tmp_file.name
