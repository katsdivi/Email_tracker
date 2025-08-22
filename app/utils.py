import requests

def geo_lookup(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
        d = r.json()
        return d.get('city', ''), d.get('regionName', ''), d.get('country', '')
    except Exception:
        return '', '', ''
