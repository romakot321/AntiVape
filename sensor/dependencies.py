from fastapi import Header, HTTPException
import os

TOKEN = os.getenv("SERVER_TOKEN", '1')


def validate_token(token: str = Header()):
    if token != TOKEN:
        raise HTTPException(403)
