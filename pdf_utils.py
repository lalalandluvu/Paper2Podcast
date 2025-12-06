from fpdf import FPDF
import tempfile

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Podcast Study Guide', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

def create_study_guide_pdf(text, filename="study_guide.pdf"):
    """
    Creates a PDF file from the given text.
    
    Args:
        text (str): The content of the study guide.
        filename (str): The name of the output file.
        
    Returns:
        str: The path to the generated PDF file.
    """
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Simple markdown-like parsing (very basic)
    lines = text.split('\n')
    for line in lines:
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
        else:
            # Handle standard text with multi-line support
            # sanitize text to avoid latin-1 errors common in FPDF
            safe_line = line.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 10, safe_line)
            
    # Save to a temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdf.output(tmp_file.name)
        return tmp_file.name
