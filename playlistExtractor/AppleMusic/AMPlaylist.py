import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
import re


class AMPlaylist:

    name = ""
    description = ""
    artwork = ""
    tracks = []
    ampID = ""
    diderror = False
    nextID = None
    ampHeaders = {
        'origin': 'https://music.apple.com',
        'authorization': 'Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldlYlBsYXlLaWQifQ.eyJpc3MiOiJBTVBXZWJQbGF5IiwiaWF0IjoxNjk1NDAwMTMyLCJleHAiOjE3MDI2NTc3MzIsInJvb3RfaHR0cHNfb3JpZ2luIjpbImFwcGxlLmNvbSJdfQ.mVrcofZI2Yl_6W5kJzXBjg06fon3sQB3rnttBpNzWoM7AUOfc6-rhbo-ARmL1FHVLcsVqyYlyUL6RU61xuhyuA'
    }
    def __init__(self, ampID):
        '''
        ampID: the string ID of the Apple Music playlist.
        AMPlaylist begins fetching songs when the class is initialized.
        '''
        url = "https://music.apple.com/us/playlist/todays-hits/pl.f4d106fed2bd41149aaacabb233eb5eb"
        response = requests.get(url)
        asseturlmatch = re.search("index-.{8}\.js", response.text)[0]
        assetURL = "https://music.apple.com/assets/" + asseturlmatch
        jsres = requests.get(assetURL)
        bearervarmatch = re.search("Bearer \$\{.{1,5}\}", jsres.text)[0]
        varmatch = re.search("\{.{1,5}\}", bearervarmatch)[0][1:-1]
        tokenmatch = jsres.text.split(" " + varmatch + "=")[1].split(",")[0][1:-1]
        self.ampHeaders = {
            'origin': 'https://music.apple.com',
            'authorization': "Bearer " + tokenmatch
        }
        self.ampID = ampID
        self.fetch_initial_info()

    def fetch_initial_info(self):
        '''
        Fetches the metadata of the playlist, and fetches the
        first batch.
        '''
        baseurl = 'https://amp-api.music.apple.com/v1/catalog/ca/playlists/' + self.ampID
        rmeta = requests.get(baseurl, headers=self.ampHeaders).json()
        if ("errors" in rmeta):
            self.diderror = True
            return
        self.name = rmeta["data"][0]["attributes"]["name"]
        self.description = rmeta["data"][0]["attributes"]["description"]["standard"]
        try:
            self.artwork = rmeta["data"][0]["attributes"]["artwork"]["url"].replace("{w}", "1080").replace("{h}", "1080")
        except:
            self.artwork = ""
        rtracks = requests.get(baseurl + '/tracks', headers=self.ampHeaders).json()
        self.extract_songs(rtracks)
        if "next" in rtracks:
            self.nextID = rtracks["next"]

    def fetch_next(self):
        '''
        ampExt: str
        Fetches the batch specified in ampExt.
        '''
        if (self.nextID == None):
            return
        rtracks = requests.get("https://amp-api.music.apple.com" + self.nextID, headers=self.ampHeaders).json()
        self.extract_songs(rtracks)
        if "next" in rtracks:
            self.nextID = rtracks["next"]
            self.fetch_next()

    def extract_songs(self, ampJson):
        '''
        ampJson: dict
        Extracts song info from the playlist, and appends
        it to self.tracks.
        '''
        rsongs = ampJson["data"]
        for song in rsongs:
            if song["type"] == "songs":
                trackdata = {
                    'title': song["attributes"]["name"],
                    'album': song["attributes"]["albumName"],
                    'artists': song["attributes"]["artistName"]
                }
                self.tracks.append(trackdata)
            elif song["type"] == "music-videos":
                trackdata = {
                    'title': song["attributes"]["name"],
                    'album': "",
                    'artists': song["attributes"]["artistName"]
                }
                self.tracks.append(trackdata)
            
        self.relay_status()
    
    def relay_status(self):
        '''
        Prints how many songs were fetched so far.
        This is called after every batch.
        '''
        return
        print(len(self.tracks), "songs so far")
    
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
            'playlistID': self.ampID,
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
                'playlistID': self.ampID
            }
            return playlistjson


if __name__ == "__main__":
    amp = AMPlaylist('pl.f54198ad42404535be13eabf3835fb22')

    print(amp.name)
    print(amp.description)
