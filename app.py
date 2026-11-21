import streamlit as st

from config import LANGUAGES, LEVELS
from gemini_client import get_client, extract_notes
from youtubeid import youtube_id

# ---------- session state ----------
STATE_DEFAULTS = {
    "link": None,
    "notes": None,
    "cards": None,
    "card_pos": 0,
    "flipped": False,
    "quiz": None,
    "quiz_problems": [],
    "quiz_submitted": False,
    "log": [],
}


def init_state():
    for key, value in STATE_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value.copy() if isinstance(value, list) else value


def reset_state():
    for key, value in STATE_DEFAULTS.items():
        st.session_state[key] = value.copy() if isinstance(value, list) else value
    st.rerun()


# ---------- first screen: paste a link ----------
def show_input_screen(client, level, language):
    st.title("LectureLab 🎓")
    url = st.text_input("YouTube link")

    if st.button("Build Study Kit"):
        if client is None:
            st.error("API key missing. Add GEMINI_API_KEY to your .env file.")
            st.stop()

        video_id = youtube_id(url)
        if video_id is None:
            st.error("That doesn't look like a YouTube video link.")
            st.stop()

        st.session_state.link = "https://www.youtube.com/watch?v=" + video_id

        try:
            with st.spinner("Watching the lecture..."):
                st.session_state.notes = extract_notes(
                    client, st.session_state.link, level, language, st.session_state.log
                )
        except Exception as error:
            st.session_state.link = None
            st.error("Something went wrong: " + str(error))
            st.stop()



# ---------- main code ----------
st.set_page_config(page_title="LectureLab", page_icon="🎓", layout="wide")

init_state()
client = get_client()

with st.sidebar:
    language = st.selectbox("Language", LANGUAGES)
    level = st.selectbox("Level", LEVELS)
    flashcard_count = st.slider("Number of flashcards", 5, 20, 10)
    quiz_count = st.slider("Number of quiz questions", 3, 15, 5)
    if st.button("New video"):
        reset_state()

if st.session_state.notes is None:
    show_input_screen(client, level, language)
else:
    left, right = st.columns(2)
    with left:
        st.video(st.session_state.link)
    with right:
        st.header(st.session_state.notes["title"])
        st.write(st.session_state.notes["summary"])

    tab_cards, tab_quiz, tab_usage = st.tabs(["Flashcards", "Quiz", "Usage"])
    with tab_cards:
        st.info("Flashcards come in Phase 4.")
    with tab_quiz:
        st.info("Quiz comes in Phase 5.")
    with tab_usage:
        st.info("Usage comes in Phase 7.")