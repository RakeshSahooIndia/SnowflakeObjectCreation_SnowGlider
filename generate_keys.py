import pickle
from pathlib import Path
import streamlit_authenticator as stauth #pip install authenticator==0.1.5

names=["Snow Gliders", "Rakesh Sahoo"]
usernames=["snowgliders","rakesh"]
rolenames=["Administrator" , "Normal"]
passwords=['infy123', 'infy123']

hashed_passwords=stauth.Hasher(passwords).generate()
#print(hashed_passwords)
file_path =Path(__file__).parent/"hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords,file)
#file1=open('mypassword.txt',"w")
#file1.writelines(hashed_passwords)
#file1.close()
#print(file1.read())
# Taking user entered password
#userPassword = ['infy123']
#hashed_passwords=stauth.Hasher(userPassword).generate()
#print(hashed_passwords)






