from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import secrets

load_dotenv()

class Settings(BaseSettings):
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str

settings = Settings()

app = FastAPI()
security = HTTPBasic()


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    is_correct_username = secrets.compare_digest(credentials.username, settings.ADMIN_USERNAME)
    is_correct_password = secrets.compare_digest(credentials.password, settings.ADMIN_PASSWORD)

    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/")
def public_root():
    return {"message": "Public endpoint accessible to everyone."}

@app.get("/admin")
def admin_only(username: str = Depends(authenticate)):
    return {"message": f"Hello, admin {username}! This endpoint is secure."}

@app.get("/info")
def app_info():
    return {"app": "Example FastAPI app", "version": "1.0"}
