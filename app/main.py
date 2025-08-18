from fastapi import FastAPI, Request, Depends
from fastapi.responses import StreamingResponse, RedirectResponse
from app.models import Event, SessionLocal
from app.auth import get_current_user
from datetime import datetime

app = FastAPI()

def save_event(data):
    db = SessionLocal()
    event = Event(**data)
    db.add(event)
    db.commit()
    db.close()

def get_device_type(user_agent: str):
    if "Mobile" in user_agent:
        return "Mobile"
    elif "Tablet" in user_agent:
        return "Tablet"
    return "Desktop"

@app.get("/track")
async def track_email(request: Request, email_uid: str):
    user_agent = request.headers.get('user-agent')
    client_ip = request.client.host
    device_type = get_device_type(user_agent)
    now = datetime.utcnow()
    event_data = {
        "event_type": "open", "email_uid": email_uid, "timestamp": now,
        "user_id": None,
        "client_ip": client_ip,
        "geo_city": "", "geo_region": "", "geo_country": "",
        "user_agent": user_agent, "device_type": device_type,
        "proxy_detected": False, "bot_detected": False,
        "target_url": "",
    }
    save_event(event_data)
    pixel = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF\x21\xF9\x04\x01\x00\x00\x00\x00\x2C\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x0C\x0A\x00\x3B'
    return StreamingResponse(iter([pixel]), media_type="image/gif")

@app.get("/click")
async def track_click(request: Request, email_uid: str, target: str):
    user_agent = request.headers.get('user-agent')
    client_ip = request.client.host
    device_type = get_device_type(user_agent)
    now = datetime.utcnow()
    event_data = {
        "event_type": "click", "email_uid": email_uid, "timestamp": now,
        "user_id": None,
        "client_ip": client_ip,
        "geo_city": "", "geo_region": "", "geo_country": "",
        "user_agent": user_agent, "device_type": device_type,
        "proxy_detected": False, "bot_detected": False,
        "target_url": target,
    }
    save_event(event_data)
    return RedirectResponse(target)

@app.get("/my_data")
async def my_data(user=Depends(get_current_user)):
    db = SessionLocal()
    events = db.query(Event).filter(Event.user_id == user['sub']).all()
    return [e.__dict__ for e in events]
