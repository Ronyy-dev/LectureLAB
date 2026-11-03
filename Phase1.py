from gemini_client import get_client
from config import MODEL

client = get_client()
interaction = client.interactions.create(
    model="gemini-3.5-flash-lite",
    input=[
        {"type": "video", "uri": "https://youtu.be/CvFHpVp8tu0?si=zkAaDqlJb9ECDf2p"},   # a public 10-20 min lecture link
        {"type": "text", "text": "Provide a 3-sentence summary of the lecture."},   # your prompt, asking for a 3-sentence summary
    ],
)
print(interaction.output_text)