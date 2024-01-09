import sys
import json
from AMPlaylist import AMPlaylist

if __name__ == "__main__":
    #python3 AMExtractInfo.py 'pl.f54198ad42404535be13eabf3835fb22'

    amp = AMPlaylist(sys.argv[1])
    pinfo = amp.return_playlist_info_json()
    print(json.dumps(pinfo))