from firebase_admin import credentials, initialize_app

cred = credentials.Certificate("service-account.json")
initialize_app(cred)
print("firebase init done")
