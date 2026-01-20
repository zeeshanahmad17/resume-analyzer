# AI Resume Analyzer 🚀

A modern, high-performance Resume Analyzer powered by **Google Gemini 1.5 Flash** and **MongoDB Atlas Vector Search**. This tool provides deep semantic analysis of resumes against job descriptions, offering ATS scoring, skill gap analysis, and actionable improvement suggestions.

## ✨ Features

-   **Semantic Analysis**: Uses Google's `text-embedding-004` to perform context-aware matching, going beyond simple keyword searches.
-   **Multi-Format Support**: Seamlessly processes **PDF**, **DOCX**, and **TXT** files.
-   **Intelligent Chunking**: Detects resume sections (Experience, Skills, Education) for more accurate LLM evaluation.
-   **Modern SPA Interface**: A high-contrast, premium dark UI built with Glassmorphism aesthetics and animated scoring.
-   **Detailed Insights**: Provides:
    -   Overall Match Score %
    -   ATS Optimization Score
    -   Matched & Missing Skill Badges
    -   Step-by-step Improvement Recommendations
    -   AI Reasoning for the evaluation

## 🛠️ Tech Stack

-   **Backend**: Python, Flask
-   **AI/LLM**: Google Gemini 1.5 Flash (Analysis), Google Gemini Text Embeddings
-   **Database**: MongoDB Atlas (Vector Search)
-   **Foundational Services**: `pdfplumber`, `python-docx`, `pymongo`
-   **Frontend**: Vanilla JavaScript (ES6+), Modern CSS (Variables, Gradients, Backdrop-blur)

## 🚀 Getting Started

### Prerequisites

-   Python 3.8+
-   Google AI Studio API Key (Gemini)
-   MongoDB Atlas Cluster with Vector Search enabled.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd resume-analyzer
    ```

2.  **Set up a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the root directory:
    ```env
    GEMINI_API_KEY=your_gemini_api_key
    MONGODB_URI=your_mongodb_connection_string
    FLASK_ENV=development
    ```

5.  **Run the application:**
    ```bash
    python app.py
    ```
    Access the UI at `http://127.0.0.1:5000`.

## 🏗️ Architecture

1.  **Ingestion**: Resume text is extracted and intelligently chunked by section.
2.  **Vectorization**: Chunks are converted to 768-dimensional embeddings using Gemini.
3.  **Storage**: Embeddings and metadata are stored in MongoDB Atlas.
4.  **Search**: A semantic search retrieves the most relevant resume parts for the specific job description.
5.  **Analysis**: Gemini 1.5 Flash synthesizes the retrieved chunks and job description into a structured JSON analysis.

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.
