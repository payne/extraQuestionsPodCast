# Ham Radio Extra Class 2024-2028 Audio Study Guide

MP3 audio files for studying the FCC Amateur Radio Extra Class question pool (2024-2028).

## Files

- `e_e0.mp3` - `e_e9.mp3`: Audio files for each section
- `e_e0_notes.txt` - `e_e9_notes.txt`: Text files with questions and answers
- `podcast.xml`: RSS feed for podcast apps

## Subscribe via Podcast App

Add this URL to your podcast app:

```
https://payne.github.io/extraQuestionsPodCast/podcast.xml
```

**How to add:**
- **Apple Podcasts**: Library > Edit > Add a Podcast by URL
- **Overcast**: + > Add URL
- **Pocket Casts**: Search > "Add by URL" link at top

## Direct Download

Download MP3 files directly from:
https://payne.github.io/extraQuestionsPodCast/

## Interactive Study

For interactive question practice with the full question pool:
https://payne.github.io/ham_radio_question_pool/extra-2024-2028/extra-2024-2028.html

## Local Development

To regenerate MP3s from a question pool JSON:

```bash
pip install edge-tts
python generate_mp3s.py <json_file> <output_dir>
```

To serve locally for testing:

```bash
./serve_podcast.sh
```
