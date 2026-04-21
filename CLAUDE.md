# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project generates MP3 audio files from ham radio question pool JSON files for study purposes. It creates podcast-style audio where each question is read aloud along with its correct answer, organized by section (E0-E9, G0-G9, T0-T9).

## Commands

### Generate MP3s
```bash
pip install edge-tts  # Required dependency

# Generate all sections
python generate_mp3s.py <json_file> <output_dir>

# Generate specific sections only
python generate_mp3s.py <json_file> <output_dir> --sections E1,E2,E3

# Use a different voice
python generate_mp3s.py <json_file> <output_dir> --voice en-US-JennyNeural
```

### Serve as Podcast
```bash
./serve_podcast.sh [port]  # Default port 8000
```
This starts a local HTTP server and generates `podcast_live.xml` with the correct local IP address for subscribing from iOS podcast apps.

## Architecture

- **generate_mp3s.py**: Main script using Microsoft Edge TTS (`edge-tts` library). Groups questions by section prefix (E1, E2, etc.), generates one MP3 per section plus corresponding `_notes.txt` files with the text content.

- **podcast.xml**: RSS feed for GitHub Pages at `https://payne.github.io/extraQuestionsPodCast/podcast.xml`. Each episode links to the interactive study page.

- **serve_podcast.sh**: For local testing, generates `podcast_live.xml` with local IP address.

## JSON Input Format

The script expects a JSON array of question objects:
```json
{
  "id": "E1A01",
  "question": "Question text",
  "answers": ["A answer", "B answer", "C answer", "D answer"],
  "correct": 0,
  "correct_letter": "A",
  "refs": "Optional reference"
}
```

## Voice Options

Default voice is `en-US-GuyNeural`. Run `edge-tts --list-voices` to see all available voices.
