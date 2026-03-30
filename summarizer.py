import os
import json
import streamlit as st
from openai import OpenAI


def summarize_text(transcript: str) -> dict:
    """
    Summarize a transcript that may be in any language.
    Always return English output.
    """

    if not transcript or not transcript.strip():
        raise ValueError("Transcript is empty.")

    # ✅ Works for BOTH local + deployed app
    api_key = os.getenv("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError(
            "OpenRouter API key not found. Set OPENROUTER_API_KEY locally or in Streamlit secrets."
        )

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    prompt = f"""
You will receive a YouTube transcript. The transcript may be in any language.

Your job:
1. Understand the transcript
2. Translate it into English
3. Return ONLY valid JSON in this format:

{{
  "english_transcript_preview": "English preview (100-150 words)",
  "tldr": "Short summary",
  "bullet_points": ["point 1", "point 2", "point 3"],
  "key_takeaways": ["takeaway 1", "takeaway 2"]
}}

Rules:
- Output must be in English only
- No markdown
- No explanation outside JSON

Transcript:
\"\"\"
{transcript}
\"\"\"
"""

    try:
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=[
                {"role": "system", "content": "Return only clean JSON in English."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )

        text = response.choices[0].message.content.strip()
        result = json.loads(text)

        return result

    except json.JSONDecodeError:
        raise ValueError("Model returned invalid JSON.")
    except Exception as e:
        raise ValueError(f"English translation and summary failed: {e}")