import streamlit as st
import snowflake.connector
import pandas as pd
from config import get_secrets
import base64
import streamlit_authenticator as stauth #pip install authenticator==0.1.5

# DB Management
# Connect to Snowflake DB for inserting data into metadata table
encode_sec='bnhsamJ6cy1xZzI2ODU4'.encode("ascii")
snwflk_account=base64.b64decode(encode_sec).decode("ascii")
#snwflk_account=get_secrets(encode_sec, "account")
snwflk_usr = get_secrets(encode_sec, "user")
snwflk_pwd = get_secrets(encode_sec, "password")

ctx = snowflake.connector.connect(
    user= snwflk_usr,
    password=snwflk_pwd,
    account=snwflk_account
    )
c = ctx.cursor()
c.execute('USE WAREHOUSE COMPUTE_WH')
c.execute('USE DATABASE SNOWFLAKE_POC')
c.execute('USE SCHEMA PUBLIC')
c.execute('USE ROLE SYSADMIN')



# DB  Functions for User Management
def hashed_password(password):
	hashed_passwords=stauth.Hasher(password).generate()
	#print(hashed_passwords)
	return hashed_password

def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, fullname TEXT, password TEXT,rolename TEXT)')

def add_userdata(username,fullname,password,rolename):
	str=f'INSERT INTO userstable(USERNAME,FULLNAME, PASSWORD,ROLENAME) VALUES (\'{username}\',\'{fullname}\',\'{password}\',\'{rolename}\')'
	c.execute(str)

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

def view_all_users():
	c.execute('SELECT USERNAME,FULLNAME, PASSWORD, ROLENAME FROM userstable')
	data = pd.DataFrame(c.fetchall())
	data.columns=['USERNAME','FULLNAME','PASSWORD','ROLENAME']
	print(data)
	return data

# DB  Functions for Connection Management
def create_contable():
	c.execute('CREATE TABLE IF NOT EXISTS connectiontable(account TEXT, username TEXT,password TEXT,rolename TEXT)')

def add_condata(account, username,password,rolename):
	str=f'INSERT INTO connectiontable(account,username, password,rolename) VALUES (\'{account}\',\'{username}\',\'{password}\',\'{rolename}\')'
	c.execute(str)
	#conn.commit()

def update_condata(account,username, password,rolename):
	c.execute(f'UPDATE connectiontable SET account= \'{account}\' , username =\'{username}\', password=\'{password}\' , rolename=\'{rolename}\'')

def delete_condata(username):
	c.execute(f'DELETE FROM connectiontable WHERE username =\'{username}\'')
	data = c.fetchall()
	return data

def display_condata():
	c.execute('SELECT ACCOUNT, USERNAME, PASSWORD, ROLENAME FROM connectiontable')
	data = c.fetchall()
	return data

view_all_users()