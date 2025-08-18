import requests
def geo_lookup(ip):
    r = requests.get(f"http://ip-api.com/json/{ip}")
    d = r.json()
    return d.get('city', ''), d.get('regionName', ''), d.get('country', '')
