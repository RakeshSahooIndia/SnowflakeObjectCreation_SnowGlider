import streamlit as st

# DB Management
import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data

def main():
    st.title("Snowflake Object Creation Application")
choice=st.sidebar.selectbox("Menu",["Signup", "Login"])
if(choice=="Login"):
    st.subheader("Login Section")
    username=st.sidebar.text_input("User Name")
    password=st.sidebar.text_input("Password",type='password')
    if st.sidebar.checkbox("Login"):
        #if password=='12345':
        create_usertable()
        result=login_user(username,password)
        if result:
            st.success("Logged in as {}".format(username))
            task=st.selectbox("Task", ["Admin Page","Snowflake Object creation Page"])
            if(task=="Admin Page"):
                st.subheader("Admin Page")
            if(task=="Snowflake Object creation Page"):
                st.subheader("Snowflake Object Creation Page")
        else:
            st.warning("Incorrect Username or password")

elif choice=="Signup":
    st.subheader("Create New Account")
    new_user=st.text_input("UserName")
    new_password=st.text_input("Password",type='password')

    if st.button("Signup"):
        create_usertable()
        add_userdata(new_user,new_password)
        st.success("You have sucessfully created a user")
        st.info("Go to Login Menu to Login")



if __name__=='__main__':
    main()