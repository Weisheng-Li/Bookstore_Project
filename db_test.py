import mysql.connector
from datetime import datetime

db = mysql.connector.connect(
	host='localhost',
	user='root',
	passwd='15819216lz',
	auth_plugin='mysql_native_password',
	database="testdatabase")

cursor = db.cursor()

cursor.execute("CREATE DATABASE testdatabase")

# Create a database
'''
cursor.execute("CREATE TABLE Person (name VARCHAR(50), \
				age SMALLINT UNSIGNED, \
				personID INT PRIMARY KEY AUTO_INCREMENT, \
				gender ENUM('M', 'F'), \
				birthdate DATETIME)")

cursor.execute("DESCRIBE Person")
cursor.execute("SHOW TABLES")
'''
mycursor.execute("INSERT INTO Person (name, age, gender, birthdate) VALUES (%s, %s, %s, %s)", ("tim", 19, "M", datetime.now()))
db.commit()

# Change column data type
cursor.execute("ALTER TABLE Person CHANGE name name VARCHAR(4)")


for x in mycursor:
	print(x);

print(cursor.fetchone())

# Bulk Insert (kind of)
users = [('tim', 'techwithtim'), 
		('joe', 'joey123'), 
		('sarah', 'sarah345')]

user_scores = [(45, 100), 
			(30, 200), 
			(46, 124)]

Q1 = "CREATE TABLE Users(id int PRIMARY KEY AUTO_INCREMENT, \
 						 name VARCHAR(50), \
 						 passwd VARCHAR(50))"

Q2 = "CREATE TABLE Scores (user int PRIMARY KEY, \
	  FOREIGN KEY(userID) REFERENCES Users(id), \
	  game1 int DEFAULT 0, game2 int DEFAULT 0)"

cursor.execute(Q1)
cursor.execute(Q2)

# insert multiple records at the same time
cursor.executemany("INSERT INTO Users (name, passwd) VALUES (%s, %s)", users)

Q3 = "INSERT INTO Users (name, passwd) VALUES (%s, %s)"
Q4 = "INSERT INTO Scores (userId, game1, game2) VALUES (%s, %s, %s)"

for x, user in enumerate(users):
	cursor.execute(Q3, users)
	last_id = cursor.lastrowid
	cursor.execute(Q4, (last_id,) + user_scores[x])

