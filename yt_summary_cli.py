import os
import re
from dotenv import load_dotenv
import argparse
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

# Use an environment variable for security
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY')) 

def extract_video_id(input_str):
    """
    Extracts the YouTube video ID from a full URL or returns the ID as is if input is already an ID.
    """
    # Check for full URL format
    url_patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",  # Handles v=ID or /ID
    ]

    for pattern in url_patterns:
        match = re.search(pattern, input_str)
        if match:
            return match.group(1)

    # Fallback: assume input is already a video ID
    return input_str

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        full_text = " ".join([entry['text'] for entry in transcript])
        return full_text
    except (TranscriptsDisabled, NoTranscriptFound) as e:
        print(f"Error: {e}")
        return None

def summarize_text(transcript, length='short'):
    prompts = {
        'short': "Summarize the following transcript in three bullet points highlighting the main takeaways:\n\n",
        'medium': "Provide a short paragraph summary of the following transcript:\n\n",
        'long': "Write a detailed multi-paragraph report based on the following transcript:\n\n"
    }

    if length not in prompts:
        raise ValueError("Summary length must be 'short', 'medium', or 'long'.")

    prompt = prompts[length] + transcript

    try:
        response = client.chat.completions.create(model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7)
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="YouTube Transcript Summarizer")
    parser.add_argument("video_id", help="YouTube video ID (e.g., dQw4w9WgXcQ)")
    parser.add_argument("--length", choices=["short", "medium", "long"], default="short",
                        help="Length of summary: short (default), medium, or long")
    args = parser.parse_args()

    print("Fetching transcript...")
    transcript = get_transcript(args.video_id)

    if not transcript:
        print("Failed to fetch transcript.")
        return

    print("Generating summary...")
    summary = summarize_text(transcript, args.length)

    if summary:
        print("\n--- Summary ---\n")
        print(summary)
    else:
        print("Failed to generate summary.")

if __name__ == "__main__":
    main()
