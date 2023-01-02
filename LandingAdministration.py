import streamlit as st
import pandas as pd
import numpy as np
import openpyxl as xl
import matplotlib.pyplot as plt
from generate_sql_from_template import generate_sql
from sql_execution import execute_sql, get_execution_dates, generate_summ_report, generate_det_report
from database_connection import snowflake_acct_connect, snowflake_ws_connect
from config import get_ini_sections
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
import UserManagement as um
import sql_generator_streamlit as sql_generator
import snowflake_objects_queries_collection as snowflake_objects_drop

def LandingAdministration(username):
    with st.sidebar:
        selected=option_menu(
            menu_title=None ,
            options=["Admin", "create","Drop","Ad-Hoc","Report"],
            icons=[ 'person-workspace', 'hourglass-split','trash','file-earmark-bar-graph','graph-up-arrow']
        )
    if selected=="Admin":
        #st.title(f"you have selected {selected}")
        AdminSelection=option_menu(
            menu_title=None,
            options=["User Management", "Connection Management"],
            icons=['people-fill', 'cpu'], #icons from bootsrap
            default_index=0,
            orientation="horizontal"
             )

        if AdminSelection=="User Management":
            UserSelection = option_menu(
                menu_title=None,
                options=["Add User", "Modify User","Delete User", "Display User"],
                icons=['person-fill-add','person-fill-gear','person-fill-x', 'database-fill-add'],  # icons from bootsrap
                default_index=0,
                orientation="horizontal"
            )
            if UserSelection == "Add User":
                new_user = st.text_input("Username")
                new_name=st.text_input("Full Name")
                new_password = st.text_input("Password", type='password')
                new_hashed_password=um.hashed_password(new_password)
                new_role=st.selectbox("role",('Administrator','Normal'), key="ListofUserRole")
                if st.button("Submit", "Submit"):
                    um.create_usertable()
                    um.add_userdata(new_user, new_name, new_hashed_password, new_role)
                    st.success("You have sucessfully created a user")
            if UserSelection == "Display User":
                    column_names=["User Name","Full Name", "Password", "Role"]
                    user_data=um.view_all_users()
                    data_frame=pd.DataFrame(user_data, columns=column_names)
                    st.dataframe(data_frame)

        if AdminSelection=="Connection Management":
            ConSelection = option_menu(
            menu_title=None,
            options=["Add Connection", "Modify Connection", "Delete Connection", "Display Connection"],
            icons=['database-fill-add', 'database-fill-add', 'database-fill-add', 'database-fill-add'],  # icons from bootsrap
            default_index=0,
            orientation="horizontal"
        )
            if ConSelection =="Add Connection":
                new_account = st.text_input("Account")
                new_user=st.text_input("User")
                new_password = st.text_input("Password", type='password')
                new_role = st.selectbox("Role", ('ORGADMIN', 'ACCOUNTADMIN','SECURITYADMIN','USERADMIN','SYSADMIN','PUBLIC'), key="ListofDBRole")
                if st.button("Submit", "Add Connection"):
                    um.create_contable()
                    um.add_condata(new_account, new_user, new_password, new_role)
                    st.success("You have sucessfully created a new connection")

            # if ConSelection =="Modify Connection":
            # if ConSelection =="Delete Connection":
            if ConSelection =="Display Connection":
                column_names = ["Account", "User Name","Password", "Role"]
                con_data = um.display_condata()
                data_frame = pd.DataFrame(con_data, columns=column_names)
                st.dataframe(data_frame)
    if selected=="create":
        sql_generator.sql_generator_streamlit(username)
    if selected=="Drop":
        snowflake_objects_drop.DropSnowflakeObjects(username)
    if selected=='Ad-Hoc':
        sql_generator.adhoc(username)
    if selected=="Report":
        sql_generator.report()

