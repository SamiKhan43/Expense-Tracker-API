import jwt
from datetime import datetime,timedelta,timezone
from pwdlib import PasswordHash

SECRET_KEY = "your_secret_key" 
ALGORITHM = "HS256"

password_hash = PasswordHash.recommended()

def create_access_token(username:str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=5)
    data = {"sub":username,"exp":expire}
    token = jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return token