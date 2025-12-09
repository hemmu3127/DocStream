
import io
from reportlab.pdfgen import canvas
from core.security import encrypt_pdf, decrypt_pdf
from utils.logger import log

def create_dummy_pdf():
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 750, "Hello World")
    c.save()
    buffer.seek(0)
    return buffer

def test_security_logging():
    print("Creating dummy PDF...")
    pdf_file = create_dummy_pdf()
    
    print("Testing Encryption...")
    encrypted_pdf = encrypt_pdf(pdf_file, "password123")
    
    print("Testing Decryption...")
    decrypted_pdf = decrypt_pdf(encrypted_pdf, "password123")
    
    print("Done.")

if __name__ == "__main__":
    test_security_logging()
