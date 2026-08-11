import os
import io
import pymupdf as fitz
import pytesseract
from PIL import Image
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Configure Tesseract path if specified in environment
TESSERACT_CMD = os.getenv("TESSERACT_CMD")
if TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD
else:
    # Try common default paths for macOS Homebrew if not in PATH already
    common_paths = [
        "/usr/local/bin/tesseract",
        "/opt/homebrew/bin/tesseract",
    ]
    for path in common_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            break

def extract_text_from_pdf(pdf_file, progress_callback=None):
    """
    Extracts text from a PDF file using a hybrid approach:
    1. Try to extract native text using PyMuPDF.
    2. If text is sparse (scanned page), render page as image and run Tesseract OCR.
    
    Args:
        pdf_file: A path to a PDF file or a file-like object (bytes).
        progress_callback: A function that accepts (progress_float, status_message).
    
    Returns:
        str: The full text of the document.
    """
    # Open document
    if isinstance(pdf_file, bytes):
        doc = fitz.open(stream=pdf_file, filetype="pdf")
    else:
        doc = fitz.open(pdf_file)
        
    total_pages = len(doc)
    full_text_parts = []
    
    for i in range(total_pages):
        page = doc.load_page(i)
        
        # 1. Try native text extraction
        text = page.get_text().strip()
        method_used = "Native Text"
        
        # 2. Fall back to OCR if page has very little native text
        if len(text) < 100:
            method_used = "Tesseract OCR"
            try:
                # Update progress
                if progress_callback:
                    progress_callback((i + 0.2) / total_pages, f"Rendering page {i+1} of {total_pages} for OCR...")
                
                # Render page to high-DPI pixmap
                pix = page.get_pixmap(dpi=150)
                img_data = pix.tobytes("png")
                
                # Update progress
                if progress_callback:
                    progress_callback((i + 0.5) / total_pages, f"Running OCR on page {i+1} of {total_pages}...")
                
                # Load image and run OCR
                img = Image.open(io.BytesIO(img_data))
                text = pytesseract.image_to_string(img).strip()
            except Exception as e:
                text = f"[OCR Failed on this page: {str(e)}]"
                method_used = "Failed OCR"
        
        # Format page header
        page_content = f"--- PAGE {i + 1} ({method_used}) ---\n{text}\n"
        full_text_parts.append(page_content)
        
        # Update page progress
        if progress_callback:
            progress_callback((i + 1) / total_pages, f"Completed page {i+1} of {total_pages} ({method_used})...")
            
    doc.close()
    return "\n".join(full_text_parts)

def check_tesseract():
    """
    Verifies if Tesseract OCR is installed and available on PATH or config.
    
    Returns:
        bool: True if available, False otherwise.
    """
    try:
        pytesseract.get_tesseract_version()
        return True
    except Exception:
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2 and sys.argv[1] == "--test":
        test_pdf = sys.argv[2]
        print(f"Testing OCR on {test_pdf}...")
        
        def print_progress(progress, message):
            print(f"[{progress*100:.1f}%] {message}")
            
        try:
            extracted = extract_text_from_pdf(test_pdf, print_progress)
            print("\n--- SAMPLE EXTRACTED TEXT (First 500 chars) ---")
            print(extracted[:500])
            print("---------------------------------------------")
            print(f"Success! Total extracted length: {len(extracted)} chars.")
        except Exception as e:
            print(f"Error during test: {e}")
    else:
        print("Usage: python app/ocr.py --test <path_to_pdf>")
