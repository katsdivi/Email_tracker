from fastapi import Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
import google.oauth2.id_token
import google.auth.transport.requests

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.google.com/o/oauth2/v2/auth",
    tokenUrl="https://www.googleapis.com/oauth2/v4/token"
)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        idinfo = google.oauth2.id_token.verify_oauth2_token(token, google.auth.transport.requests.Request())
        return idinfo
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid credentials")
