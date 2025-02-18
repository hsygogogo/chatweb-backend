from init import db
import json

table_name = "user"

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

def List():
    # 执行SQL查询
    cursor=db.cursor()
    sql = "SELECT * FROM {} limit 10".format(table_name)
    cursor.execute(sql)
 
    # 获取查询结果
    result = cursor.fetchall()
    cursor.close()
    return conv_db_result(column_list,result)

def Count():
    # 执行SQL查询
    cursor=db.cursor()
    sql = "SELECT count(*) FROM {} limit 1".format(table_name)
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    #print(result)
    return result


def ListByPage(limit,offset):
    # 执行SQL查询
    cursor=db.cursor()
    sql = "SELECT * FROM {} limit {} offset {}".format(table_name,limit,offset)
    cursor.execute(sql)
 
    # 获取查询结果
    result = cursor.fetchall()
    cursor.close()
    return conv_db_result(column_list,result)

def Create(name, age, gender, mobile_no):
    cursor=db.cursor()
    sql = "INSERT INTO {} (name, age, gender, mobile_no) VALUES ({},{},{},{})".format(table_name,format_string(name),age, \
      format_string(gender), format_string(mobile_no))
    cursor.execute(sql)
    db.commit()
    cursor.close()

def Delete(id):
    cursor=db.cursor()
    sql = "DELETE FROM {} WHERE id = {}".format(table_name,id)
    print(sql)
    cursor.execute(sql)
    db.commit()
    cursor.close()

def main():
    res = List()
    print(res)
    res = Count()
    print(res)
    return res

if __name__ == "__main__":
    main()
