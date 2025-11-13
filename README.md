# PDF Pro Toolkit

A production-grade Streamlit application for common PDF manipulation tasks, including image-to-PDF conversion, PDF merging, and PDF compression.

## Features

- **Convert Images to PDF**: Upload multiple PNG or JPEG files and convert them into a single, multi-page PDF.
- **Merge PDFs**: Combine several PDF documents into one.
- **Compress PDF**: Reduce the file size of a PDF using lossless compression.

## Project Structure

The project is organized into a modular structure to ensure maintainability and scalability:

- `app.py`: The main entry point for the Streamlit application (UI layer).
- `core/`: Contains the core business logic for PDF and image processing.
- `utils/`: Includes utility modules like the centralized logger.
- `requirements.txt`: A list of all Python dependencies with pinned versions.
- `.env`: A configuration file for environment-specific variables.

## Setup and Installation

### Prerequisites

- Python 3.8+
- `pip` for package management

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd pdf_tool
```

### 2. Install the requirements

```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit app 
```bash
streamlit run app.py
```