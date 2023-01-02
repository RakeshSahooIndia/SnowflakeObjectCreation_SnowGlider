import streamlit as st
import sql_generator_streamlit as sql_generator
from streamlit_option_menu import option_menu
import snowflake_objects_queries_collection as snowflake_objects_drop

def LandingNormalUser(username):
    with st.sidebar:
        selected=option_menu(
            menu_title=None ,
            options = ["create", "Drop", "Ad-Hoc", "Report"],
            icons = ['hourglass-split', 'trash', 'file-earmark-bar-graph', 'graph-up-arrow']
        )
    if selected=="create":
        sql_generator.sql_generator_streamlit(username)
    if selected == "Drop":
        snowflake_objects_drop.DropSnowflakeObjects(username)
    if selected == 'Ad-Hoc':
        sql_generator.adhoc(username)
    if selected=="Report":
        sql_generator.report()

