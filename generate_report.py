"""
Generate a PDF report of the Email Spam Detection output.
Includes terminal output and graph images.
"""

import subprocess
import sys
import os

# Get script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# ============================================
# Step 1: Run the main script and capture output
# ============================================
print("Running email_spam_detection.py and capturing output...")

result = subprocess.run(
    [sys.executable, os.path.join(script_dir, "email_spam_detection.py")],
    capture_output=True,
    text=True,
    cwd=script_dir
)

output = result.stdout
if result.stderr:
    # Filter out nltk download messages and matplotlib warnings
    stderr_lines = [
        line for line in result.stderr.splitlines()
        if not any(skip in line for skip in ['nltk_data', 'UserWarning', 'plt.show'])
    ]
    if stderr_lines:
        output += "\n" + "\n".join(stderr_lines)

print("Output captured successfully!")
print(f"Output length: {len(output)} characters")

# ============================================
# Step 2: Generate PDF
# ============================================
from fpdf import FPDF

class PDFReport(FPDF):
    def __init__(self):
        super().__init__()
        self.is_cover_page = False

    def header(self):
        if self.is_cover_page:
            return
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(255, 255, 255)
        self.set_fill_color(44, 62, 80)
        self.cell(0, 12, 'Email Spam Detection - Output Report', 0, 1, 'C', fill=True)
        self.ln(5)

    def footer(self):
        if self.is_cover_page:
            return
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no() - 1}/{{nb}}', 0, 0, 'C')

    def add_cover_page(self):
        self.is_cover_page = True
        self.add_page()

        # Decorative border
        self.set_draw_color(44, 62, 80)
        self.set_line_width(1.5)
        self.rect(12, 12, 186, 273)
        self.set_line_width(0.5)
        self.rect(15, 15, 180, 267)

        # Top decorative line
        self.set_fill_color(44, 62, 80)
        self.rect(30, 45, 150, 3, 'F')

        # Project Title
        self.set_y(55)
        self.set_font('Helvetica', 'B', 28)
        self.set_text_color(44, 62, 80)
        self.cell(0, 15, 'Spam Email Classifier', 0, 1, 'C')
        self.set_font('Helvetica', 'B', 22)
        self.cell(0, 12, 'Project', 0, 1, 'C')

        # Decorative line below title
        self.set_fill_color(41, 128, 185)
        self.rect(60, self.get_y() + 5, 90, 1.5, 'F')

        # Submitted By section
        self.set_y(110)
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(41, 128, 185)
        self.cell(0, 10, 'Submitted By', 0, 1, 'C')
        self.set_draw_color(41, 128, 185)
        self.line(75, self.get_y(), 135, self.get_y())
        self.ln(5)

        self.set_font('Helvetica', '', 13)
        self.set_text_color(50, 50, 50)
        self.cell(0, 8, 'Name: Shah Faisal', 0, 1, 'C')
        self.cell(0, 8, 'Roll Number: 88', 0, 1, 'C')

        # Class section
        self.ln(8)
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(41, 128, 185)
        self.cell(0, 10, 'Class', 0, 1, 'C')
        self.set_draw_color(41, 128, 185)
        self.line(75, self.get_y(), 135, self.get_y())
        self.ln(5)

        self.set_font('Helvetica', '', 13)
        self.set_text_color(50, 50, 50)
        self.cell(0, 8, 'Program: Artificial Intelligence', 0, 1, 'C')
        self.cell(0, 8, 'Semester: 6th', 0, 1, 'C')
        self.cell(0, 8, 'Section: B', 0, 1, 'C')

        # Submitted To section
        self.ln(8)
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(41, 128, 185)
        self.cell(0, 10, 'Submitted To', 0, 1, 'C')
        self.set_draw_color(41, 128, 185)
        self.line(75, self.get_y(), 135, self.get_y())
        self.ln(5)

        self.set_font('Helvetica', '', 13)
        self.set_text_color(50, 50, 50)
        self.cell(0, 8, 'Instructor: Miss Sawera Qureshi', 0, 1, 'C')

        # Bottom decorative line
        self.set_fill_color(44, 62, 80)
        self.rect(30, 240, 150, 3, 'F')

        # Date of Submission
        self.set_y(248)
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(44, 62, 80)
        self.cell(0, 8, 'Date of Submission', 0, 1, 'C')
        self.set_font('Helvetica', '', 13)
        self.set_text_color(50, 50, 50)
        self.cell(0, 8, '7 May 2026', 0, 1, 'C')

        self.is_cover_page = False

    def section_title(self, title):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(41, 128, 185)
        self.cell(0, 10, title, 0, 1, 'L')
        self.set_draw_color(41, 128, 185)
        self.line(self.get_x(), self.get_y(), self.get_x() + 190, self.get_y())
        self.ln(3)

    def add_terminal_output(self, text):
        self.set_font('Courier', '', 7.5)
        self.set_text_color(0, 0, 0)
        self.set_fill_color(245, 245, 245)

        lines = text.split('\n')
        for line in lines:
            # Check if we need a new page
            if self.get_y() > 270:
                self.add_page()

            # Handle long lines by wrapping
            if len(line) > 110:
                # Use multi_cell for long lines
                x_before = self.get_x()
                self.multi_cell(190, 4, line, 0, 'L', fill=True)
            else:
                self.cell(190, 4, line, 0, 1, 'L', fill=True)

    def add_graph(self, image_path, title, width=170):
        if not os.path.exists(image_path):
            self.set_font('Helvetica', 'I', 10)
            self.set_text_color(255, 0, 0)
            self.cell(0, 10, f'Image not found: {image_path}', 0, 1)
            return

        # Check if enough space, otherwise new page
        if self.get_y() > 160:
            self.add_page()

        self.section_title(title)
        x = (210 - width) / 2  # Center the image
        self.image(image_path, x=x, w=width)
        self.ln(10)


# Create PDF
print("Generating PDF report...")
pdf = PDFReport()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=20)

# Cover Page
pdf.add_cover_page()

# Page 2: Terminal Output
pdf.add_page()
pdf.set_font('Helvetica', '', 10)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 6, 'Generated from: email_spam_detection.py', 0, 1, 'C')
pdf.cell(0, 6, 'Dataset: SMS Spam Collection (spam.csv)', 0, 1, 'C')
pdf.ln(5)

# Terminal Output Section
pdf.section_title('Terminal Output')
pdf.add_terminal_output(output)

# Graphs Section
pdf.add_page()
pdf.section_title('Visualizations')
pdf.ln(3)

# Graph 1: Label Distribution
graph1 = os.path.join(script_dir, 'label_distribution.png')
pdf.add_graph(graph1, 'Email Spam vs Ham Distribution')

# Graph 2: Confusion Matrix
graph2 = os.path.join(script_dir, 'confusion_matrix_mnb.png')
pdf.add_graph(graph2, 'Confusion Matrix - Multinomial Naive Bayes')

# Save PDF
pdf_path = os.path.join(script_dir, 'Email_Spam_Detection_Report.pdf')
pdf.output(pdf_path)
print(f"\nPDF report saved to: {pdf_path}")
