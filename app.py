"""Responsive Streamlit app for YouTube video summarizer."""

import streamlit as st
from transcript import get_transcript
from summarizer import summarize_text


st.set_page_config(
    page_title="YouTube Summarizer",
    page_icon="📺",
    layout="centered",
)


def inject_css():
    st.markdown(
        """
        <style>
        .main {
            padding-top: 1.2rem;
            padding-bottom: 2rem;
        }

        .block-container {
            max-width: 850px;
            padding-top: 1rem;
            padding-bottom: 2rem;
        }

        .hero-box {
            padding: 1.2rem;
            border-radius: 18px;
            background: linear-gradient(135deg, #111827, #1f2937);
            color: white;
            margin-bottom: 1rem;
        }

        .hero-title {
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 0.4rem;
        }

        .hero-text {
            font-size: 0.98rem;
            line-height: 1.5;
            color: #e5e7eb;
        }

        .section-card {
            background: #f8fafc;
            padding: 1rem;
            border-radius: 14px;
            margin-top: 1rem;
            border: 1px solid #e5e7eb;
        }

        .section-title {
            font-size: 1.05rem;
            font-weight: 700;
            margin-bottom: 0.65rem;
            color: #111827;
        }

        .helper-text {
            font-size: 0.9rem;
            color: #6b7280;
            margin-top: 0.35rem;
        }

        .stButton > button {
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            color: white;
            font-weight: 600;
            border-radius: 10px;
            height: 3rem;
            border: none;
        }

        .stButton > button:hover {
            background: linear-gradient(135deg, #1d4ed8, #1e40af);
            color: white;
        }

        @media (max-width: 768px) {
            .hero-title {
                font-size: 1.4rem;
            }

            .hero-text {
                font-size: 0.92rem;
            }

            .section-title {
                font-size: 1rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_list(items):
    for item in items:
        st.markdown(f"- {item}")


def main():
    inject_css()

    st.markdown(
        """
        <div class="hero-box">
            <div class="hero-title">📺 YouTube Video Summarizer</div>
            <div class="hero-text">
                Paste a YouTube video link and get an English summary with a transcript preview,
                TLDR, bullet points, and key takeaways.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Enter Video URL")

    if "example_url" not in st.session_state:
        st.session_state["example_url"] = ""

    col1, col2 = st.columns([5, 1])

    with col1:
        url = st.text_input(
            "YouTube URL",
            value=st.session_state["example_url"],
            placeholder="Paste YouTube video link here...",
            label_visibility="collapsed",
        )

    with col2:
        if st.button("Try Example"):
            st.session_state["example_url"] = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            st.rerun()

    st.caption("⚠️ Only works for videos with captions/subtitles enabled.")

    if st.button("🚀 Summarize Video", use_container_width=True):
        if not url or not url.strip():
            st.error("Please enter a valid YouTube URL.")
            return

        with st.spinner("Fetching transcript and generating summary..."):
            try:
                transcript = get_transcript(url)

                short_transcript = transcript[:4000]
                summary = summarize_text(short_transcript)

                st.success("Summary generated successfully.")

                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown(
                    '<div class="section-title">📄 Transcript Preview (English)</div>',
                    unsafe_allow_html=True,
                )
                st.write(summary["english_transcript_preview"])
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown(
                    '<div class="section-title">🎯 TLDR</div>',
                    unsafe_allow_html=True,
                )
                st.write(summary["tldr"])
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown(
                    '<div class="section-title">📝 Bullet Points</div>',
                    unsafe_allow_html=True,
                )
                render_list(summary["bullet_points"])
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown(
                    '<div class="section-title">✅ Key Takeaways</div>',
                    unsafe_allow_html=True,
                )
                render_list(summary["key_takeaways"])
                st.markdown("</div>", unsafe_allow_html=True)

                with st.expander("Show original transcript preview"):
                    st.write(transcript[:700])

            except Exception as e:
                error_text = str(e).lower()

                if "subtitles are disabled" in error_text or "transcripts are disabled" in error_text:
                    st.error(
                        "This video does not have captions/subtitles enabled, so a transcript cannot be fetched."
                    )
                elif "could not retrieve a transcript" in error_text or "no transcripts are available" in error_text:
                    st.error(
                        "No usable transcript was found for this video. Try another video."
                    )
                elif "429" in str(e) or "quota" in error_text or "rate limit" in error_text:
                    st.error(
                        "Free-tier API limit reached. Please try again later or test with a shorter video."
                    )
                else:
                    st.error(f"Error: {e}")

    st.markdown("---")
    st.markdown(
        """
        ### ⚙️ How it works

        1. Paste a YouTube video link  
        2. The app extracts the transcript if captions are available  
        3. AI translates and summarizes the content into English  
        4. You get a transcript preview, TLDR, bullet points, and key takeaways  
        """
    )


if __name__ == "__main__":
    main()