# app.py
import streamlit as st
import os
from dotenv import load_dotenv

# Import core processing functions
from core.image_processing import convert_images_to_pdf
from core.pdf_processing import merge_pdfs, compress_pdf, split_pdf, rotate_pdf_pages
from core.security import encrypt_pdf, decrypt_pdf

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
    ["Convert Images to PDF", "Merge PDFs", "Compress PDF", "Split PDF", "Rotate PDF", "Secure PDF"]
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

elif app_mode == "Split PDF":
    st.header("Split PDF")
    st.info("Extract specific pages from your PDF.")
    
    uploaded_pdf = st.file_uploader("Upload PDF to Split", type="pdf")
    
    if uploaded_pdf:
        st.write("Enter page numbers and/or ranges separated by commas (e.g., '1, 3-5, 8').")
        page_range = st.text_input("Page Range", placeholder="1, 3-5")
        
        if page_range:
            if st.button("Split PDF", type="primary"):
                with st.spinner("Splitting PDF..."):
                    try:
                        split_pdf_bytes = split_pdf(uploaded_pdf, page_range)
                        st.success("✅ PDF Split Successfully!")
                        st.download_button(
                            label="📥 Download Split PDF",
                            data=split_pdf_bytes,
                            file_name=f"split_{uploaded_pdf.name}",
                            mime="application/pdf"
                        )
                    except ValueError as ve:
                        st.error(f"Invalid input: {ve}")
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
                        log.error(f"Split failed: {e}")

elif app_mode == "Rotate PDF":
    st.header("Rotate PDF Pages")
    st.info("Rotate pages in your PDF document.")

    uploaded_pdf = st.file_uploader("Upload PDF to Rotate", type="pdf")

    if uploaded_pdf:
        rotation = st.selectbox(
            "Rotation Angle (Clockwise)",
            options=[90, 180, 270],
            format_func=lambda x: f"{x} degrees"
        )
        
        rotation_scope = st.radio("Rotate Pages", ["All Pages", "Specific Pages"])
        page_range = None
        
        if rotation_scope == "Specific Pages":
            st.write("Enter page numbers and/or ranges separated by commas (e.g., '1, 3-5, 8').")
            page_range = st.text_input("Page Range (Rotation)", placeholder="1, 3-5")

        if st.button("Rotate PDF", type="primary"):
            if rotation_scope == "Specific Pages" and not page_range:
                st.warning("⚠️ Please enter a page range.")
            else:
                with st.spinner("Rotating PDF..."):
                    try:
                        rotated_pdf = rotate_pdf_pages(uploaded_pdf, rotation, page_range)
                        st.success("✅ PDF Rotated Successfully!")
                        st.download_button(
                            label="📥 Download Rotated PDF",
                            data=rotated_pdf,
                            file_name=f"rotated_{uploaded_pdf.name}",
                            mime="application/pdf"
                        )
                    except ValueError as ve:
                        st.error(f"Invalid input: {ve}")
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
                        log.error(f"Rotation failed: {e}")

elif app_mode == "Secure PDF":
    st.header("Secure PDF")
    st.info("Encrypt or Decrypt your PDF files.")
    
    action = st.radio("Choose Action", ["Encrypt", "Decrypt"])
    
    if action == "Encrypt":
        st.subheader("Encrypt PDF")
        uploaded_pdf = st.file_uploader("Upload PDF to Encrypt", type="pdf")
        password = st.text_input("Enter Password", type="password")
        
        if uploaded_pdf and password:
            if st.button("Encrypt PDF", type="primary"):
                with st.spinner("Encrypting..."):
                    try:
                        encrypted_pdf = encrypt_pdf(uploaded_pdf, password)
                        st.success("✅ PDF Encrypted Successfully!")
                        st.download_button(
                            label="📥 Download Encrypted PDF",
                            data=encrypted_pdf,
                            file_name=f"encrypted_{uploaded_pdf.name}",
                            mime="application/pdf"
                        )
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
                        log.error(f"Encryption failed: {e}")
                        
    elif action == "Decrypt":
        st.subheader("Decrypt PDF")
        uploaded_pdf = st.file_uploader("Upload Encrypted PDF", type="pdf")
        password = st.text_input("Enter Password", type="password")
        
        if uploaded_pdf and password:
            if st.button("Decrypt PDF", type="primary"):
                with st.spinner("Decrypting..."):
                    try:
                        decrypted_pdf = decrypt_pdf(uploaded_pdf, password)
                        st.success("✅ PDF Decrypted Successfully!")
                        st.download_button(
                            label="📥 Download Decrypted PDF",
                            data=decrypted_pdf,
                            file_name=f"decrypted_{uploaded_pdf.name}",
                            mime="application/pdf"
                        )
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
                        log.error(f"Decryption failed: {e}")