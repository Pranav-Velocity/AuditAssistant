
import firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import db


cred = credentials.Certificate("globalconnect-3bb5e-firebase-adminsdk-c2nua-8e11a0ebab.json")
firebase_admin.initialize_app(cred)
# email = input("ENTER EMAIL ID:")
# stall = input("ENTER STALL ID:")
# user = auth.get_user_by_email(email)

# print(user.email)
# print(stall)
# stall = stall + "/"
ref = db.reference('https://globalconnect-3bb5e-default-rtdb.firebaseio.com/stall_med_1/User7l81At18JoZs6inSylAC2l9fxt33')
print(ref.get())

firebaseConfig = {
    apiKey: "AIzaSyD-Utp-7ptobynFx7Uo1d_MyfifXLo5sDc",
    authDomain: "globalconnect-3bb5e.firebaseapp.com",
    databaseURL: "https://globalconnect-3bb5e-default-rtdb.firebaseio.com",
    projectId: "globalconnect-3bb5e",
    storageBucket: "globalconnect-3bb5e.appspot.com",
    messagingSenderId: "550879751617",
    appId: "1:550879751617:web:1b3b0ea97bc13ecb605340",
    measurementId: "G-12GT3VJSXM"
};