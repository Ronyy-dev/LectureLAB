MODEL="gemini-3.5-flash-lite"
LANGUAGES=["English","Hindi","Hinglish"]
LEVELS=["Rookie","Intermediate","Advanced"]
NOTES_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "summary": {"type": "string"},
        "chapters": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "start": {"type": "string"},
                    "heading": {"type": "string"},
                    "key_points": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
                "required": ["start", "heading", "key_points"],
            },
        },
        "key_terms": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "term": {"type": "string"},
                    "definition": {"type": "string"},
                },
                "required": ["term", "definition"],
            },
        },
    },
    "required": ["title", "summary", "chapters", "key_terms"],

}

NOTES_PROMPT="""Watch this video and create study notes as if you are the class topper . 
Include what is shown and said in the video. Chapters in time order, with the real start time as MM:SS or HH:MM:SS.
Write 3 to 6 short key points for each chapter.List the key terms with a one-line definition for each, including any formulas or conversions.Write for a {level} audience in {language}.
Include only what is in the video. """