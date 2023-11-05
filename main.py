import uvicorn
import firebase_admin
import pyrebase
import json
 
from firebase_admin import credentials, auth, firestore
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException


cred = credentials.Certificate('eeee_service_account_keys.json')
firebase = firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(json.load(open('firebase_config.json')))
app = FastAPI()
allow_all = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_all,
    allow_credentials=True,
    allow_methods=allow_all,
    allow_headers=allow_all
)

db = firestore.client()

# signup endpoint
@app.post("/signup", include_in_schema=False)
async def signup(request: Request):
    req = await request.json()
    email = req['email']
    password = req['password']
    username = req['username']
    displayName = req['full_name']
    if email is None or password is None:
        return HTTPException(detail={'message': 'Error! Missing Email or Password'}, status_code=400)
    try:
        user = auth.create_user(
            email=email,
            password=password,
            uid=username
        )
        user_ref = db.collection("testapi").document(user.uid)
        import datetime
        user_ref.set({
            "username":username,
            "email":email,
            "full_name":displayName,
            "created_at":datetime.datetime.now()
        })
        return JSONResponse(content={'message': f'Successfully created user {user.uid}'}, status_code=200)      
    except Exception as e:
        print(e)
        return HTTPException(detail={'message': 'Error Creating User'}, status_code=400)
 
# login endpoint
@app.post("/login", include_in_schema=False)
async def login(request: Request):
    req_json = await request.json()
    email = req_json['email']
    password = req_json['password']
    try:
        user = pb.auth().sign_in_with_email_and_password(email, password)
        jwt = user['idToken']
        return JSONResponse(content={'token': jwt}, status_code=200)
    except Exception as e:
        print(e)
        return HTTPException(detail={'message': 'There was an error logging in'}, status_code=400)
 
#update full_name endpoint
@app.put("/update", include_in_schema=False)
async def update_username(request: Request):
    req = await request.json()
    token = req['token']  # Make sure the token is passed in the request
    update_name = req.get('full_name')
    email = req.get("email")
    data = {}
    # Validate the token using Firebase Admin SDK
    if not update_name and not email:
        return HTTPException(detail = {"message":"please provide one param to update data"}, status_code=400)
    if update_name:
        data["full_name"] = update_name
    if email:
        data["email"] = email
    try:
        decoded_token = auth.verify_id_token(token)
    except Exception as e:
        print(e)
        return HTTPException(detail={'message': 'Invalid token'}, status_code=401)

    # Update the user's display name in Firebase Authentication
    try:
        user_uid = decoded_token['uid']
        if email:
            auth.update_user(user_uid, email=email)
        user_ref = db.collection("testapi").document(user_uid)
        user_ref.update(data)
        return JSONResponse(content={'message': 'Username updated successfully','update_name': update_name}, status_code=200)
    except Exception as e:
        print(e)
        return HTTPException(detail={'message': 'Error updating username'}, status_code=400)
    
#display endpoint 
@app.get("/display", include_in_schema=False)
async def display_user_data(request: Request):
    token = request.headers.get('token')
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        user_ref = db.collection("testapi").document(uid).get().to_dict()
        import json
        print(user_ref)
        user_ref["created_at"] = str(user_ref["created_at"])
        return JSONResponse(content=user_ref, status_code=200)
    except Exception as e:
        print(e)
        return HTTPException(detail={'message': 'Unable to fetch user data'}, status_code=500)


#delete endpoint
@app.delete("/delete", include_in_schema=False)
async def delete_user(request: Request):
    req = await request.json()
    email = req['email']
    password = req['password']
    try:
        user = pb.auth().sign_in_with_email_and_password(email, password)
        user_info = pb.auth().get_account_info(user['idToken'])
        uid = user_info['users'][0]['localId']
        auth.delete_user(uid)
        user_ref = db.collection("testapi").document(uid)
        user_ref.delete()
        return JSONResponse(content={'message': 'User deleted successfully'}, status_code=200)
    except Exception as e:
        print(e)
        return HTTPException(detail={'message': 'Error deleting user'}, status_code=400)

 
if __name__ == "__main__":
     uvicorn.run("main:app")