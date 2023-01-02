import pickle
from pathlib import Path
import yaml
import pandas as pd
import snowflake.connector
import UserManagement as um
from streamlit_option_menu import option_menu
import streamlit as st
import streamlit_authenticator as stauth # pip install streamlit-authenticator==0.1.5
import LandingAdministration as LandingAdmin
import LandingNormalUser as LandingNormalUser
import base64
from config import get_secrets

def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
local_css("snowset.css")

#Page Title
col1, col2,col3 =st.columns((1,4,1))
with col1:
    st.image('infosys.jpg', width=100)
with col2:
    st.markdown("<h2 style='text-align: center;background-color:#288499;padding-top: 0rem;padding-bottom:0rem;'>Snowset App</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center;background-color:coral;padding-top: 0rem;padding-bottom:0rem'>Snowflake Object Creation Application</h2>",unsafe_allow_html=True)
with col3:
    st.write("")

#--- USer authentication From File ---
names=["Snow Gliders", "Rakesh Sahoo"]
usernames=["snowgliders","rakesh"]
rolenames=["Administrator","Normal"]
file_path =Path(__file__).parent/"hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords=pickle.load(file)
authenticator=stauth.Authenticate(names,usernames,hashed_passwords,"Objectcreation","abcdef",cookie_expiry_days=30)

name,authentication_status, username =authenticator.login("Login Page", "main")

if name != None:
    user_role=rolenames[usernames.index(username)]

#---- SIDEBAR--

if name != None:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.subheader(f"Welcome {name}")
    st.sidebar.text(f"Role : {user_role}")
if authentication_status==False:
    st.error("username/password is incorrect")
if authentication_status==None:
    st.warning("Please enter your username and apssword")
if authentication_status==True and user_role=="Administrator":
    LandingAdmin.LandingAdministration(username)
if authentication_status==True and  user_role == "Normal":
    LandingNormalUser.LandingNormalUser(username)






