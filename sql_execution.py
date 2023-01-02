import pandas as pd
from snowflake.connector import ProgrammingError
import streamlit as st

def execute_sql(sql_list,acct_nm,user_nm, con1, con2):
    length = len(sql_list)
    df_status_report = pd.DataFrame()
    qry_list = []
    status_list = []
    error_list = []
    cur = con1.cursor()
    sql_cnt = 0
    success_cnt = 0
    fail_cnt = 0
    if length > 0:
        for sql in sql_list:
            try:
                sql_cnt += 1
                qry_list.append(sql)
                cur.execute(sql)
                query_id = cur.sfqid
                con1.get_query_status_throw_if_error(query_id)
                status_list.append("success")
                error_list.append("")
                success_cnt += 1
            except ProgrammingError as e:
                status_list.append("fail")
                error_list.append(e.msg)
                fail_cnt += 1
                continue
            except Exception as e:
                cur.close()

        df_status_report["SQL"] = qry_list
        df_status_report["STATUS"] = status_list
        df_status_report["ERROR"] = error_list
        save_execution_logs(df_status_report, sql_cnt, success_cnt, fail_cnt,acct_nm,user_nm, con2)
        if cur is not None:
            cur.close()


def save_execution_logs(df, sql_cnt, success_cnt, fail_cnt,acct_nm,user_nm, con):
    exec_id = 0
    cur1 = con.cursor()
    sql = "insert into SNOWFLAKE_POC.PUBLIC.EXECUTION_SUMMARY (SQL_CNT,SUCCESS_CNT,FAIL_CNT,ACCT_NAME,USER_NAME) VALUES ('" + str(
        int(sql_cnt)) + "','" + str(int(success_cnt)) + "','" + str(int(fail_cnt)) + "','" + str(acct_nm) + "','" + str(user_nm) + "')"
    cur1.execute(sql)
    cur1.execute('select max(EXEC_ID) from SNOWFLAKE_POC.PUBLIC.EXECUTION_SUMMARY')
    for record in cur1:
        exec_id = record[0]

    for index, row in df.iterrows():
        sql = "insert into SNOWFLAKE_POC.PUBLIC.EXECUTION_DETAIL (EXEC_ID,EXEC_SQL,EXEC_STATUS,ERROR_MSG,ACCT_NAME,USER_NAME) VALUES (" + str(
            exec_id) + ",'" + str(row['SQL']).replace("'", "") + "','" + str(row['STATUS']) + "','" + str(
            row['ERROR']).replace("'", "") + "','" + str(acct_nm) + "','" + str(user_nm) + "')"
        cur1.execute(sql)

    if cur1 is not None:
        cur1.close()


def generate_det_report(exec_id, con):
    cur = con.cursor()
    df = pd.DataFrame()
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    list5 = []
    list6 = []
    sql = "select left(convert_timezone('Asia/Kolkata', exec_dttm),24),ACCT_NAME,USER_NAME,EXEC_SQL,EXEC_STATUS,ERROR_MSG FROM SNOWFLAKE_POC.PUBLIC.EXECUTION_DETAIL WHERE EXEC_ID=" + str(
        int(exec_id))
    cur.execute(sql)
    for record in cur:
        list1.append(record[0])
        list2.append(record[1])
        list3.append(record[2])
        list4.append(record[3])
        list5.append(record[4])
        list6.append(record[5])

    if cur is not None:
        cur.close()

    df["Date"] = list1
    df["Account"] = list2
    df["User"] = list3
    df["SQL Command"] = list4
    df["Status"] = list5
    df["Error"] = list6
    return df


# execute all sql commands
def generate_summ_report(exec_id, con):
    cur = con.cursor()
    df = pd.DataFrame()
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    list5 = []
    list6 = []
    sql = "select left(convert_timezone('Asia/Kolkata', exec_dttm),24),ACCT_NAME,USER_NAME,SQL_CNT,SUCCESS_CNT,FAIL_CNT FROM SNOWFLAKE_POC.PUBLIC.EXECUTION_SUMMARY WHERE EXEC_ID=" + str(int(exec_id))
    cur.execute(sql)
    for record in cur:
        list1.append(record[0])
        list2.append(record[1])
        list3.append(record[2])
        list4.append(record[3])
        list5.append(record[4])
        list6.append(record[5])

    if cur is not None:
        cur.close()

    df["Date"] = list1
    df["Account"] = list2
    df["User"] = list3
    df["No. of SQL commands executed"] = list4
    df["Success count"] = list5
    df["Fail count"] = list6
    return df


def get_execution_dates(con):
    cur = con.cursor()
    exec_dt = []
    sql = "select EXEC_ID,left(convert_timezone('Asia/Kolkata', exec_dttm),24) FROM SNOWFLAKE_POC.PUBLIC.EXECUTION_SUMMARY order by EXEC_ID desc"
    cur.execute(sql)
    for record in cur:
        exec_dt.append("Execution ID=" + str(record[0]) + " And Execution Date=" + str(record[1]))

    if cur is not None:
        cur.close()

    return exec_dt

