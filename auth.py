import jwt
from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from dotenv import load_dotenv


load_dotenv()

# Secret key used to sign and verify JWTs
SECRET_KEY = os.getenv("SECRET_KEY")

# Algorithm used for signing the token
ALGORITHM = "HS256"

password_hash = PasswordHash.recommended()


def create_access_token(username: str):
    # Token will expire after 30 minutes
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    # Store the username and expiry time inside the token
    data = {
        "id": username,
        "exp": expire
    }

    # Sign the token using our secret key
    token = jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# Reads the Bearer token from the Authorization header
bearer_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    token = credentials.credentials

    try:
        # Decode and verify the JWT
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # Get the username stored in the token
        username = payload.get("id")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="invalid token"
            )

        return username

    # Token exists but its expiry time has passed
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="token has expired"
        )

    # Token is invalid or its signature doesn't match
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token signature"
        )
