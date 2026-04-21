#!/bin/bash
#
# Serve the Ham Radio Extra Class podcast on your local network
# Your iPhone podcast app can subscribe to the feed URL shown below
#

cd "$(dirname "$0")"

# Get local IP address (works on macOS)
LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null)

if [ -z "$LOCAL_IP" ]; then
    echo "Could not detect local IP. Using localhost."
    LOCAL_IP="localhost"
fi

PORT=${1:-8000}

# Update podcast.xml with the correct IP
sed "s/HOST_PLACEHOLDER/$LOCAL_IP/g" podcast.xml > podcast_live.xml

echo "=============================================="
echo "  Ham Radio Extra Class Podcast Server"
echo "=============================================="
echo ""
echo "Add this feed URL to your iPhone podcast app:"
echo ""
echo "  http://$LOCAL_IP:$PORT/podcast_live.xml"
echo ""
echo "Make sure your iPhone is on the same WiFi network."
echo "Press Ctrl+C to stop the server."
echo "=============================================="
echo ""

# Start HTTP server
python3 -m http.server $PORT
