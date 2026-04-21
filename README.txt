Ham Radio Extra Class 2024-2028 Audio Study Guide
==================================================

This folder contains MP3 audio files for studying the FCC Amateur Radio
Extra Class question pool (2024-2028).

FILES
-----
e_e0.mp3 - e_e9.mp3    : Audio files for each section
e_e0_notes.txt - ...   : Text files with questions and answers
podcast.xml            : RSS feed template for podcast apps
serve_podcast.sh       : Script to serve files to your iPhone

LOADING ON iPHONE VIA PODCAST APP
---------------------------------
1. Make sure your Mac and iPhone are on the same WiFi network

2. Run the server:
   ./serve_podcast.sh

3. The script will display a URL like:
   http://192.168.1.xxx:8000/podcast_live.xml

4. On your iPhone, open your podcast app and add a podcast by URL:
   - Apple Podcasts: Library > Edit > Add by URL
   - Overcast: + > Add URL
   - Pocket Casts: Search > "Add by URL" link at top

5. Paste the URL and subscribe

6. Download the episodes for offline listening

7. Press Ctrl+C on your Mac to stop the server when done

ALTERNATIVE: DIRECT FILE TRANSFER
---------------------------------
You can also transfer the MP3 files directly via:
- AirDrop
- iCloud Drive
- Finder (connect iPhone via USB, drag to Files app)
