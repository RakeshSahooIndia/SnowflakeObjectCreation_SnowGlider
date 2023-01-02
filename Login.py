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

#page configuration
#st.set_page_config(page_title="SnowSet",page_icon=":tada:", layout="wide")
#with open("snowset.css") as snowset:
#    st.markdown(f"<style>snowset_css.read()</style>", unsafe_allow_html=True)
#    st.markdown("<h1 style='text-align: center;'>Snowset App</h1>", unsafe_allow_html=True)
#    st.markdown("<h2 style='text-align: center;'>Snowflake Object Creation Application</h2>", unsafe_allow_html=True)
#Page Title
col1, col2,col3 =st.columns((1,4,1))
with col1:
    st.image('infosys.jpg', width=100)
with col2:
    st.markdown("<h2 style='text-align: center;background-color:#288499;padding-top: 0rem;padding-bottom:0rem;'>Snowset App</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center;background-color:coral;padding-top: 0rem;padding-bottom:0rem'>Snowflake Object Creation Application</h2>",unsafe_allow_html=True)
with col3:
    st.write("")

#---Connect to config db( snowflake DB here) for user authentication commneted on 31 Dec 2022---#
#--- Check if we can better do the below code instead of encoding/decoding.. At the moment the code below not required
# becoz it is getting done in usermanagement.py. but we should mobe hear and store the connection object to a variable
# so that each time we dont create a new connection object in usermanagement.py---#
#encode_sec='bnhsamJ6cy1xZzI2ODU4'.encode("ascii")
#snwflk_account=base64.b64decode(encode_sec).decode("ascii")
#snwflk_account=get_secrets(encode_sec, "account")
#snwflk_usr = get_secrets(encode_sec, "user")
#snwflk_pwd = get_secrets(encode_sec, "password")

@st.experimental_memo(ttl=600)
ctx = snowflake.connector.connect(
    user='snowgliders',
    password='Infy@123',
    account='nxljbzs-qg26858'
    )
c = ctx.cursor()

c.execute('USE DATABASE SNOWFLAKE_POC')
c.execute('USE SCHEMA PUBLIC')
c.execute('USE ROLE SYSADMIN')

#--- USer authentication From File commented on 2 Jan 2023---
#names=["Snow Gliders", "Rakesh Sahoo"]
#usernames=["snowgliders","rakesh"]
#rolenames=["Administrator","Normal"]
#file_path =Path(__file__).parent/"hashed_pw.pkl"
#with file_path.open("rb") as file:
#    hashed_passwords=pickle.load(file)
#authenticator=stauth.Authenticate(names,usernames,hashed_passwords,"Objectcreation","abcdef",cookie_expiry_days=30)



#with open('config.yml') as file:
#    config = yaml.load(file, Loader= yaml.SafeLoader)
#authenticator = stauth.Authenticate(
#    config['credentials'],
#    config['cookie']['name'],
#    config['cookie']['key'],
#    config['cookie']['expiry_days'],
#    config['preauthorized']
#)
#--- USer authentication From File commented on 2 Jan 2023---
#name,authentication_status, username =authenticator.login("Login Page", "main")
#print(name, authentication_status, username)
#if name != None:
#    user_role=rolenames[usernames.index(username)]
#print(user_role)

# --- USer authentication From database added on 22 Dec 2022---
c.execute('SELECT USERNAME,FULLNAME, PASSWORD, ROLENAME FROM userstable')
user_list=c.fetchall()
df_user = pd.DataFrame(user_list, columns=['USERNAME','FULLNAME','PASSWORD','ROLENAME'])
#data.columns=['USERNAME','FULLNAME','PASSWORD','ROLENAME']
#st.write(df_user)

#df_user=um.view_all_users()
#st.write(df_user)
#for x in data:
#    print(x)
usernames=df_user['USERNAME'].tolist()
#st.write(usernames)
names=df_user["FULLNAME"].tolist()
#st.write(names)
hashed_passwords=df_user["PASSWORD"].tolist()
#print(passwords)
authenticator= stauth.Authenticate(names ,usernames , hashed_passwords, "Objectcreation","abcdef",cookie_expiry_days=30)
name,authentication_status,username = authenticator.login("Login Page", "main")
#st.write(st.session_state["authentication_status"])
#st.write(st.session_state["name"])
#st.write(st.session_state["username"])


#---- SIDEBAR--

authenticator.logout("Logout","sidebar")
if name != None:
    st.sidebar.subheader(f"Welcome {name}")
    #st.sidebar.text(f"Role : {user_role}")
if authentication_status==False:
    st.error("username/password is incorrect")
if authentication_status==None:
    st.warning("Please enter your username and password")
#if authentication_status==True and user_role=="Administrator":
#    LandingAdmin.LandingAdministration(username)
#if authentication_status==True and  user_role == "Normal":
#    LandingNormalUser.LandingNormalUser(username)






