# app.py
import streamlit as st
import os
from dotenv import load_dotenv

# Import core processing functions
from core.image_processing import convert_images_to_pdf
from core.pdf_processing import merge_pdfs, compress_pdf  # <-- Updated import

# Import logger
from utils.logger import log

# Load environment variables from .env file
load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title=os.getenv("APP_TITLE", "PDF Toolkit"),
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Main Application UI ---
st.title(os.getenv("APP_TITLE"))
st.markdown("Your one-stop, production-grade solution for common PDF tasks.")

# --- Sidebar for Navigation ---
st.sidebar.title("Features")
app_mode = st.sidebar.selectbox(
    "Choose the feature you want to use",
    ["Convert Images to PDF", "Merge PDFs", "Compress PDF"]
)

if app_mode == "Convert Images to PDF":
    st.header("Convert Multiple Images to a Single PDF")
    st.info("Upload PNG or JPEG files. They will be converted into a single PDF in the order of upload.")

    uploaded_images = st.file_uploader(
        "Upload image files",
        type=["png", "jpeg", "jpg"],
        accept_multiple_files=True
    )

    if uploaded_images:
        if st.button("Convert to PDF", type="primary"):
            with st.spinner("Converting images to PDF..."):
                try:
                    pdf_bytes = convert_images_to_pdf(uploaded_images)
                    st.success("✅ Images successfully converted!")
                    st.download_button(
                        label="📥 Download PDF",
                        data=pdf_bytes,
                        file_name="converted_images.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"An error occurred during conversion: {e}")
                    log.error(f"Image to PDF conversion failed: {e}")

elif app_mode == "Merge PDFs":
    st.header("Merge Multiple PDFs into One")
    st.info("Upload two or more PDF files to combine them into a single document.")

    uploaded_pdfs = st.file_uploader(
        "Upload PDF files to merge",
        type="pdf",
        accept_multiple_files=True
    )

    if uploaded_pdfs:
        if st.button("Merge PDFs", type="primary"):
            if len(uploaded_pdfs) < 2:
                st.warning("⚠️ Please upload at least two PDF files to merge.")
            else:
                with st.spinner("Merging PDFs..."):
                    try:
                        merged_pdf_bytes = merge_pdfs(uploaded_pdfs)
                        st.success("✅ PDFs merged successfully!")
                        st.download_button(
                            label="📥 Download Merged PDF",
                            data=merged_pdf_bytes,
                            file_name="merged_document.pdf",
                            mime="application/pdf"
                        )
                    except Exception as e:
                        st.error(f"An error occurred during merging: {e}")
                        log.error(f"PDF merging failed: {e}")

elif app_mode == "Compress PDF":
    st.header("Compress PDF")
    st.info("Upload a PDF and adjust the compression quality. Lower quality = smaller file size.")

    uploaded_pdf = st.file_uploader(
        "Upload a PDF file to compress",
        type="pdf"
    )

    if uploaded_pdf:
        original_size_kb = len(uploaded_pdf.getvalue()) / 1024
        st.write(f"**Original file size:** {original_size_kb:.2f} KB")

        quality = st.slider(
            label="Compression Quality",
            min_value=1,
            max_value=95,
            value=50,
            step=5,
            help="Lower values = more compression (smaller file size, lower quality). Higher values = less compression (larger file size, better quality)."
        )

        if st.button("Compress PDF", type="primary"):
            with st.spinner("Compressing PDF..."):
                try:
                    compressed_pdf_bytes = compress_pdf(uploaded_pdf, quality)
                    
                    compressed_size_kb = len(compressed_pdf_bytes.getvalue()) / 1024
                    reduction = (original_size_kb - compressed_size_kb) / original_size_kb * 100 if original_size_kb > 0 else 0

                    st.success("✅ PDF compressed successfully!")
                    st.info(f"Original size: {original_size_kb:.2f} KB")
                    st.info(f"**Compressed size: {compressed_size_kb:.2f} KB**")
                    st.info(f"File size reduced by: {reduction:.2f}%")

                    st.download_button(
                        label="📥 Download Compressed PDF",
                        data=compressed_pdf_bytes,
                        file_name=f"compressed_{uploaded_pdf.name}",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"An error occurred during compression: {e}")
                    log.error(f"PDF compression failed: {e}", exc_info=True)