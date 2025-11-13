# core/image_processing.py
import io
import tempfile
import os
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from typing import List
from streamlit.runtime.uploaded_file_manager import UploadedFile

from utils.logger import log

def convert_images_to_pdf(image_files: List[UploadedFile]) -> io.BytesIO:
    """
    Converts a list of uploaded image files into a single, multi-page PDF.
    This version uses a temporary file with explicit resource management to prevent file-locking errors.

    Args:
        image_files: A list of Streamlit UploadedFile objects (images).

    Returns:
        A BytesIO object containing the generated PDF data.
    """
    log.info(f"Starting PDF conversion for {len(image_files)} images.")
    pdf_bytes = io.BytesIO()
    
    c = canvas.Canvas(pdf_bytes, pagesize=letter)
    width, height = letter

    for i, img_file in enumerate(image_files):
        temp_img_path = None  # Initialize path to None
        try:
            img_file.seek(0)
            
            # Create a temporary file path with the correct extension
            suffix = os.path.splitext(img_file.name)[1]
            # Use tempfile.mkstemp() to get a path and a low-level file handle
            fd, temp_img_path = tempfile.mkstemp(suffix=suffix)
            os.close(fd) # Immediately close the handle, we just need the path

            log.debug(f"Processing image {i+1}: {img_file.name}. Created temp file at: {temp_img_path}")
            
            # Write the uploaded file's content to the temporary path
            with open(temp_img_path, 'wb') as temp_out:
                temp_out.write(img_file.getvalue())

            # --- THE DEFINITIVE FIX ---
            # Use a 'with' statement for Pillow to ensure its file handle is
            # closed immediately after getting the dimensions.
            with Image.open(temp_img_path) as img_pil:
                img_width, img_height = img_pil.size
            # --- The file handle from Image.open() is now guaranteed to be closed ---

            aspect = img_height / float(img_width)
            scaled_width = width
            scaled_height = width * aspect
            if scaled_height > height:
                scaled_height = height
                scaled_width = height / aspect

            x_centered = (width - scaled_width) / 2
            y_centered = (height - scaled_height) / 2
            
            # Pass the FILE PATH to drawImage. This works reliably.
            c.drawImage(temp_img_path, x_centered, y_centered, width=scaled_width, height=scaled_height, preserveAspectRatio=True, mask='auto', anchor='c')
            
            c.showPage()

        except Exception as e:
            log.error(f"Failed to process image {img_file.name}: {e}", exc_info=True)
            raise  # Re-raise the exception to be handled by the UI
        finally:
            # The 'finally' block ensures cleanup happens no matter what.
            if temp_img_path and os.path.exists(temp_img_path):
                os.remove(temp_img_path)
                log.debug(f"Successfully cleaned up temp file: {temp_img_path}")

    c.save()
    pdf_bytes.seek(0)
    log.info("Successfully completed PDF conversion.")
    return pdf_bytes