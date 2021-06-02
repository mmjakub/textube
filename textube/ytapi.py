import base64
import html
from http.client import HTTPSConnection
import json
import threading
import urllib.parse


class ConnectionManager():
    _thread_local = threading.local()
    _thread_local.gapis = HTTPSConnection('www.googleapis.com')
    _thread_local.yt = HTTPSConnection('www.youtube-nocookie.com')

    @classmethod
    def threadInit(cls):
        cls._thread_local.gapis = HTTPSConnection('www.googleapis.com')
        cls._thread_local.yt = HTTPSConnection('www.youtube-nocookie.com')

    @classmethod
    def closeAll(cls):
        cls._thread_local.gapis.close()
        cls._thread_local.yt.close()

    @classmethod
    def yt(cls):
        return cls._thread_local.yt

    @classmethod
    def gapis(cls):
        return cls._thread_local.gapis

def yt_api_get(endpoint, **params):
    params.update(key='AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM')
    gapis = ConnectionManager.gapis()
    gapis.request('GET', f'/youtube/v3/{endpoint}?{"&".join(f"{k}={v}" for k,v in params.items())}', headers={
        'X-Origin': 'https://explorer.apis.google.com',
        'X-Referer': 'https://explorer.apis.google.com'})
    return json.loads(gapis.getresponse().read())

def itube_api(endpoint, **kwargs):
    data = {'context': {'client': {'clientName': 'WEB', 'clientVersion': '2.00000101'}}}
    data.update(kwargs)
    yt = ConnectionManager.yt()
    yt.request('POST',
        f'https://www.youtube-nocookie.com/youtubei/v1/{endpoint}?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
        body=json.dumps(data))
    return json.loads(yt.getresponse().read())

def yt_get(url):
    yt = ConnectionManager.yt()
    yt.request('GET', url)
    body = str(yt.getresponse().read())
    return html.unescape(html.unescape(body))

def channel2uploads(id):
    return 'UU' + id[2:] if id.startswith('UC') else id
    
def flatten_cue(cue):
    cue = cue['transcriptCueGroupRenderer']
    return cue['formattedStartOffset']['simpleText'],\
        cue['cues'][0]['transcriptCueRenderer']['cue']['simpleText']

def fetch_videoIds(playlistId):
    return list(fetch_items(playlistId, selector=lambda e: e['videoId']))

def fetch_items(playlistId, part='contentDetails', selector=lambda e: e, token=None):
    params = {} if token is None else {'pageToken': token}
    data = yt_api_get('playlistItems', part=part, maxResults=50,
        playlistId=playlistId, **params)
    yield from (selector(e[part]) for e in data['items'])
    if (token := data.get('nextPageToken')) is not None:
        yield from fetch_items(playlistId, part, selector, token)

def get_transcript(videoId):
    params = urllib.parse.quote(base64.b64encode(bytes([10,11]) + videoId.encode()))
    r_json = itube_api('get_transcript', params=params)
    try:
        cues = r_json['actions'][0]['updateEngagementPanelAction']['content']\
            ['transcriptRenderer']['body']['transcriptBodyRenderer']['cueGroups']
    except (KeyError):
        return []
    return list(map(flatten_cue, cues))

def get_captions_from_config(videoId, fmt=None):
    params = {} if fmt is None else {'fmt': fmt}
    config = itube_api('player', videoId=videoId)
    try:
        return yt_get(config['captions']['playerCaptionsTracklistRenderer']['captionTracks'][0]['baseUrl'])
    except KeyError:
        return None
