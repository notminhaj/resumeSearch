# ResumeSearch

ResumeSearch is a tool designed to help users search and analyze resumes efficiently using advanced language models.

## Features

- **Resume Upload**: Upload multiple resumes in PDF format.
- **Job Description Matching**: Find the best candidate matches based on job descriptions.
- **AI-Powered Ranking**: Utilize Mistral's language model to rank candidates effectively.

## Prerequisites

- Python 3.x
- [Mistral API Key](https://mistral.ai/signup) (subscribe to their free plan)
- [Git](https://git-scm.com/)
- [Virtualenv](https://docs.python.org/3/library/venv.html)

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/notminhaj/resumeSearch.git
   cd resumeSearch
   ```

2. **Set Up a Virtual Environment**:

   ```bash
   python -m venv resumeChat
   ```

3. **Activate the Virtual Environment**:

   - On Windows:

     ```bash
     resumeChat\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source resumeChat/bin/activate
     ```

4. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Configure Mistral API Key**:

   - Obtain your API key from [Mistral](https://mistral.ai/signup).
   - Add your API key to the `resumeChat.py` file:

     ```python
     MISTRAL_API_KEY = "your_api_key_here"
     ```

## Usage

1. **Run the Application**:

   ```bash
   python main.py
   ```

2. **Access the Web Interface**:

   Open your web browser and navigate to `http://127.0.0.1:5000/`.

3. **Upload Resumes**:

   - Click on the "Upload Resumes" section.
   - Select multiple PDF files to upload.

4. **Search for Candidates**:

   - Enter the job description in the search bar.
   - Specify the number of top candidates to display.
   - Click "Search" to view ranked candidates based on the job description.
