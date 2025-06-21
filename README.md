# Automated Metadata Generation

## Project Overview

This project provides an automated system for generating rich metadata from various document types, including `.txt`, `.docx`, and `.pdf` files. The primary goal is to enhance document discoverability and analysis by automatically extracting text, performing Optical Character Recognition (OCR) on scanned documents, and generating a concise summary and key file statistics. The system features a user-friendly web interface for easy document upload and metadata visualization.

## Features

- **Multi-Format Support**: Extracts text from `.txt`, `.docx`, and both text-based and scanned `.pdf` files.
- **Automated OCR**: Automatically uses Tesseract for OCR on PDFs where direct text extraction fails.
- **Advanced Summarization**: Leverages the `google/pegasus-xsum` model from Hugging Face to generate high-quality, abstractive summaries.
- **Structured Metadata**: Outputs key information including a summary, filename, file size, and word count.
- **Web Interface**: A clean, modern web app built with Flask for uploading files and viewing results.
- **Interactive UI**: Features include drag-and-drop file uploads and a "copy summary" button.

## Project Structure

```
.
├── app.py                      # Main Flask application file
├── extraction.py               # Module for text extraction logic
├── metadata.py                 # Module for metadata and summary generation
├── notebook_generator.py       # Script to generate the final notebook
├── requirements.txt            # Project dependencies
├── templates/
│   ├── index.html              # Upload page for the web app
│   └── results.html            # Results page for the web app
├── uploads/                    # Temporary folder for file uploads
└── Automated Meta Data Generation.ipynb  # Jupyter Notebook with the full code pipeline
```

## Setup and Installation

Follow these steps to set up the project locally.

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd <repository-folder>
```

### 2. Install Python Dependencies
It is recommended to use a virtual environment.
```bash
pip install -r requirements.txt
```

### 3. Install External Dependencies (Required for OCR)

#### Tesseract-OCR
- **Purpose**: Used for extracting text from images and scanned PDFs.
- **Windows**: Download and install from the [official Tesseract installer for Windows](https://github.com/UB-Mannheim/tesseract/wiki). Make sure to add the installation directory (e.g., `C:\Program Files\Tesseract-OCR`) to your system's `PATH` environment variable.
- **Linux (Debian/Ubuntu)**: `sudo apt-get install tesseract-ocr`
- **macOS**: `brew install tesseract`

#### Poppler
- **Purpose**: Used by the `pdf2image` library to convert PDF pages into images for OCR.
- **Windows**: Download the [latest Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases/). Extract it and add the `bin` folder (e.g., `C:\path\to\poppler-xx\bin`) to your system's `PATH`.
- **Linux (Debian/Ubuntu)**: `sudo apt-get install poppler-utils`
- **macOS**: `brew install poppler`

## How to Run the Web App

Once all dependencies are installed, you can start the Flask web server:

```bash
python app.py
```

The application will be available at **http://127.0.0.1:5001**. The first time you run it, the script will download the summarization model from Hugging Face, which may take several minutes.
