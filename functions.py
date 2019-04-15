import requests

def get_tba_data(url, retry=True):
    try:
        ans = requests.get("https://www.thebluealliance.com/api/v3/" + url,
                           "accept=application%2Fjson&X-TBA-Auth-Key=gl4GXuoqG8anLUrLo356LIeeQZk15cfSoXF72YT3mYkI38cCoAmReoCSSF4XWccQ").json()
        return ans
    except:
        print("oops " + url)
        return get_tba_data(url) if retry else None

def get_data(url, retry=True):
    try:
        ans = requests.get(url).json()
        return ans
    except:
        print("oops " + url)
        return get_data(url) if retry else None