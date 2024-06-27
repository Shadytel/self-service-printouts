#!/usr/bin/env python

import pandas as pd
from jinja2 import Environment, DictLoader
from fpdf import FPDF
import argparse
import PyPDF2
import os


parser = argparse.ArgumentParser()
parser.add_argument('csv_file', type=str, help='Path to the CSV of phone numbers and PINs')
args = parser.parse_args()

df = pd.read_csv(args.csv_file)

template_str = """
Welcome new Shadytel subscriber!

Please follow these simple instructions to set up your phone service:

1. Connect your phone to an available jack at the nearest Shadystake.

2. Pick up the phone and follow the prompts. Enter your phone number and PIN when prompted.

3. Your phone line is ready for use!

Your phone Number: {{ phone_number }}
Your PIN: {{ pin }}

Thank you for subscribing to Shadytel, the only choice for phone service!
"""

env = Environment(loader=DictLoader({'template': template_str}))
template = env.get_template('template')

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 18)
        self.cell(0, 10, 'Shadytel Self-Service Provisioning System Instructions Form', 0, 1, 'C')

    def chapter_body(self, body):
        self.set_font('Arial', '', 18)
        self.multi_cell(0, 10, body)
        self.ln()

def merge_pdfs(pdf_list, output_path):
    pdf_merger = PyPDF2.PdfMerger()

    for pdf in pdf_list:
        pdf_merger.append(pdf)

    with open(output_path, 'wb') as output_file:
        pdf_merger.write(output_file)

pdf_files = []
for index, row in df.iterrows():
    phone_number = row[0]
    pin = row[3]
    output_from_parsed_template = template.render(phone_number=phone_number, pin=pin)

    pdf = PDF()
    pdf.add_page()
    pdf.chapter_body(output_from_parsed_template)

    pdf_file_name = f'output_{index + 1}.pdf'
    pdf.output(pdf_file_name)
    pdf_files.append(pdf_file_name)

merge_pdfs(pdf_files, "merged.pdf")

for pdf_file in pdf_files:
    os.remove(pdf_file)

