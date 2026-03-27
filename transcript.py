"""
Simple YouTube transcript extractor for beginners.
Extracts video IDs from YouTube URLs and fetches their transcripts.
"""

import re
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str) -> str:
    """
    Extract the video ID from a YouTube URL.

    Supports:
    - Standard URLs: https://www.youtube.com/watch?v=VIDEO_ID
    - Short URLs: https://youtu.be/VIDEO_ID

    Args:
        url (str): The YouTube URL

    Returns:
        str: The extracted 11-character video ID

    Raises:
        ValueError: If the URL is empty or invalid
    """
    if not url or not url.strip():
        raise ValueError("YouTube URL cannot be empty.")

    url = url.strip()

    standard_pattern = r"(?:https?://)?(?:www\.)?(?:m\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})"
    short_pattern = r"(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]{11})"

    for pattern in (standard_pattern, short_pattern):
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    raise ValueError(
        "Invalid YouTube URL. Please use a valid video link such as:\n"
        "- https://www.youtube.com/watch?v=VIDEO_ID\n"
        "- https://youtu.be/VIDEO_ID"
    )


def get_transcript(url: str) -> str:
    """
    Fetch the transcript from a YouTube video and return it as plain text.
    
    First attempts to fetch an English transcript.
    If English is not available, falls back to any available transcript.

    Args:
        url (str): The YouTube video URL

    Returns:
        str: The complete transcript as a single string

    Raises:
        ValueError: If the URL is invalid or no transcript is available
    """
    video_id = extract_video_id(url)
    
    api = YouTubeTranscriptApi()

    # Try to fetch English transcript first
    try:
        transcript_data = api.fetch(video_id, languages=["en"])
        transcript_text = " ".join(snippet.text for snippet in transcript_data).strip()
        
        if not transcript_text:
            raise ValueError("Transcript was fetched but appears to be empty.")
        
        return transcript_text

    except Exception:
        # English not available; try any available transcript
        try:
            transcript_list = api.list(video_id)
            
            # Get the first available transcript by iterating
            first_transcript = None
            for transcript in transcript_list:
                first_transcript = transcript
                break
            
            if first_transcript is None:
                raise ValueError(
                    "No transcripts available for this video. "
                    "The video may not have captions enabled."
                )
            
            # Fetch the transcript
            transcript_data = first_transcript.fetch()
            transcript_text = " ".join(snippet.text for snippet in transcript_data).strip()
            
            if not transcript_text:
                raise ValueError("Transcript was fetched but appears to be empty.")
            
            return transcript_text
        
        except Exception as e:
            raise ValueError(f"Failed to fetch transcript: {e}")


if __name__ == "__main__":
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    try:
        transcript = get_transcript(test_url)
        print("\n--- TRANSCRIPT PREVIEW ---\n")
        print(transcript[:500])  # show first 500 chars only
    except Exception as e:
        print(f"\nERROR: {e}")