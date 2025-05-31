# Resume Extractor

A web-based application that extracts key information from PDF resumes and stores the extracted data in multiple formats.

## Features

- Extracts important information from PDF resumes including:
  - Name
  - Email
  - Phone number
  - Skills section
  - Experience section
- Stores extracted data in multiple formats:
  - Individual JSON files per resume
  - Central JSON database
  - CSV format for easy analysis
- Web-based interface for easy uploads and viewing results
- Docker container support for easy deployment

## Prerequisites

- Python 3.9 or higher
- Docker (for containerized deployment)
- PyMuPDF (for PDF processing)

## Installation

### Option 1: Using Docker (Recommended)

```bash
# Build the Docker image
docker build -t resume_extractor .

# Run the container
docker run -p 5000:5000 resume_extractor


## Usage

1. Access the application at `http://localhost:5000`
2. Click "Choose File" to select a PDF resume
3. Click "Upload" to process the resume
4. View the extracted information on the same page
5. Access previous results at `/results` endpoint

## Data Storage

The application stores extracted data in multiple formats:

1. Individual JSON files in the `results` folder (one per resume)
2. Central JSON database (`resumes_data.json`)
3. CSV database (`resumes_data.csv` in results folder)

### Accessing Stored Data ###

# Using Docker
```bash
# Copy CSV file from container
docker cp <container_id>:/app/results/resumes_data.csv .

# Copy JSON files from container
docker cp -a <container_id>:/app/results .
```

#### Using Local Installation
All data files are stored in the `results` directory of the project.

## Directory Structure

```
resume_extractor/
├── app.py              # Main Flask application
├── static/             # Static files (CSS, JS)
├── templates/          # HTML templates
│   ├── index.html     # Main upload page
│   └── results.html   # Results page
├── resumes/           # Directory for uploaded PDFs
├── results/           # Directory for processed results
├── resumes_data.json  # Central JSON database
├── resumes_data.csv   # CSV database
└── requirements.txt   # Python dependencies
```

## Data Format

The CSV file contains the following columns:
- name: Full name extracted from resume
- email: Email address
- phone: Phone number
- skills: Skills section content
- experience: Experience section content

## Acknowledgments

- PyMuPDF for PDF processing capabilities
- Flask for the web framework
- Docker for container support
