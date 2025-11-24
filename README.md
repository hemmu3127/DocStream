# PDF Pro Toolkit

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
git clone https://github.com/hemmu3127/DocStream.git
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