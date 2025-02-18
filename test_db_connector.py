from init import db
import json

table_name = "test"

def get_col_names():
    cursor=db.cursor()
    sql = "SHOW COLUMNS FROM {}".format(table_name)
    cursor.execute(sql)
        
    # 获取所有列名
    columns = cursor.fetchall()
    column_list = list()
    for column in columns:
        column_list.append(column[0])
    return column_list

column_list = get_col_names()

def conv_db_result(col_names,data):
    if len(data) <= 0 or len(col_names) != len(data[0]):
        return list()
    result = list()
    for i in range(len(data)):
        row = dict()
        for j in range(len(col_names)):
            row[col_names[j]]=data[i][j]
        result.append(row)
    data = {"dataList":result}
    return data

def format_string(input):
    return "\""+input+"\""

def List(table, name, age):
    # 执行SQL查询
    cursor=db.cursor()
    sql = "SELECT * FROM {} limit 10".format(table_name)
    cursor.execute(sql)
 
    # 获取查询结果
    result = cursor.fetchall()
    cursor.close()
    return conv_db_result(column_list,result)

def Create(table, name, age):
    cursor=db.cursor()
    sql = "INSERT INTO {} (name, age) VALUES ({},{})".format(table,format_string(name),age)
    cursor.execute(sql)
    db.commit()
    cursor.close()

def Delete(table, id):
    cursor=db.cursor()
    sql = "DELETE FROM {} WHERE id = {}".format(table,id)
    print(sql)
    cursor.execute(sql)
    db.commit()
    cursor.close()

def main():
    res = List("test","","")
    print(res)
    return res

if __name__ == "__main__":
    main()
