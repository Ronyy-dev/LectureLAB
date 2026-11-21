import os
from certifi import contents
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

       request = {"model": MODEL, "input": contents}
       if schema is not None:
        request["response_format"] = {
            "type": "text",
            "mime_type": "application/json",
            "schema": schema,
        }

       for attempt in range(1, MAX_TRIES + 1):
        try:
            interaction = client.interactions.create(**request)
            break
        except Exception as error:
            text = str(error).lower()
            is_busy = any(word in text for word in ["503", "unavailable", "high demand"])
            if is_busy and attempt < MAX_TRIES:
                time.sleep(2 * attempt)
            else:
                raise

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