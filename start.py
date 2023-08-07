import pytesseract
import os
import glob
import shutil
from PIL import Image
from pdf2image import convert_from_path
from fpdf import FPDF


def ocr_pdf(file_path):
    # Convert PDF to images
    pages = convert_from_path(file_path, 500)

    image_counter = 1

    # Save each page as an image
    for page in pages:
        filename = "page_"+str(image_counter)+".jpg"
        # Save the image of the page in system
        page.save(filename, 'JPEG')
        image_counter += 1

    # Recognize the text as string in image using pytesseract
    filelimit = image_counter-1
    output = ""
    for i in range(1, filelimit + 1):
        filename = "page_"+str(i)+".jpg"
        text = str(((pytesseract.image_to_string(Image.open(filename)))))
        output += text
        # Remove the image file after OCR
        os.remove(filename)

    # Replace the unicode quotation marks with ASCII quotes
    output = output.replace('\u201c', '"').replace('\u201d', '"').replace('\u2018', "'").replace('\u2019', "'")
    output = "".join(ch for ch in output if ord(ch)<128)

    # Writing the recognized text into new PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 11)
    pdf.multi_cell(275, txt = output)

    new_file_path = os.path.basename(file_path).replace('.pdf', '') + '-editable.pdf'
    pdf.output(f'output/{new_file_path}')

    # Move the processed file to the processed directory
    shutil.move(file_path, f'processed/{os.path.basename(file_path)}')

def process_all_pdfs_in_folder(folder_path):
    for file in glob.glob(f"{folder_path}/*.pdf"):
        print(f'Processing file {file}')
        ocr_pdf(file)
        print(f'Finished processing file {file}')

# Create directories if they do not exist
os.makedirs('output', exist_ok=True)
os.makedirs('processed', exist_ok=True)
os.makedirs('input', exist_ok=True)

# Run the function with the path to the folder with the PDFs
process_all_pdfs_in_folder('input')
