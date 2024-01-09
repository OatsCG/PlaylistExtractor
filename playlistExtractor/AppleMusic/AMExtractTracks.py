import sys
import json
import urllib.parse
from AMPlaylist import AMPlaylist

if __name__ == "__main__":
    #python3 AMExtractTracks.py 'pl.f54198ad42404535be13eabf3835fb22'
    amp = AMPlaylist(sys.argv[1])
    amp.fetch_next()
    print(json.dumps(amp.return_playlist_json()))