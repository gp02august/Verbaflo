# Implementation Approach for Resume Generator

This document outlines the approach to implement the HTML Resume Generator application using Flask, OpenAI, and PyPDF2.

## Overview

The application allows users to upload LinkedIn PDF resumes, converts them into HTML format using OpenAI's GPT model, and provides a downloadable HTML file.

## 1. Project Setup

### 1.1. Install Dependencies

Create a virtual environment and install the required packages:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install Flask OpenAI PyPDF2 python-dotenv
OPENAI_API_KEY=your_openai_api_key
python app.py
Open your web browser and navigate to http://127.0.0.1:5000.
```


**Upload a PDF File**

* Go to the home page.
* Click on the file input field and select a PDF file.
* Click the "Upload" button.

**Generate and Download HTML Resume**

After uploading, the application will process the file and convert it into an HTML resume.

The HTML resume will be available for download once the process is complete.
**1.2 Directory Structure**
resume-generator/
│
├── app.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── uploads/ (for storing uploaded PDF files)
├── README.md
├── requirements.txt
└── .env (for storing the OpenAI API key)
