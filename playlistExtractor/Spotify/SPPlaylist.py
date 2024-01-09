import requests

class SPPlaylist:
    name = ""
    description = ""
    artwork = ""
    tracks = []
    spID = ""
    diderror = False
    nextURL = None
    spHeaders = {}

    def __init__(self, spID):
        '''
        spID: the string ID of the Spotify playlist.
        SPPlaylist begins fetching songs when the class is initialized.
        '''
        self.spID = spID
        self.getBearerToken()
        self.fetch_initial_info()

    def getBearerToken(self):
        '''
        Fetch an up-to-date public Bearer accessToken from spotify.
        '''
        url = "https://spotify.com"
        r = requests.get(url=url)
        rtext = r.text
        atexpsplit = rtext.split("accessTokenExpirationTimestampMs")[0]
        atsplit = atexpsplit.split("accessToken")[-1]
        accessToken = atsplit[3:-3]
        self.spHeaders = {
            'Authorization': f'Bearer {accessToken}'
        }

    def fetch_initial_info(self):
        '''
        Fetches the metadata of the playlist, and fetches the
        first batch.
        '''
        baseurl = f'https://api.spotify.com/v1/playlists/{self.spID}'
        rmeta = requests.get(baseurl, headers=self.spHeaders).json()
        #print(rmeta)
        if ("error" in rmeta):
            self.diderror = True
            return
        self.name = rmeta["name"]
        self.description = rmeta["description"]
        try:
            self.artwork = rmeta["images"][0]["url"]
        except:
            self.artwork = ""
        rtracks = rmeta["tracks"]
        self.extract_songs(rtracks)
        if "next" in rtracks:
            self.nextURL = rtracks["next"]
    
    def fetch_next(self):
        '''
        ampExt: str
        Recursively fetches the batch specified in ampExt.
        '''
        if (self.nextURL == None):
            return
        rtracks = requests.get(self.nextURL, headers=self.spHeaders).json()
        self.extract_songs(rtracks)
        if "next" in rtracks:
            self.nextURL = rtracks["next"]
            self.fetch_next()
    
    def extract_songs(self, tracks: dict[str: any]):
        rsongs: list[dict] = tracks["items"]
        for song in rsongs:
            if song["track"]["type"] == "track":
                trackdata = {
                    'title': song["track"]["name"],
                    'album': song["track"]["album"]["name"],
                    'artists': ', '.join([artist['name'] for artist in song['track']['artists']])
                }
                self.tracks.append(trackdata)
            else:
                print("NOT A SONG NOT A SONG")
                print(song)
                quit()
    
    def return_playlist_json(self):
        '''
        returns the playlist in the following json format:

        {
            name: str
            description: str
            artwork: str
            playlistID: str
            tracks: [
                {
                    title: str
                    album: str
                    artists: str
                }
                ...
            ]
        }
        '''
        playlistjson = {
            'name': self.name,
            'description': self.description,
            'artwork': self.artwork,
            'playlistID': self.spID,
            'tracks': self.tracks
        }
        return playlistjson
    
    def return_playlist_info_json(self):
        '''
        returns the playlist info in the following json format:

        {
            name: str
            description: str
            artwork: str
            playlistID: str
        }
        OR
        {
            error: True
        }
        '''
        if (self.diderror):
            errorjson = {
                'error': True
            }
            return errorjson
        else:
            playlistjson = {
                'name': self.name,
                'description': self.description,
                'artwork': self.artwork,
                'playlistID': self.spID
            }
            return playlistjson


if __name__ == "__main__":
    sp = SPPlaylist("7IcCCwOjy2ZMINPPIGHcgf")

    print(sp.name)
    print(sp.description)