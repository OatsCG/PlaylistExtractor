import sys
import json
import urllib.parse
from SPPlaylist import SPPlaylist

if __name__ == "__main__":
    #python3 SPExtractTracks.py '7IcCCwOjy2ZMINPPIGHcgf'

    amp = SPPlaylist(sys.argv[1])
    amp.fetch_next()
    print(json.dumps(amp.return_playlist_json()))