# Interview Question & Answer Generator AI

This project is a web application that automatically generates interview-style questions and their corresponding answers from a given PDF document. It leverages the power of Large Language Models (LLMs) through LangChain and Google's Generative AI to create a study guide or a question bank from your documents.

The application is built with Streamlit, providing a simple and interactive user interface for uploading PDFs and viewing the results.

## 🚀 Features

-   **Easy PDF Upload**: Simply upload any PDF document through the web interface.
-   **Automated Question Generation**: The AI analyzes the content of the PDF and generates relevant questions.
-   **AI-Powered Answer Generation**: For each generated question, the application creates a detailed answer based on the information within the document.
-   **Interactive UI**: A clean and user-friendly interface built with Streamlit.
-   **Progress Tracking**: Real-time progress bars to keep you updated on the generation process.
-   **CSV Export**: Download the generated questions and answers as a CSV file for offline use.
-   **Data Preview**: View the generated Q&A pairs directly in the app before downloading.

## 🛠️ How It Works

The application follows a sophisticated pipeline to process your documents and generate Q&A pairs:

1.  **PDF Loading**: The uploaded PDF is loaded and its text content is extracted.
2.  **Text Chunking**: The extracted text is split into smaller, manageable chunks to be processed by the LLM.
3.  **Question Generation**: A specialized LangChain chain (`load_summarize_chain` with a "refine" strategy) is used with a Google Gemini model to iteratively generate a list of questions from the text chunks.
4.  **Vector Store Creation**: The text chunks are converted into vector embeddings using Google's embedding model and stored in a FAISS vector store. This creates a searchable knowledge base from your document.
5.  **Answer Generation (RAG)**: For each generated question, a Retrieval-Augmented Generation (RAG) chain (`RetrievalQA`) is used. It retrieves the most relevant text chunks from the vector store and uses them as context for the LLM to generate an accurate answer.
6.  **Display and Export**: The final list of questions and answers is displayed in a table and made available for download as a CSV file.

## 🔧 Tech Stack

-   **Backend**: Python
-   **Web Framework**: Streamlit
-   **LLM Orchestration**: LangChain
-   **AI/LLM Provider**: Google Generative AI (Gemini)
-   **Vector Store**: FAISS (Facebook AI Similarity Search)
-   **File Handling**: PyPDFLoader

## ⚙️ Setup and Installation

Follow these steps to get the project running on your local machine.

### Prerequisites

-   Python 3.9+
-   A Google API Key with the "Generative Language API" enabled.

### 1. Clone the Repository

```bash
git clone https://github.com/pugazhmukilan/InterviewQuestion-GeneratorAI.git
cd InterviewQuestion-GeneratorAI
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install all the required Python packages.

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a file named `.env` in the root directory of the project and add your Google API key:

```
GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY_HERE"
```

## ▶️ How to Run

Once the setup is complete, you can run the Streamlit application with the following command:

```bash
streamlit run app.py
```

This will start the web server and open the application in your default web browser.

## Usage

1.  Open the application in your browser.
2.  Click on the "Upload your PDF file" button and select a PDF from your local machine.
3.  Wait for the application to process the file. You will see a progress bar indicating the status.
4.  Once processing is complete, a preview of the generated questions and answers will be displayed.
5.  Click the "Download CSV" button to save the results to your computer.
