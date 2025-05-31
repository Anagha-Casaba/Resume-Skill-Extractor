import fitz  # PyMuPDF
import re
from typing import Dict, List

def extract_resume_data(file_path: str) -> Dict[str, str]:
    """
    Extracts key information from a PDF resume.

    Args:
        file_path: Path to the PDF resume file

    Returns:
        Dictionary containing extracted information:
        - name: Full name
        - email: Email address
        - phone: Phone number
        - skills: Skills section content
        - experience: Experience section content
    """
    try:
        # Open PDF and extract text
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()

        # Extract name (first non-empty line)
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        name = lines[0] if lines else "Not found"

        # Extract email using regex
        email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
        email = email_match.group(0) if email_match else "Not found"

        # Extract phone number using regex
        phone_match = re.search(r'\+?\d[\d\s\-]{8,15}', text)
        phone = phone_match.group(0) if phone_match else "Not found"

        # Extract sections
        skills_section = extract_section(text, ['Skills', 'Technical Skills', 'Technologies', 'Core Competencies', 'Tools'])
        experience_section = extract_section(text, ['Experience', 'Professional Experience', 'Work Experience', 'Employment History'])

        return {
            "name": name,
            "email": email,
            "phone": phone,
            "skills": skills_section,
            "experience": experience_section
        }

    except Exception as e:
        return {
            "name": "Error",
            "email": f"Error: {str(e)}",
            "phone": "Error",
            "skills": "Error",
            "experience": "Error"
        }

def extract_section(text: str, section_headers: List[str]) -> str:
    """
    Extracts content from a specific section of the resume.

    Args:
        text: Full text of the resume
        section_headers: List of possible section headers to look for

    Returns:
        Cleaned content of the section or "Not found" if not found
    """
    try:
        pattern = r'(?i)(' + '|'.join(section_headers) + r')\s*[\n:]*\s*(.*?)' + \
                  r'(?=\n[A-Z][^\n]{1,100}\n|\Z)'  # Lookahead for next likely section header or end

        matches = re.findall(pattern, text, re.DOTALL)
        if not matches:
            return "Not found"

        # Combine all matching content
        content = " ".join([match[1].strip() for match in matches])

        # Clean content
        content = re.sub(r'\s*[-•*]\s*', ' ', content)  # remove bullet points
        content = re.sub(r'\s+', ' ', content)  # normalize spaces
        content = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '', content)  # remove emails
        content = re.sub(r'\+?\d[\d\s\-]{8,15}', '', content)  # remove phone numbers
        content = re.sub(r'\d{4}\s*[-–]\s*(?:\d{4}|present|current)', '', content, flags=re.IGNORECASE)  # remove years

        return content.strip() or "Not found"

    except Exception as e:
        print(f"Error extracting section: {str(e)}")
        return "Not found"

import json
import csv
import os

import os
import csv
from typing import Dict

def store_data_json(data: Dict[str, str]):
    """
    Appends extracted data to a JSON file.
    """
    try:
        # Use absolute path for Docker
        file_path = "/app/resumes_data.json"
        
        # Create empty list if file doesn't exist
        all_data = []
        
        # Try to read existing data if file exists
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    existing_data = json.load(f)
                    if isinstance(existing_data, list):
                        all_data = existing_data
            except (json.JSONDecodeError, IOError):
                pass  # File exists but is empty or invalid, start fresh

        # Add new data
        all_data.append(data)

        # Write data back to file
        with open(file_path, 'w') as f:
            json.dump(all_data, f, indent=4)

    except Exception as e:
        print(f"Error saving to JSON: {str(e)}")
        raise  # Re-raise the error to be caught by Flask

def store_data_csv(data: Dict[str, str]):
    """
    Appends extracted data to a CSV file in the results folder.
    """
    try:
        # Use absolute path in the container
        file_path = "/app/results/resumes_data.csv"
        
        # Create empty file if it doesn't exist
        if not os.path.exists(file_path):
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["name", "email", "phone", "skills", "experience"])
                writer.writeheader()

        # Append the new data
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["name", "email", "phone", "skills", "experience"])
            writer.writerow(data)

    except Exception as e:
        print(f"Error saving to CSV: {str(e)}")
        raise  # Re-raise the error to be caught by Flask