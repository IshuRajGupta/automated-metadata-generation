import os
import docx
import PyPDF2
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

# If Tesseract is not in your PATH, include the following line:
# pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'
# e.g., pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_txt(file_path):
    """Extracts text from a .txt file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_text_from_docx(file_path):
    """Extracts text from a .docx file."""
    doc = docx.Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs])

def extract_text_from_pdf(file_path):
    """Extracts text from a text-based .pdf file."""
    text = ''
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + '\n'
    except Exception as e:
        print(f"Error with pdfplumber: {e}, trying PyPDF2")
        # Fallback to PyPDF2
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + '\n'
        except Exception as e2:
            print(f"Error with PyPDF2: {e2}")
    return text

def extract_text_from_scanned_pdf(file_path):
    """Extracts text from a scanned (image-based) .pdf file using OCR."""
    try:
        # On Windows, you might need to provide the poppler path to convert_from_path
        # images = convert_from_path(file_path, poppler_path=r'<path_to_your_poppler_bin_folder>')
        images = convert_from_path(file_path)
        text = ''
        for img in images:
            text += pytesseract.image_to_string(img) + '\n'
        return text
    except Exception as e:
        print(f"Error during OCR: {e}")
        return ''

def extract_text(file_path):
    """Extracts text from a file, attempting standard text extraction first,
    and falling back to OCR for PDFs if necessary."""
    if not os.path.exists(file_path):
        return 'File not found'
        
    file_extension = os.path.splitext(file_path)[1].lower()
    text = ''

    if file_extension == '.txt':
        text = extract_text_from_txt(file_path)
    elif file_extension == '.docx':
        text = extract_text_from_docx(file_path)
    elif file_extension == '.pdf':
        # First, try standard text extraction
        text = extract_text_from_pdf(file_path)
        # If it's empty or very short, it might be a scanned PDF, so try OCR
        if not text or len(text.strip()) < 100:
            print(f'Standard text extraction yielded little or no text for {os.path.basename(file_path)}, trying OCR.')
            # Append in case some text was extracted. Also prevents re-downloading images for OCR'd PDFs.
            text += extract_text_from_scanned_pdf(file_path)
    else:
        print(f'Unsupported file type: {file_extension}')
        
    return text

if __name__ == '__main__':
    # Create a dummy documents folder and some test files
    if not os.path.exists('documents'):
        os.makedirs('documents')
    
    with open('documents/test.txt', 'w') as f:
        f.write('This is a test text file.')
        
    # To test docx, you would need a test.docx file in the documents folder.
    # To test pdf, you would need a test.pdf file in the documents folder.

    print("Testing with test.txt:")
    print(extract_text('documents/test.txt'))
    
    # Example of how you would test other files:
    # print("\nTesting with test.docx:")
    # print(extract_text('documents/test.docx'))
    # print("\nTesting with test.pdf:")
    # print(extract_text('documents/test.pdf')) 