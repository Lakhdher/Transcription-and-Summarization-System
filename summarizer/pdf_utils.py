import fitz
from fpdf import FPDF
from PyPDF2 import PdfMerger, PdfFileReader


def convert_pdf_to_text(path):
    """
    Extracts text from a PDF file using fitz.
    """
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def create_pdf(input_file, output_file):
    # Create a new FPDF object
    pdf = FPDF()

    # Open the text file and read its contents
    with open(input_file, "r") as f:
        text = f.read()

    # Add a new page to the PDF
    pdf.add_page()

    # Set the font and font size
    pdf.set_font("Arial", size=12)

    # Write the text to the PDF
    pdf.write(5, text)

    # Save the PDF
    pdf.output(output_file)
