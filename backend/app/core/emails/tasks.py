from fastapi_mail import FastMail, ConnectionConfig
from pydantic import SecretStr
from pathlib import Path
from backend.app.core.config import settings