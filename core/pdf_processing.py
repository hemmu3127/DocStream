# core/pdf_processing.py
import io
from pypdf import PdfReader, PdfWriter
from typing import List
from streamlit.runtime.uploaded_file_manager import UploadedFile
from PIL import Image

from utils.logger import log

def merge_pdfs(pdf_files: List[UploadedFile]) -> io.BytesIO:
    """
    Merges multiple uploaded PDF files into a single PDF document.
    """
    log.info(f"Starting PDF merge for {len(pdf_files)} files.")
    merger = PdfWriter()
    
    try:
        for pdf_file in pdf_files:
            pdf_file.seek(0)
            merger.append(pdf_file)
        
        merged_pdf_bytes = io.BytesIO()
        merger.write(merged_pdf_bytes)
        merger.close()
        merged_pdf_bytes.seek(0)
        log.info("Successfully completed PDF merge.")
        return merged_pdf_bytes
    except Exception as e:
        log.error(f"An error occurred during PDF merging: {e}")
        raise


def compress_pdf(pdf_file: UploadedFile, quality: int) -> io.BytesIO:
    """
    Compresses a PDF by reducing image quality and removing unnecessary data.

    Args:
        pdf_file: The uploaded PDF file.
        quality: An integer (1-95) for the JPEG quality level.

    Returns:
        A BytesIO object containing the compressed PDF data.
    """
    log.info(f"Starting PDF compression with quality={quality}.")
    pdf_file.seek(0)
    
    reader = PdfReader(pdf_file)
    writer = PdfWriter()

    # Track if we found any images to compress
    images_found = 0
    images_compressed = 0

    for page in reader.pages:
        writer.add_page(page)

    # Compress images
    for page in writer.pages:
        if page.images:
            for image in page.images:
                images_found += 1
                try:
                    # Extract image data
                    pil_image = Image.open(io.BytesIO(image.data))
                    original_format = pil_image.format
                    
                    log.debug(f"Processing image: format={original_format}, mode={pil_image.mode}, size={pil_image.size}")
                    
                    # Convert to RGB if necessary
                    if pil_image.mode in ("RGBA", "LA", "P"):
                        # Handle transparency by converting to RGB with white background
                        if pil_image.mode == "P":
                            pil_image = pil_image.convert("RGBA")
                        
                        if pil_image.mode in ("RGBA", "LA"):
                            background = Image.new("RGB", pil_image.size, (255, 255, 255))
                            if pil_image.mode == "LA":
                                pil_image = pil_image.convert("RGBA")
                            background.paste(pil_image, mask=pil_image.split()[-1])
                            pil_image = background
                    elif pil_image.mode != "RGB":
                        pil_image = pil_image.convert("RGB")

                    # Compress the image as JPEG
                    with io.BytesIO() as output:
                        pil_image.save(output, format="JPEG", quality=quality, optimize=True)
                        output.seek(0)
                        compressed_data = output.read()
                        
                        # Only replace if compression actually reduced size
                        if len(compressed_data) < len(image.data):
                            image.replace(compressed_data)
                            images_compressed += 1
                            log.debug(f"Image compressed: {len(image.data)} -> {len(compressed_data)} bytes")
                        else:
                            log.debug(f"Skipped image compression (would increase size)")
                            
                except Exception as e:
                    log.warning(f"Could not compress an image: {e}. Skipping it.")
                    continue
    
    log.info(f"Found {images_found} images, successfully compressed {images_compressed}")
    
    # Additional compression options
    writer.add_metadata({})  # Remove metadata to save space
    
    # Compress content streams
    for page in writer.pages:
        page.compress_content_streams()
    
    compressed_bytes = io.BytesIO()
    writer.write(compressed_bytes)
    compressed_bytes.seek(0)
    
    log.info("Successfully completed PDF compression.")
    return compressed_bytes


def split_pdf(pdf_file: UploadedFile, page_range: str) -> io.BytesIO:
    """
    Splits a PDF file based on the provided page range string.
    
    Args:
        pdf_file: The uploaded PDF file.
        page_range: A string representing pages to keep (e.g., "1, 3-5, 8").
                    Pages are 1-indexed.
                    
    Returns:
        A BytesIO object containing the split PDF data.
    """
    log.info(f"Starting PDF split with range: {page_range}")
    pdf_file.seek(0)
    reader = PdfReader(pdf_file)
    writer = PdfWriter()
    
    total_pages = len(reader.pages)
    selected_pages = set()
    
    # Parse the page range string
    try:
        parts = [p.strip() for p in page_range.split(',')]
        for part in parts:
            if '-' in part:
                start, end = map(int, part.split('-'))
                # Handle range (inclusive, 1-based to 0-based)
                for i in range(start - 1, end):
                    selected_pages.add(i)
            else:
                # Handle single page
                selected_pages.add(int(part) - 1)
    except ValueError:
        raise ValueError("Invalid page range format. Use numbers and ranges like '1, 3-5'.")
        
    # Sort pages to maintain order
    sorted_pages = sorted(list(selected_pages))
    
    # Validate and add pages
    for page_num in sorted_pages:
        if 0 <= page_num < total_pages:
            writer.add_page(reader.pages[page_num])
        else:
            log.warning(f"Page {page_num + 1} is out of range (Total: {total_pages}). Skipping.")
            
    output_stream = io.BytesIO()
    writer.write(output_stream)
    output_stream.seek(0)
    
    log.info(f"Successfully split PDF. Extracted {len(writer.pages)} pages.")
    return output_stream