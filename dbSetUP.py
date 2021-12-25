import mysql.connector
from datetime import datetime

db = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='15819216lz',
    auth_plugin='mysql_native_password',
    database="bookstoreDB")

cursor = db.cursor()

# DB creation
# cursor.execute("CREATE DATABASE bookstoreDB")

# Customer Table Creation
'''
cursor.execute("CREATE TABLE Customer \
                (loginName VARCHAR(30), \
                firstName VARCHAR(20) NOT NULL, \
                lastName VARCHAR(20) NOT NULL, \
                password VARCHAR(30) NOT NULL, \
                isManager BOOLEAN NOT NULL, \
                address VARCHAR(100) NOT NULL, \
                phoneNumber VARCHAR(15) NOT NULL, \
                PRIMARY KEY (loginName))")

cursor.execute("DESCRIBE Customer")
for x in cursor:
    print(x)
'''

# Create the first manager account
'''
cursor.execute("INSERT INTO Customer \
                VALUES (%s, %s, %s, %s, %s, %s, %s)", \
               ('Origin', 'Geralt', 'of Rivia', '123456', True, 'Kaer Morhen', '9081201384'))

db.commit()

cursor.execute("SELECT * FROM Customer")
for x in cursor:
    print(x)
'''

# Book Table Creation
'''
cursor.execute("CREATE TABLE Book \
                (ISBN CHAR(13), \
                title VARCHAR(100) NOT NULL, \
                publisher VARCHAR(70) NOT NULL, \
                language CHAR(3) NOT NULL, \
                publicationDate DATE, \
                numberOfPages SMALLINT CHECK(numberOfPages >= 0) NOT NULL, \
                stockLevel SMALLINT CHECK(stockLevel >= 0) NOT NULL, \
                discountPercentage DECIMAL(4,3) CHECK(discountPercentage <= 1 \
                                                 AND discountPercentage >= 0) NOT NULL, \
                price DECIMAL(7,2) CHECK(price >= 0) NOT NULL, \
                PRIMARY KEY (ISBN))")

cursor.execute("DESCRIBE Book")
for x in cursor:
    print(x)
'''

# Author Table Creation
'''
cursor.execute("CREATE TABLE Author \
                (Name VARCHAR(30) NOT NULL, \
                authorID INT AUTO_INCREMENT, \
                PRIMARY KEY (authorID))")

cursor.execute("DESCRIBE Author")
for x in cursor:
    print(x)
'''

# Authorship Table Creation
'''
cursor.execute("CREATE TABLE authorship \
                (ISBN CHAR(13), \
                authorID INT, \
                PRIMARY KEY (ISBN, authorID), \
                FOREIGN KEY (ISBN) REFERENCES Book(ISBN) \
                 ON UPDATE RESTRICT ON DELETE CASCADE, \
                FOREIGN KEY (authorID) REFERENCES Author(authorID) \
                 ON UPDATE RESTRICT ON DELETE RESTRICT)")

cursor.execute("DESCRIBE authorship")
for x in cursor:
    print(x)
'''

# has Table Creation (Connect book with keywords)
'''
cursor.execute("CREATE TABLE has \
                (ISBN CHAR(13), \
                keyword VARCHAR(30), \
                PRIMARY KEY (ISBN, keyword), \
                FOREIGN KEY (ISBN) REFERENCES Book(ISBN) \
                 ON UPDATE RESTRICT ON DELETE CASCADE)")

cursor.execute("DESCRIBE has")
for x in cursor:
    print(x)
'''

# classifiedAs Table Creation (Connect book with genre)
'''
cursor.execute("CREATE TABLE classifiedAs \
                (ISBN CHAR(13), \
                genre VARCHAR(15), \
                PRIMARY KEY (ISBN, genre), \
                FOREIGN KEY (ISBN) REFERENCES Book(ISBN) \
                 ON UPDATE RESTRICT ON DELETE CASCADE)")

cursor.execute("DESCRIBE classifiedAs")
for x in cursor:
    print(x)
'''

# Order Table (part of order)
'''
cursor.execute("CREATE TABLE OrderTable \
                (orderID INT AUTO_INCREMENT, \
                loginName VARCHAR(30) NOT NULL, \
                orderDate DATE NOT NULL, \
                PRIMARY KEY (orderID), \
                FOREIGN KEY (loginName) REFERENCES Customer(loginName) \
                 ON UPDATE RESTRICT ON DELETE RESTRICT)")

cursor.execute("DESCRIBE OrderTable")
for x in cursor:
    print(x)
'''


# Include Table (part of order)
'''
cursor.execute("CREATE TABLE include \
                (ISBN CHAR(13), \
                orderID INT, \
                purchasePrice DECIMAL(7, 2) NOT NULL, \
                quantity TINYINT NOT NULL, \
                PRIMARY KEY (ISBN, orderID), \
                FOREIGN KEY (ISBN) REFERENCES Book(ISBN) \
                 ON UPDATE RESTRICT ON DELETE RESTRICT, \
                FOREIGN KEY (orderID) REFERENCES OrderTable(orderID) \
                 ON UPDATE RESTRICT ON DELETE CASCADE)")

cursor.execute("DESCRIBE include")
for x in cursor:
    print(x)
'''


# Shopping Cart Table
'''
cursor.execute("CREATE TABLE shoppingCart \
                (loginName VARCHAR(30), \
                ISBN CHAR(13), \
                quantity TINYINT NOT NULL, \
                PRIMARY KEY (loginName, ISBN), \
                FOREIGN KEY (loginName) REFERENCES Customer(loginName) \
                 ON UPDATE RESTRICT ON DELETE RESTRICT, \
                FOREIGN KEY (ISBN) REFERENCES Book(ISBN) \
                 ON UPDATE RESTRICT ON DELETE CASCADE)")

cursor.execute("DESCRIBE shoppingCart")
for x in cursor:
    print(x)
'''

# Create Comment table
'''
cursor.execute("CREATE TABLE Comment \
                (ISBN CHAR(13), \
                loginName VARCHAR(30), \
                score TINYINT NOT NULL, \
                commentDate DATE NOT NULL, \
                msg TEXT, \
                avgUsefulnessScore INT DEFAULT 0, \
                PRIMARY KEY (loginName, ISBN), \
                FOREIGN KEY (loginName) REFERENCES Customer(loginName) \
                 ON UPDATE RESTRICT ON DELETE RESTRICT, \
                FOREIGN KEY (ISBN) REFERENCES Book(ISBN) \
                 ON UPDATE RESTRICT ON DELETE CASCADE)")

cursor.execute("DESCRIBE Comment")
for x in cursor:
    print(x)
'''

# Create giveUsefulnessRating table
'''
cursor.execute("CREATE TABLE giveUsefulnessRating \
                (ISBN CHAR(13), \
                commentGiver VARCHAR(30), \
                ratingGiver VARCHAR(30), \
                score ENUM('useless', 'useful', 'very useful') NOT NULL, \
                PRIMARY KEY (ISBN, commentGiver, ratingGiver), \
                FOREIGN KEY (commentGiver) REFERENCES Customer(loginName) \
                 ON UPDATE RESTRICT ON DELETE RESTRICT, \
                FOREIGN KEY (ratingGiver) REFERENCES Customer(loginName) \
                 ON UPDATE RESTRICT ON DELETE RESTRICT, \
                FOREIGN KEY (ISBN) REFERENCES Book(ISBN) \
                 ON UPDATE RESTRICT ON DELETE CASCADE)")

cursor.execute("DESCRIBE giveUsefulnessRating")
for x in cursor:
    print(x)
'''

# Create the trust table
'''
cursor.execute("CREATE TABLE trust \
                (giver VARCHAR(30), \
                receiver VARCHAR(30), \
                isTrusted BOOL NOT NULL, \
                PRIMARY KEY (giver, receiver), \
                FOREIGN KEY (giver) REFERENCES Customer(loginName) \
                 ON UPDATE RESTRICT ON DELETE RESTRICT, \
                FOREIGN KEY (receiver) REFERENCES Customer(loginName) \
                 ON UPDATE RESTRICT ON DELETE RESTRICT)")

cursor.execute("DESCRIBE trust")
for x in cursor:
    print(x)
'''

# Create degree separation table
'''
cursor.execute("CREATE TABLE separation \
                (firstAuthorID INT, \
                secondAuthorID INT, \
                PRIMARY KEY (firstAuthorID, secondAuthorID), \
                FOREIGN KEY (firstAuthorID) REFERENCES Author(authorID) \
                 ON UPDATE RESTRICT ON DELETE CASCADE, \
                FOREIGN KEY (secondAuthorID) REFERENCES Author(authorID) \
                 ON UPDATE RESTRICT ON DELETE CASCADE)")

cursor.execute("DESCRIBE separation")
for x in cursor:
    print(x)
'''