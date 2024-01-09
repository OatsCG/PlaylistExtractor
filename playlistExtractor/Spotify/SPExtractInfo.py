import sys
import json
from SPPlaylist import SPPlaylist

if __name__ == "__main__":
    #python3 SPExtractInfo.py '7IcCCwOjy2ZMINPPIGHcgf'

    sp = SPPlaylist(sys.argv[1])
    pinfo = sp.return_playlist_info_json()
    print(json.dumps(pinfo))