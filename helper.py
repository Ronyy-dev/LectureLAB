from gemini_client import get_client, extract_notes
from youtubeid import youtube_id

client = get_client()
log = []

raw_link = "https://youtu.be/CvFHpVp8tu0?si=zkAaDqlJb9ECDf2p"
video_id = youtube_id(raw_link)
clean_link = "https://www.youtube.com/watch?v=" + video_id

notes = extract_notes(client, clean_link, "Beginner", "English", log)

print(notes["title"])
print(notes["summary"])
print()

for chapter in notes["chapters"]:
    print(chapter["start"], chapter["heading"])
    for point in chapter["key_points"]:
        print("   -", point)

print()
for item in notes["key_terms"]:
    print(item["term"], ":", item["definition"])

print()
print(log)