import PyPDF2
import docx
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"pdf", "docx", "doc", "txt"}


def allowed_file(filename):
    """
    Check if the file has an allowed extension.

    Args:
        filename (str): The name of the file to check.

    Returns:
        bool: True if the file has an allowed extension, False otherwise.
    """

    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file):
    """
    Extract text from a PDF file.
    
    Args:
        file: File object from Flask request.
        
    Returns:
        str: The extracted text.
    """
    
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text.strip()
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")
    
def extract_text_from_docx(file):
    """
    Extract text from a DOCX file.
    Args:
        file: File ojbect from Flask request.
        
    Returns:
        str: The extracted text
    """
    
    try:
        doc = docx.Document(file)
        text = ""
        
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        
        return text.strip()
    except Exception as e:
        raise Exception(f"Error reading DOCX: {str(e)}")
    
def extract_text_from_txt(file):
    """
    Extract text from a TXT file.
    Args:
        file: File object from Flask request.
    
    Returns:
        str: The extracted text.
    """
    try:
        # Try UTF-8 first
        content = file.read()
        
        # Try different encodings
        for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']:
            try:
                text = content.decode(encoding)
                return text.strip()
            except (UnicodeDecodeError, AttributeError):
                continue
        
        # If all encodings fail
        raise Exception("Could not decode text file with supported encodings")
        
    except Exception as e:
        raise Exception(f"Error reading TXT: {str(e)}")
    
def process_file(file):
    """
    Process the uploaded file and extract text based on its type.
    
    Args:
        file: File object from Flask request.
    
    Returns:
        str: The extracted text.
    """
    if not file:
        raise ValueError("No file provided.")

    filename = secure_filename(file.filename)
    
    if not allowed_file(filename):
        raise Exception("File type not allowed. Allowed types are: pdf, docx, doc, txt.")
    
    file_ext = filename.rsplit(".", 1)[1].lower()
    
    if file_ext == 'pdf':
        return extract_text_from_pdf(file)
    elif file_ext == 'docx' or file_ext == 'doc':
        return extract_text_from_docx(file)
    elif file_ext == 'txt':
        return extract_text_from_txt(file)
    else:
        raise Exception("Unsupported file type.")
    
    
# Example usage:
if __name__ == "__main__":
    print("=== File Processor Test ===")
    print("This module is meant to be used with Flask file uploads.")
    print("\nTo test manually:")
    print("1. Start the Flask server")
    print("2. Use the web interface or curl to upload a file")
    print("\nSupported formats: PDF, DOCX, TXT")
    print("========================")