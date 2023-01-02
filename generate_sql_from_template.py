# generate SQL commands from template excel
def generate_sql(df,sheet_nm):
    sql_list = []
    col_num = len(df.columns)
    for index, row in df.iterrows():
        if sheet_nm=="WAREHOUSE":
            sql_template = 'CREATE WAREHOUSE '
            for x in range(col_num):
                if row[x] != '':
                    if x == 0:
                        sql_template = sql_template + str(row[x]) + ' '
                    else:
                        sql_template = sql_template + str(row.index[x]) + '=' + str(row[x]) + ' '
            sql_list.append(sql_template.replace(".0", ""))

        if sheet_nm=="STANDARD_DB":
            sql_template = 'CREATE DATABASE  '
            for x in range(col_num):
                if row[x] != '':
                    if x == 0:
                        sql_list.append("USE WAREHOUSE "+str(row[x]))
                    elif x==1:
                        sql_template = sql_template + str(row[x]) + ' '
                    elif x == 2:
                        sql_template = sql_template + 'TRANSIENT '
                    else:
                        sql_template = sql_template + str(row.index[x]) + '=' + str(row[x]) + ' '
            sql_list.append(sql_template.replace(".0", ""))

        if sheet_nm=="SCHEMA":
            sql_template = 'CREATE SCHEMA '
            for x in range(col_num):
                if row[x] != '':
                    if x == 0:
                        sql_list.append("USE WAREHOUSE "+str(row[x]))
                    elif x==1:
                        sql_template = sql_template + str(row[x]) + '.'
                    elif x==2:
                        sql_template = sql_template + str(row[x]) + ' '
                    else:
                        sql_template = sql_template + str(row.index[x]) + '=' + str(row[x]) + ' '
            sql_list.append(sql_template.replace(".0", ""))

        if sheet_nm=="TABLE":

            sql_template = 'CREATE TABLE '
            for x in range(col_num):
                if row[x] != '':
                    if x == 0:
                        sql_list.append("USE WAREHOUSE "+str(row[x]))
                    elif x==1:
                        sql_template = sql_template + str(row[x]) + '.'
                    elif x==2:
                        sql_template = sql_template + str(row[x]) + '.'
                    elif x==3:
                        sql_template = sql_template + str(row[x]) + ' ('
                    else:
                        sql_template = sql_template + str(row[x]) + ')'
            sql_list.append(sql_template.replace(".0", ""))

        if sheet_nm=="ROLE":
            sql_template = 'CREATE ROLE '
            for x in range(col_num):
                if row[x] != '':
                    if x == 0:
                        sql_template = sql_template + str(row[x]) + ' '
                    else:
                        sql_template = sql_template + str(row.index[x]) + '=' + str(row[x]) + ' '
            sql_list.append(sql_template.replace(".0", ""))

        if sheet_nm=="USER":
            sql_template = 'CREATE USER '
            for x in range(col_num):
                if row[x] != '':
                    if x == 0:
                        sql_template = sql_template + str(row[x]) + ' '

                    else:
                        sql_template = sql_template + str(row.index[x]) + "='" + str(row[x]) + "' "
            sql_list.append(sql_template.replace(".0", ""))

    return sql_list