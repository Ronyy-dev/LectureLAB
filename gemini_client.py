import os
from dotenv import load_dotenv
from google import genai
import time
import json
from config import LEVELS
from config import LANGUAGES
from config import MODEL, NOTES_PROMPT, NOTES_SCHEMA

def get_client():
    load_dotenv()
    key = os.getenv("GEMINI_API_KEY")
    if key is None or key == "":
        return None
    return genai.Client(api_key=key)

                         
def video_part(youtube_link):
    return {"type": "video", "uri": youtube_link}

def call_gemini(client, contents, log, step, schema=None):
    start = time.time()

    if schema is not None:
        interaction = client.interactions.create(
            model=MODEL,
            input=contents,
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": schema,
            },
        )
    else:
        interaction = client.interactions.create(
            model=MODEL,
            input=contents,
        )

    seconds = round(time.time() - start, 2)

    log.append({
        "step": step,
        "seconds": seconds,
        "input_tokens": interaction.usage.total_input_tokens,
        "output_tokens": interaction.usage.total_output_tokens,
    })

    if schema is not None:
        return json.loads(interaction.output_text)
    return interaction.output_text

def extract_notes(client, youtube_id, level, language, log):
    prompt= NOTES_PROMPT.format(level=level, language= language )
    input_list = [
        video_part(youtube_id),
        {"type": "text", "text": prompt},
    ]
    print(input_list)
    return call_gemini(client, input_list, log, "notes", NOTES_SCHEMA)    