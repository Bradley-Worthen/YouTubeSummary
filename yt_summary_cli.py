import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from urllib.parse import urlparse, parse_qs

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_video_id(input_str):
    """
    Extracts the YouTube video ID from a URL or returns the input if it's already a valid ID.
    Supports:
      - https://www.youtube.com/watch?v=VIDEO_ID
      - https://youtu.be/VIDEO_ID
      - VIDEO_ID (direct)
    """
    try:
        parsed = urlparse(input_str)

        # Handle full YouTube URLs
        if parsed.netloc in ['www.youtube.com', 'youtube.com']:
            query = parse_qs(parsed.query)
            video_id = query.get('v')
            if video_id and len(video_id[0]) == 11:
                return video_id[0]

        # Handle shortened youtu.be URLs
        elif parsed.netloc in ['youtu.be']:
            video_id = parsed.path.lstrip('/')
            if len(video_id) == 11:
                return video_id

    except Exception:
        pass

    # Fallback: Assume it's a raw video ID
    if len(input_str) == 11 and all(c.isalnum() or c in ['-', '_'] for c in input_str):
        return input_str

    raise ValueError("Invalid YouTube video URL or ID.")


def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        full_text = " ".join([entry['text'] for entry in transcript])
        return full_text
    except (TranscriptsDisabled, NoTranscriptFound) as e:
        print(f"Transcript error: {e}")
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
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="YouTube Transcript Summarizer")
    parser.add_argument("video", help="YouTube video URL or ID")
    parser.add_argument("--length", choices=["short", "medium", "long"], default="short",
                        help="Length of summary: short (default), medium, or long")
    args = parser.parse_args()

    video_id = extract_video_id(args.video)

    print(f"Extracted video ID: {video_id}")
    print("Fetching transcript...")

    transcript = get_transcript(video_id)

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
