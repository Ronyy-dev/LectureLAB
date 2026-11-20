import streamlit as st
from google import genai
from dotenv import load_dotenv
import time
load_dotenv()
client = genai.Client()
import time

st.set_page_config(page_title="LectureLab", page_icon="🎓",
layout="wide")

st.title("LectureLab")
