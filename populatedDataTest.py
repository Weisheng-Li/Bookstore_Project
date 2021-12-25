import mysql.connector
from datetime import datetime

db = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='15819216lz',
        auth_plugin='mysql_native_password',
        database="bookstoreDB")

cursor = db.cursor(buffered=True)


print_the_book = (
    "SELECT * "
    "FROM Book "
    "WHERE ISBN=%s")

find_authorID = (
    "SELECT authorID "
    "FROM authorship "
    "WHERE ISBN=%s")

print_the_author = (
    "SELECT Name "
    "FROM Author "
    "WHERE authorID=%s")

cursor.execute(print_the_book, ("9780099744214",))
for row in cursor:
    print("Book information: ")
    print(row)

print("Author: ")
cursor.execute(find_authorID, (row[0],))
cursor2 = db.cursor()
for x in cursor:
    cur_authorID = x[0]
    cursor2.execute(print_the_author, (cur_authorID,))
    print(cursor2.fetchone())

db.commit()


db.close()
