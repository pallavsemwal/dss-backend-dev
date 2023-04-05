
from distutils.command.config import config
from django.template import loader
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.platypus import Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(filename, pdf_text):
    pdf = SimpleDocTemplate(filename, pagesize=letter)
    # Define the styles
    styles = getSampleStyleSheet()
    style_heading = styles["Heading1"]
    style_normal = styles["Normal"]

    # Define the logo image and size
    logo = 'C://Users//ankit//Downloads//example_image.jpg'
    logo_width = 2*inch
    logo_height = 1*inch

    # Define the text for the heading and the text box
    heading_text = "Notice"
    textbox_text = pdf_text

    # Create the content
    content = []

    # Add the logo to the upper right of the page
    logo_image = Image(logo, width=logo_width, height=logo_height)
    logo_image.hAlign = "RIGHT"
    content.append(logo_image)
    content.append(Spacer(1, 0.25*inch))

    # Add the heading to the page
    heading = Paragraph(heading_text, style_heading)
    content.append(heading)
    content.append(Spacer(1, 0.25*inch))

    # Add the text box to the page
    textbox = Paragraph(textbox_text, style_normal)
    content.append(textbox)
    content.append(Spacer(1, 0.5*inch))

    # Build the PDF
    pdf.build(content)

