import sqlite3


conn = sqlite3.connect('mytest1.db')
cursor = conn.cursor()

print('hello SQL')

while True:
    name  = input('student\'s name')
    username = input('student\'s username')
    id_num = input('student\'s id number:')
 # '''insert语句 把一个新的行插入到表中'''

    sql = ''' insert into students
              (name, username, id)
              values
              (:st_name, :st_username, :id_num)'''
    # 把数据保存到name username和 id_num中
    cursor.execute(sql,{'st_name':name, 'st_username':username, 'id_num':id_num})
    conn.commit()
	break
    cont = ('Another student? ')
    if cont[0].lower() == 'n':
        break
cursor.close()
