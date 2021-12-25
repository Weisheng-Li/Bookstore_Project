import mysql.connector
import csv
import hashlib
from datetime import datetime

default_stock = 100
default_discount = 1
default_price = 10

try:
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='15819216lz',
        auth_plugin='mysql_native_password',
        database="bookstoreDB")

    db.autocommit = False
    cursor = db.cursor(buffered=True)

    # DB clean up
    delete2 = (
        "DELETE "
        "FROM OrderTable")
    cursor.execute(delete2)

    delete3 = (
        "DELETE "
        "FROM include")
    cursor.execute(delete3)

    delete4 = (
        "DELETE "
        "FROM shoppingCart")
    cursor.execute(delete4)

    delete5 = (
        "DELETE "
        "FROM Comment")
    cursor.execute(delete5)

    delete6 = (
        "DELETE "
        "FROM giveUsefulnessRating")
    cursor.execute(delete6)

    delete7 = (
        "DELETE "
        "FROM trust")
    cursor.execute(delete7)

    '''
    # Insert the first manager
    insert_firstManager = (
        "INSERT INTO Customer "
        "VALUES (%s, %s, %s, %s, %s, %s, %s)")

    pwd = "123456"
    pwd_storage = hashlib.sha256(pwd.encode('utf-8')).digest()[:8]
    pwd_storage = str(int.from_bytes(pwd_storage, "big"))
    cursor.execute(insert_firstManager, ("Origin", "Geralt", "of Rivia", pwd_storage, True, "Kaer Morhen", "9081201384"))

    insert_query = (
        "INSERT INTO Book "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")

    author_insert_query = (
        "INSERT INTO Author (Name) "
        "VALUES (%s)")

    authorship_insert_query = (
        "INSERT INTO authorship "
        "VALUES (%s, %s)")

    Allauthor_set = set()

    with open("books.csv", encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for (bookID, title, authors, average_rating, isbn, isbn13,
            language, numofPage, rating_count, text_review_count,
            pub_date, publisher) in csv_data:
            
            # skip the first line, which contains column names
            if line_count == 0:
                line_count += 1
                continue

            # handle the language 
            if language.find("en-") != -1:
                language = "eng"

            # truncate the string if it exceeds max length
            if len(title) > 100:
                title = title[:100]
            if len(publisher) > 70:
                publisher = publisher[:70]

            # parse the date
            month, day, year = pub_date.split('/')
            if len(month) < 2:
                month = '0' + month
            if len(day) < 2:
                day = '0' + day
            pub_date = year + '-' + month + '-' + day

            # parse the authors
            authorID = None
            author_list = authors.split("/")
            authorID_list = []
            for author in author_list:

                # repeated author check
                prev_len = len(Allauthor_set)
                Allauthor_set.add(author)
                later_len = len(Allauthor_set)
                if prev_len == later_len:
                    continue

                if len(author) > 30:
                    author = author[:30]

                cursor.execute(author_insert_query, (author,))
                authorID = cursor.lastrowid
                authorID_list.append(authorID)
                cursor.execute(authorship_insert_query, (isbn13, authorID))

            # Populate the one degree separation table
            separation_insert = (
                "INSERT INTO separation "
                "VALUES (%s, %s)")

            for A1 in authorID_list:
                for A2 in authorID_list:
                    if A1 != A2:
                        # ignore the duplicate key error, 
                        # because there is no way to avoid it
                        try: 
                            cursor.execute(separation_insert, (A1, A2))
                        except mysql.connector.IntegrityError:
                            pass


            # Populate the Book table
            cursor.execute(insert_query, (isbn13, title, publisher, language, 
                                          pub_date, numofPage, default_stock, 
                                          default_discount, default_price))
            
            line_count += 1

    '''
    db.commit()

except mysql.connector.Error as error:
    print("Transaction failed: {}".format(error))
    db.rollback()

finally:
    # print(f'current line count: {line_count}.')
    if db.is_connected():
        db.close()
