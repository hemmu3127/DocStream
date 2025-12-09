import io
from pypdf import PdfReader, PdfWriter
from utils.logger import log

def encrypt_pdf(file, password):
    """
    Encrypts a PDF file with a password.
    
    Args:
        file: The input PDF file (file-like object).
        password: The password to set.
        
    Returns:
        io.BytesIO: The encrypted PDF content.
    """
    log.info("Starting PDF encryption.")
    try:
        reader = PdfReader(file)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        writer.encrypt(password)
        
        output_stream = io.BytesIO()
        writer.write(output_stream)
        output_stream.seek(0)
        log.info("Successfully encrypted PDF.")
        return output_stream
    except Exception as e:
        log.error(f"PDF encryption failed: {e}")
        raise

def decrypt_pdf(file, password):
    """
    Decrypts a PDF file using the provided password.
    
    Args:
        file: The input PDF file (file-like object).
        password: The password to unlock the file.
        
    Returns:
        io.BytesIO: The decrypted PDF content.
    """
    log.info("Starting PDF decryption.")
    try:
        reader = PdfReader(file)
        
        if reader.is_encrypted:
            reader.decrypt(password)
        else:
            log.warning("PDF is not encrypted, proceeding without decryption.")

        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
            
        output_stream = io.BytesIO()
        writer.write(output_stream)
        output_stream.seek(0)
        log.info("Successfully decrypted PDF.")
        return output_stream
    except Exception as e:
        log.error(f"PDF decryption failed: {e}")
        raise
