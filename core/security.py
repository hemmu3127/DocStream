import io
from pypdf import PdfReader, PdfWriter

def encrypt_pdf(file, password):
    """
    Encrypts a PDF file with a password.
    
    Args:
        file: The input PDF file (file-like object).
        password: The password to set.
        
    Returns:
        io.BytesIO: The encrypted PDF content.
    """
    reader = PdfReader(file)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(password)
    
    output_stream = io.BytesIO()
    writer.write(output_stream)
    output_stream.seek(0)
    return output_stream

def decrypt_pdf(file, password):
    """
    Decrypts a PDF file using the provided password.
    
    Args:
        file: The input PDF file (file-like object).
        password: The password to unlock the file.
        
    Returns:
        io.BytesIO: The decrypted PDF content.
    """
    reader = PdfReader(file)
    
    if reader.is_encrypted:
        reader.decrypt(password)

    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
        
    output_stream = io.BytesIO()
    writer.write(output_stream)
    output_stream.seek(0)
    return output_stream
