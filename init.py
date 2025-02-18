import pymysql

def init():
    db = pymysql.connect(
        host="localhost",
        user="your-user",
        password="your-passwd",
        database="your-db"
    )
    return db

db = init()

def main():
    print(type(db))

if __name__ == "__main__":
    main()
