# 🎥📄 YouTube Transcript Summarizer CLI

This is a command-line Python application that extracts the English transcript from a YouTube video and uses the OpenAI API to generate a summary. 
You can provide either a video ID or a full YouTube URL, and choose between three levels of summary detail.


Disclaimer: This application utilizes the OpenAI API. You must have an OpenAI account with funds ($1 should be sufficient for multiple runs) and an API key in order to run this applicaiton.
You can generate an API key here: https://platform.openai.com/api-keys
               
---

## ✨ Features

- Extracts English transcripts from YouTube videos
- Generates summaries using OpenAI's GPT model
- Accepts either a video ID or full YouTube URL
- Choose from 3 summary lengths:
  - `short`: 3 bullet points
  - `medium`: a short paragraph
  - `long`: a multi-paragraph report

---

## ✅ Requirements

- Python 3.7+
- An OpenAI API key
- Internet connection (to fetch transcripts and query the OpenAI API)

---

## 📦 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Bradley-Worthen/YouTubeSummary.git
cd YouTubeSummary

```
### 2. Create and activate a virtual environment (recommended)
```bash
python -m venv venv

# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Create a .env file for your OpenAI API key

In the root of the project directory, create a file called .env and add:
```bash
OPENAI_API_KEY=your-openai-api-key-here
```
Note:
🔐 Do NOT share your API key.

---

## 🚀 Usage
You can provide either a YouTube video ID or a full URL in quotes.
```bash
python yt_summary_cli.py <video-id-or-url> --length <short|medium|long>

### Examples:
# Using a full URL
python yt_summary_cli.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --length long

# Using just a video ID
python yt_summary_cli.py dQw4w9WgXcQ --length short
```
### Notes:
If you do not provide the --length flag, it defaults to short.

If you do not put the URL in quotes and there is a wildcard character present, the terminal shell will return "no matches found"

When you are finished using the application you can deactivate the virtual envrionment by typing "deactivate" in your terminal. 
"(venv)" should no longer be stated on the next line in the terminal window. 

---
## 🗂 Repository Structure
```bash
yt-summary-cli/
├── yt_summary_cli.py     # Main application script
├── requirements.txt      # Python dependencies
├── .gitignore            # Ignores .env and venv/
└── .env                  # (not committed) Your API key goes here
```
