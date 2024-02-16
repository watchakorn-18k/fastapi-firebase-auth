from settings import FIREBASE_WEB_API_KEY
import requests
import json

SIGN_IN_WITH_PASSWORD_URL = (
    "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
)

SEND_VERIFY_EMAIL_URL = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"

VERIFY_EMAIL_URL = (
    "https://www.googleapis.com/identitytoolkit/v3/relyingparty/setAccountInfo"
)


def sign_in_with_email_and_password(
    email: str, password: str, return_secure_token: bool = True
):
    payload = json.dumps(
        {"email": email, "password": password, "returnSecureToken": return_secure_token}
    )
    r = requests.post(
        SIGN_IN_WITH_PASSWORD_URL, params={"key": FIREBASE_WEB_API_KEY}, data=payload
    )

    return r.json()


def send_verify_email(id_token):
    headers = {"Content-Type": "application/json"}
    url = f"{SEND_VERIFY_EMAIL_URL}?key={FIREBASE_WEB_API_KEY}"
    data = {"requestType": "VERIFY_EMAIL", "idToken": id_token}
    response = requests.post(
        url, headers=headers, json=data, auth=("api_key", FIREBASE_WEB_API_KEY)
    )
    return response


def verify_email(oob_code):
    body = {"oobCode": oob_code}
    params = {"key": FIREBASE_WEB_API_KEY}
    response = requests.request("post", VERIFY_EMAIL_URL, params=params, json=body)
    return response
