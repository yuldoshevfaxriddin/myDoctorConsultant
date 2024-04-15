import mysql.connector as mysql
import settings
import datetime
conn = mysql.connect(host=settings.DB_HOSTNAME,user=settings.DB_USERNAME,password=settings.DB_PASSWORD,database=settings.DB_NAME)

cursor = conn.cursor()

def showTables():
    cursor.execute('SHOW TABLES')
    for i in cursor:
        print(i)
def showUsers():
    cursor.execute("SELECT * FROM users")
    myresult = cursor.fetchall()
    for x in myresult:
          print(x)
def dropTables():
    cursor.execute("SHOW TABLES")
    table_list = []
    for x in cursor:
        table_list.append(x[0])
    print('tables',table_list)
    for i in table_list:
        cursor.execute(f"DROP TABLE {i}")
        # mycursor.execute(f"DROP TABLE region")

    print('dropping succes !')

def createTables():
    cursor.execute(""" CREATE TABLE users (
        id INT AUTO_INCREMENT PRIMARY KEY, 
        name VARCHAR(255),
        username VARCHAR(255),
        password VARCHAR(255),
        created_at VARCHAR(255)
        ); """)
    cursor.execute(""" CREATE TABLE personal_chat (
        id INT AUTO_INCREMENT PRIMARY KEY, 
        user_1 VARCHAR(255),
        user_2 VARCHAR(255),
        created_at VARCHAR(255)
        ); """)
    cursor.execute(""" CREATE TABLE chat (
        id INT AUTO_INCREMENT PRIMARY KEY,
        chat_name VARCHAR(255),
        created_at VARCHAR(255)
        ); """)
    cursor.execute(""" CREATE TABLE multi_chat (
        chat_id VARCHAR(255),
        user_id VARCHAR(255),
        created_at VARCHAR(255)
        ); """)
    cursor.execute(""" CREATE TABLE messages (
        id INT AUTO_INCREMENT PRIMARY KEY,
        chat_id VARCHAR(255),
        user_id VARCHAR(255),
        text TEXT,
        created_at VARCHAR(255)
        ); """)
    cursor.execute(""" CREATE TABLE sessions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id VARCHAR(255),
        request_session VARCHAR(255),
        created_at VARCHAR(255)
        ); """)
    
    print('tables created !')

def createUser(user:dict):
    sql_1 = f"""INSERT INTO users ( `name`, `username`, `password`, `created_at`) 
        VALUES ('{user['name']}','{user['username']}','{user['password']}','{datetime.datetime.timestamp(datetime.datetime.now())}')"""
    cursor.execute(sql_1)
    last_user_id = cursor.lastrowid
    # sql_2 = f"""INSERT INTO sessions ( `user_id`, `request_session`) 
    #     VALUES ('{last_user_id}','{user['request_session']}')"""
    # cursor.execute(sql_2)
    conn.commit()
    return last_user_id
def createPersonalChat(user_id_1,user_id_2):
    sql = f"""INSERT INTO personal_chat ( `user_1`, `user_2`, `created_at`) 
        VALUES ('{user_id_1}','{user_id_2}','{datetime.datetime.timestamp(datetime.datetime.now())}')"""
    cursor.execute(sql)
    conn.commit()
    return cursor.lastrowid
def createChat(chat_name):
    sql = f"""INSERT INTO chat ( `chat_name`, `created_at`) 
        VALUES ('{chat_name}','{datetime.datetime.timestamp(datetime.datetime.now())}')"""
    cursor.execute(sql)
    conn.commit()
    return cursor.lastrowid
def createMultiChat(chat_id,user_id):
    sql = f"""INSERT INTO multi_chat ( `chat_id`,`user_id`, `created_at`) 
        VALUES ('{chat_id}','{user_id}','{datetime.datetime.timestamp(datetime.datetime.now())}')"""
    cursor.execute(sql)
    conn.commit()
    return cursor.lastrowid
def createMessage(chat_id,user_id,message):
    sql = f"""INSERT INTO messages ( `chat_id`,`user_id`,`text`, `created_at`) 
        VALUES ('{chat_id}','{user_id}','{message}','{datetime.datetime.timestamp(datetime.datetime.now())}')"""
    cursor.execute(sql)
    conn.commit()
    return cursor.lastrowid
def createSession(user_id,new_session):
    sql = f"""INSERT INTO sessions ( `user_id`,`request_session`, `created_at`) 
        VALUES ('{user_id}','{new_session}','{datetime.datetime.timestamp(datetime.datetime.now())}')"""
    cursor.execute(sql)
    conn.commit()
    return cursor.lastrowid

def updateUserSession(user):
    sql = f"""UPDATE `sessions` SET `request_session`='{user['request_session']}',`created_at`='{datetime.datetime.timestamp(datetime.datetime.now())}' WHERE `user_id`={user['id']};"""
    cursor.execute(sql)
    conn.commit()
    
def checkUser(user_name,user_password,user_session=None):
    sql = f"SELECT * FROM users WHERE `username`='{user_name}' AND `password`='{user_password}'"
    cursor.execute(sql)
    myresult = cursor.fetchall()
    if len(myresult) > 0:
        user = {
            'id':myresult[0][0],
            'request_session':user_session
        }
    return myresult
def checkUserSession(user):
    sql = f"SELECT * FROM sessions WHERE `user_id`='{user['id']}'"
    cursor.execute(sql)
    myresult = cursor.fetchall()
    message = ''
    if len(myresult) > 0:
        updateUserSession(user)
        message = 'session update'
    else:
        createSession(user['id'],user['request_session'])
        message = 'session create'
    return {'message':message,'status':myresult}

def getPersonalChats(user_1):
    sql = f"SELECT * FROM personal_chat WHERE `user_1`='{user_1}' OR `user_2`='{user_1}') "
    cursor.execute(sql)
    myresult = cursor.fetchall()
    print(myresult)
    # updateUserSession(user)
    return myresult


def dbSeeder():
    createTables()
    chat_names = ['global','toshkent','xorazm','surxondaryo']
    for chat_name in chat_names:
        createChat(chat_name)
    print('seeder succes !')

if __name__=='__main__':

    # user = {}
    # user['name'] = 'tohir'
    # user['username'] = '@tohir'
    # user['password'] = 'toh123'
    # user['request_session'] = 'abc12312sdfs'

    showTables()
    # dropTables()
    # dbSeeder()
    # createUser(user=user)
    # user['id'] = 16
    # user['request_session'] = 'salom'
    # updateUserSession(user)
    # creatPersonalChat(13,16)
    # createMultiChat(2,12)
    # createMessage(2,10,'salom dunyo hammaga !')
    # print(checkUser('@tohir','toh123','salom_session'))
    # showUsers()
