from datetime import datetime, timedelta
from init_firebase import *
from fastapi import FastAPI, Response, Request
from starlette.requests import Request as StarletteRequest
from models import User
from firebase_admin import auth
from rest_firebase_api import (
    send_verify_email,
    sign_in_with_email_and_password,
    verify_email,
)

app = FastAPI()


@app.get("/")
async def index():
    return {"message": "Hello World"}


@app.post("/signup")
async def sign_up(user: User):
    email = user.email
    password = user.password
    user = auth.create_user(email=email, password=password)
    return user


@app.post("/signin")
async def sign_in(user: User, response: Response):
    email = user.email
    password = user.password
    user = sign_in_with_email_and_password(email, password)
    email_verified = auth.get_user_by_email(email).email_verified
    user["email_verified"] = email_verified
    if "idToken" in user:
        response.set_cookie(
            key="id_token",
            value=user["idToken"],
            expires=int((datetime.utcnow() + timedelta(hours=1)).timestamp()),
        )
    return user


@app.get("/send-email-verify")
async def send_email_verify(request: Request):
    id_token = request.cookies.get("id_token")
    if id_token:
        send_verify_email(id_token)
    else:
        return {"message": "please login first 😭"}
    return {"message": "send email verify 😎"}


@app.get("/verify-email")
async def verify_email_link(request: Request):
    oob_code = request.query_params.get("oobCode")
    print(oob_code)
    if oob_code:
        response = verify_email(oob_code).json()
        if "error" in response:
            return {"message": response["error"]["message"]}
    else:
        return {"message": "please click link at email 😭"}
    return {"message": "verify email 😎"}
