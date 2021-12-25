from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import datetime, date, timedelta
import mysql.connector
import hashlib
import os

app = Flask(__name__)
# The following two settings are both for sessions to work
app.secret_key = "Asoiw930857SKkce"
app.permanent_session_lifetime = timedelta(minutes=5)

db = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='15819216lz',
    auth_plugin='mysql_native_password',
    database="bookstoreDB")

@app.route("/")
def home():
    if "fname" in session:
        fname = session["fname"]
    else: 
        fname = ""
    return render_template("index.html", firstName = (", " + fname) if fname else "")

@app.route("/userSignUp", methods=["POST", "GET"])
def userSignUp():
    if "user" in session:
        flash("Please log out first")
        return redirect(url_for("home"))

    if request.method == "POST":
        logname = fname = lname = pwd = addr = pn = ""
        if "logname" in request.form:
            logname = request.form["logname"]
        if "fname" in request.form:
            fname = request.form["fname"]
        if "lname" in request.form:
            lname = request.form["lname"]
        if "pwd" in request.form:
            pwd = request.form["pwd"]
        if "addr" in request.form:
            addr = request.form["addr"]
        if "pn" in request.form:
            pn = request.form["pn"]

        # if all entries are not empty
        if logname and fname and lname and \
            pwd and addr and pn:

            cursor = db.cursor(buffered=True)

            # Hash the password
            pwd_storage = hashlib.sha256(pwd.encode('utf-8')).digest()[:8]
            pwd_storage = str(int.from_bytes(pwd_storage, "big"))

            # add user information into the database
            cursor.execute("INSERT INTO Customer \
                            VALUES (%s, %s, %s, %s, %s, %s, %s)", \
                            (logname, fname, lname, pwd_storage, False, addr, pn))

            db.commit()
            cursor.close()
            flash("Your account has been created!")
            return redirect(url_for("login"))
        else: 
            flash("You need to fill out all entries!")
            return render_template("signUp.html")
    else:
        return render_template("signUp.html")

@app.route("/managerSignUp", methods=["POST", "GET"])
def managerSignUp():
    if "ism" in session and session["ism"] == True: 
        if request.method == "POST":
            logname = fname = lname = pwd = addr = pn = ""
            if "logname" in request.form:
                logname = request.form["logname"]
            if "fname" in request.form:
                fname = request.form["fname"]
            if "lname" in request.form:
                lname = request.form["lname"]
            if "pwd" in request.form:
                pwd = request.form["pwd"]
            if "addr" in request.form:
                addr = request.form["addr"]
            if "pn" in request.form:
                pn = request.form["pn"]

            # if all entries are not empty
            if logname and fname and lname and \
                pwd and addr and pn:

                cursor = db.cursor(buffered=True)

                # Hash the password
                pwd_storage = hashlib.sha256(pwd.encode('utf-8')).digest()[:8]
                pwd_storage = str(int.from_bytes(pwd_storage, "big"))

                # add user information into the database
                cursor.execute("INSERT INTO Customer \
                                VALUES (%s, %s, %s, %s, %s, %s, %s)", \
                                (logname, fname, lname, pwd_storage, True, addr, pn))

                db.commit()
                cursor.close()
                flash("Your manager account has been created!")
                return redirect(url_for("login"))
            else: 
                flash("You need to fill out all entries!")
                return render_template("signUp.html")
        else:
            return render_template("signUp.html")
    else:
        flash("Only managers can create manager account!")
        return redirect(url_for("home"))

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        logname = pwd = ""
        if "logname" in request.form:
            logname = request.form["logname"]
        if "pwd" in request.form:
            pwd = request.form["pwd"]

        cursor = db.cursor(buffered=True)

        find_user = (
        "SELECT * "
        "FROM Customer "
        "WHERE loginName = %s")

        cursor.execute(find_user, (logname,))

        row = cursor.fetchone()
        cursor.close()

        # Check correctness of the password
        correct_raw_pwd = row[3]
        correct_decoded_pwd = (int(correct_raw_pwd)).to_bytes(8, byteorder='big')

        input_key = hashlib.sha256(pwd.encode('utf-8')).digest()[:8]

        if input_key != correct_decoded_pwd:
            flash("login failed! Please double check your login name and password")
            return redirect(url_for("login"))
        else:
            (loginName, firstName, lastName, password, isManager,
            address, phoneNumber) = row;

            session["user"] = logname
            session["fname"] = firstName
            session["lname"] = lastName
            session["ism"] = isManager
            session["addr"] = address
            session["pn"] = phoneNumber

            return redirect(url_for("home"))
    else:
        if "user" in session:
            return redirect(url_for("home"))

        return render_template("login.html")

@app.route("/logout")
def logout():
    if "user" in session:
        flash("You have been logged out!")
        session.pop("user", None)
        session.pop("fname", None)
        session.pop("lname", None)
        session.pop("pwd", None)
        session.pop("ism", None)
        session.pop("addr", None)
        session.pop("pn", None)
    return redirect(url_for("login"))

@app.route("/bookPage", methods=["POST", "GET"])
def bookPage():
    if request.method == "POST":
        if "user" in session:
            cursor = db.cursor(buffered=True)

            # if user tries to add this book into his shopping cart
            if "quant" in request.form:
                quantity = request.form["quant"]

                check_existence = (
                    "SELECT * "
                    "FROM shoppingCart "
                    "WHERE loginName=%s AND ISBN=%s")

                cart_insert = (
                    "INSERT INTO shoppingCart "
                    "VALUES (%s, %s, %s)")

                cart_update = (
                    "UPDATE shoppingCart "
                    "SET quantity=%s "
                    "WHERE loginName=%s AND ISBN=%s")

                cursor.execute(check_existence, (session["user"], request.args["ISBN"]))
                # The book is already in the shopping cart
                if cursor.rowcount != 0:
                    cursor.execute(cart_update, (quantity, session["user"], request.args["ISBN"]))
                    flash("The quantity of the book in your shopping cart has been updated.")
                else:
                    cursor.execute(cart_insert, (session["user"], request.args["ISBN"], quantity))
                    flash("This book has been added to you shopping cart.")
                
                db.commit()

            elif "score" in request.form:
                if int(request.form["score"]) > 10 or int(request.form["score"]) < 0:
                    flash("The score is out of range!")
                    return redirect(url_for("bookPage") + "?ISBN=" + request.args["ISBN"])

                # test if comment already exist
                userComment_query = (
                    "SELECT score, msg "
                    "FROM Comment "
                    "WHERE ISBN=%s AND loginName=%s")
            
                cursor.execute(userComment_query, (request.args["ISBN"], session["user"]))
                hasComment = (cursor.rowcount != 0)


                if hasComment:
                    if "mycmt" in request.form:
                        userComment_update = (
                            "UPDATE Comment "
                            "SET score=%s, msg=%s, commentDate=%s "
                            "WHERE ISBN=%s AND loginName=%s")
                        
                        cursor.execute(userComment_update, (request.form["score"], request.form["mycmt"], 
                                                            date.today(), request.args["ISBN"], session["user"]))
                    else: 
                        userComment_update = (
                            "UPDATE Comment "
                            "SET score=%s, msg=%s, commentDate=%s "
                            "WHERE ISBN=%s AND loginName=%s")
                        
                        cursor.execute(userComment_update, (request.form["score"], None, 
                                                            date.today(), request.args["ISBN"], session["user"]))
                else:
                    if request.form["mycmt"]:
                        leave_comment = (
                            "INSERT INTO Comment (ISBN, loginName, score, commentDate, msg) "
                            "VALUES (%s, %s, %s, %s, %s)")
                        cursor.execute(leave_comment, (request.args["ISBN"], session["user"], 
                                       int(request.form["score"]), date.today(), request.form["mycmt"]))
                    else:
                        leave_comment = (
                            "INSERT INTO Comment (ISBN, loginName, score, commentDate) "
                            "VALUES (%s, %s, %s, %s)")
                        cursor.execute(leave_comment, (request.args["ISBN"], session["user"], 
                                       int(request.form["score"]), date.today()))

                db.commit()
                flash("Your Comment has been posted")
            else:
                pass

            cursor.close()
            if "n" in request.form:
                return redirect(url_for("bookPage") + "?ISBN=" + request.args["ISBN"] + "&n=" + request.form["n"])
            return redirect(url_for("bookPage") + "?ISBN=" + request.args["ISBN"])
        else:
            if "n" in request.form:
                return redirect(url_for("bookPage") + "?ISBN=" + request.args["ISBN"] + "&n=" + request.form["n"])
            else:
                flash("Please login first!")
                return redirect(url_for("bookPage") + "?ISBN=" + request.args["ISBN"])
    else:
        cur_ISBN = request.args["ISBN"]

        # fetch basic information for the book
        bookinfo_query = (
            "SELECT * "
            "FROM Book NATURAL JOIN authorship NATURAL JOIN Author "
            "WHERE ISBN=%s")

        cursor = db.cursor(buffered=True)
        cursor2 = db.cursor(buffered=True)
        cursor.execute(bookinfo_query, (cur_ISBN,))

        # Combine all authors of the book into a author string
        authorList = []
        for bookInfo in cursor:
            authorList.append(bookInfo[10])

        authorstr = ", ".join(authorList)

        # Calculate the current price (discount percentage * price)
        cur_price = round(bookInfo[8] * bookInfo[9], 2)

        # fetch keywords and genres
        keyword_query = (
            "SELECT keyword "
            "FROM has "
            "WHERE ISBN=%s")

        cursor.execute(keyword_query, (cur_ISBN,))

        keyword_list = []
        for row in cursor:
            keyword_list.append(row[0])
        keywordstr = ", ".join(keyword_list)

        genre_query = (
            "SELECT genre "
            "FROM classifiedAs "
            "WHERE ISBN=%s")

        cursor.execute(genre_query, (cur_ISBN,))

        genre_list = []
        for row in cursor:
            genre_list.append(row[0])
        genrestr = ", ".join(genre_list)

        # find the lowerest price in the history
        lowestPrice_query = (
            "SELECT purchasePrice "
            "FROM include "
            "WHERE ISBN=%s "
            "ORDER BY purchasePrice DESC "
            "LIMIT 1")

        cursor.execute(lowestPrice_query, (bookInfo[1],))

        if cursor.rowcount != 0:
            lowestPrice = round(cursor.fetchone()[0], 2)
        else:
            lowestPrice = cur_price

        # List all the book suggestion (up to 5)
        suggestion_query = (
            "SELECT inc2.ISBN "
            "FROM include inc1 JOIN include inc2 ON inc1.orderID = inc2.orderID "
            "WHERE inc1.ISBN=%s AND inc2.ISBN!=%s "
            "GROUP BY inc2.ISBN "
            "ORDER BY SUM(inc2.quantity) DESC "
            "LIMIT 5")

        cursor.execute(suggestion_query, (bookInfo[1], bookInfo[1]))

        suggested_bookInfo_query = (
            "SELECT ISBN, title "
            "FROM Book "
            "WHERE ISBN=%s")

        suggested_books = []
        for row in cursor:
            cursor2.execute(suggested_bookInfo_query, row)
            suggested_books.append(cursor2.fetchone())

        # fetch current user's comment
        userComment = None
        if "user" in session:
            userComment_query = (
                "SELECT score, msg "
                "FROM Comment "
                "WHERE ISBN=%s AND loginName=%s")

            cursor.execute(userComment_query, (cur_ISBN, session["user"]))
            userComment = cursor.fetchone()

        # fetch all comments on this book
        parameters = (cur_ISBN,)

        if "user" in session:
            comment_query = (
                "SELECT * "
                "FROM Comment "
                "WHERE ISBN=%s AND loginName!=%s")
            parameters += (session["user"],)

        else:
            comment_query = (
                "SELECT * "
                "FROM Comment "
                "WHERE ISBN=%s")

        if "n" in request.args:
            comment_query += (
                " ORDER BY avgUsefulnessScore DESC"
                " LIMIT %s")
            parameters += (int(request.args["n"]),)

        cursor.execute(comment_query, parameters)

        comments = []
        for row in cursor:
            comments.append(row)

        cursor.close()
        cursor2.close()

        return render_template("bookPage.html", values=bookInfo + (cur_price,) + (lowestPrice,), authors=authorstr,
                                                mycomment=userComment, comment=comments, suggestions=suggested_books,
                                                keywords=keywordstr, genres=genrestr)

@app.route("/shoppingCart", methods=["POST", "GET"])
def shoppingCart():
    if request.method == "POST":
        # User just place the order

        cursor = db.cursor(buffered=True)

        # retrieve order information from shopping cart
        shpcart_query = (
            "SELECT * "
            "FROM shoppingCart "
            "WHERE loginName=%s")

        price_query = (
            "SELECT discountPercentage, price, stockLevel, title "
            "FROM Book "
            "WHERE ISBN=%s")

        cursor.execute(shpcart_query, (session["user"],))

        orders = []
        cursor2 = db.cursor(buffered=True)
        for row in cursor:
            cursor2.execute(price_query, (row[1],))
            cur_book = cursor2.fetchone()
            edited_row = row + ((cur_book[0] * cur_book[1]),)

            # check if there are sufficient copies available
            if cur_book[2] < row[2]:
                flash(cur_book[3] + " doesn't have sufficient stock")
                cursor2.close()
                cursor.close()
                return redirect(url_for("shoppingCart"))

            edited_row += (cur_book[2],)
            orders.append(edited_row)

        cursor2.close()

        # Store order information into the database and reduce stock level
        place_order1 = (
            "INSERT INTO OrderTable (loginName, orderDate) "
            "VALUES (%s, %s)")
        place_order2 = (
            "INSERT INTO include "
            "VALUES (%s, %s, %s, %s)")
        reduce_stock = (
            "UPDATE Book "
            "SET stockLevel=stockLevel-%s "
            "WHERE ISBN=%s")

        cursor.execute(place_order1, (session["user"], date.today()))
        orderID = cursor.lastrowid
        for row in orders:
            # row: loginName, ISBN, quantity, current price, stockLevel
            cursor.execute(place_order2, (row[1], orderID, row[3], row[2]))
            cursor.execute(reduce_stock, (row[2], row[1]))

        # Clear the shopping cart
        clear_shoppingcart = (
            "DELETE "
            "FROM shoppingCart "
            "WHERE loginName=%s")
        cursor.execute(clear_shoppingcart, (session["user"],))

        db.commit()
        cursor.close()

        flash("Your order has been placed!")
        return redirect(url_for("shoppingCart"))
    else:
        if "user" in session:
            shpcart_query = (
                "SELECT * "
                "FROM shoppingCart "
                "WHERE loginName=%s")

            title_query = (
                "SELECT title, discountPercentage, price "
                "From Book "
                "WHERE ISBN=%s")

            cursor1 = db.cursor(buffered=True)
            cursor2 = db.cursor(buffered=True)

            cursor1.execute(shpcart_query, (session["user"],))
            result = []
            totalprice = 0
            for row in cursor1:
                rowList = list(row)

                # replace ISBN with title
                cursor2.execute(title_query, (row[1],))
                cur_book = cursor2.fetchone()
                rowList[1] = cur_book[0]

                # add the current price
                rowList.append(round(cur_book[1] * cur_book[2] * row[2], 2))
                totalprice += rowList[-1]

                # add ISBN
                rowList.append(row[1])

                result.append(rowList)

            cursor1.close()
            cursor2.close()
            return render_template("shoppingCart.html", values=result, total=totalprice)
        else:
            flash("Please login first")
            return redirect(url_for("login"))

@app.route("/bookBrowsing", methods=["POST", "GET"])
def bookBrowsing():
    if request.method == "POST":
        aut_input = pub_input = tit_input = lang_input = None
        if "aut" in request.form:
            aut_input = request.form["aut"]
        if "pub" in request.form:
            pub_input = request.form["pub"]
        if "tit" in request.form:
            tit_input = request.form["tit"]
        if "lang" in request.form:
            lang_input = request.form["lang"]

        if not aut_input and not pub_input and not tit_input and not lang_input:
            # Do nothing
            return render_template("bookBrowsing.html") 

        search_query = (
            "SELECT ISBN, title, Name, publicationDate "
            "FROM Book NATURAL JOIN authorship NATURAL JOIN Author "
            "WHERE")

        appendAND = 0
        args_tuple = tuple()
        if aut_input:
            if len(aut_input) > 30:
                aut_input = aut_input[:30]
            search_query += " Name LIKE %s"
            aut_input = "%" + aut_input + "%"
            args_tuple += (aut_input,)
            appendAND = 1

        if pub_input:
            if len(pub_input) > 70:
                pub_input = pub_input[:70]
            if appendAND == 1:
                search_query += " AND"
            search_query += " publisher LIKE %s"
            pub_input = "%" + pub_input + "%"
            args_tuple += (pub_input,)
            appendAND = 1

        if tit_input:
            if len(tit_input) > 100:
                tit_input = tit_input[:100]
            if appendAND == 1:
                search_query += " AND"
            search_query += " title LIKE %s"
            tit_input = "%" + tit_input + "%"
            args_tuple += (tit_input,)
            appendAND = 1

        if lang_input:
            if len(lang_input) > 3:
                lang_input = lang_input[:3]
            if appendAND == 1:
                search_query += " AND"
            search_query += " language LIKE %s"
            lang_input = "%" + lang_input + "%"
            args_tuple += (lang_input,)
            appendAND = 1

        # Handle "Only show books with discount" Option
        if "disc_only" in request.form:
            search_query += " AND discountPercentage<1"

        # Process the query string based on desired sorting order
        if "order" in request.form:
            if request.form["order"] == "pub_date":
                search_query += " ORDER BY publicationDate DESC"

        cursor = db.cursor(buffered=True)

        cursor.execute(search_query, args_tuple)

        search_result = []
        ISBN_set = set() # check no duplicate books
        max_count = 80
        for row in cursor:
            len1 = len(ISBN_set)
            ISBN_set.add(row[0])
            len2 = len(ISBN_set)

            if len1 == len2:
                continue
                
            max_count -= 1
            if max_count < 0:
                break
            search_result.append(row)

        cursor.close()

        return render_template("bookBrowsing.html", values=search_result) 
    else:
        return render_template("bookBrowsing.html") 

@app.route("/comment", methods=["POST", "GET"])
def comment():
    # Get all information about this comment
    ISBN = request.args["ISBN"]
    loginName = request.args["logName"]

    cursor = db.cursor(buffered=True)

    find_comment = (
        "SELECT * "
        "FROM Comment "
        "WHERE ISBN=%s AND loginName=%s")

    cursor.execute(find_comment, (ISBN, loginName))
    # commentInfo: ISBN, loginName, score, commentDate, msg, avgUsefulnessScore
    commentInfo = cursor.fetchone()

    # Fetch information about this user
    user_query = (
        "SELECT firstName, lastName, isManager "
        "FROM Customer "
        "WHERE loginName=%s")

    cursor.execute(user_query, (loginName,))
    user_info = cursor.fetchone()

    trustCount_query = (
        "SELECT isTrusted, COUNT(*)"
        "FROM trust "
        "WHERE receiver=%s "
        "GROUP BY isTrusted")

    cursor.execute(trustCount_query, (loginName,))
    trustCount_dic = {}
    for row in cursor:
        trustCount_dic[row[0]] = row[1]

    # Get other comments he or she has made
    otherComment_query = (
        "SELECT ISBN, title, score, msg "
        "FROM Book NATURAL JOIN Comment "
        "WHERE loginName=%s AND ISBN!=%s")

    cursor.execute(otherComment_query, (loginName, ISBN))

    otherComment_list = []
    for row in cursor:
        otherComment_list.append(row)

    cursor.close()

    if request.method == "POST":
        if "user" not in session:
            flash("Please login first")
            return render_template("comment.html", values=commentInfo, userInfo=user_info, 
                                                trustcount=trustCount_dic, otherComment=otherComment_list)

        # if user click the rating submission button
        if "usefulRating" in request.form:
            rating = request.form["usefulRating"]

            cursor = db.cursor(buffered=True)

            check_exist_rating = (
                "SELECT * "
                "FROM giveUsefulnessRating "
                "WHERE ISBN=%s AND commentGiver=%s AND ratingGiver=%s")

            cursor.execute(check_exist_rating, (commentInfo[0], commentInfo[1], session["user"]))

            existRating=(cursor.rowcount != 0)
            if existRating:
                usefulRating_update = (
                    "UPDATE giveUsefulnessRating "
                    "SET score=%s "
                    "WHERE ISBN=%s AND commentGiver=%s AND ratingGiver=%s")
                cursor.execute(usefulRating_update, (rating, commentInfo[0], commentInfo[1], session["user"]))
            else:
                usefulRating_insert = (
                    "INSERT INTO giveUsefulnessRating "
                    "VALUES (%s, %s, %s, %s)")
                cursor.execute(usefulRating_insert, (commentInfo[0], commentInfo[1], session["user"], rating))

            # Update the average usefulness score of a comment
            find_usefulness_score = (
                "SELECT score "
                "FROM giveUsefulnessRating "
                "WHERE ISBN=%s AND commentGiver=%s")
            cursor.execute(find_usefulness_score, (commentInfo[0], commentInfo[1]))

            rating_count = {
                "very useful": 0,
                "useful": 0,
                "useless": 0
            }
            for row in cursor:
                rating_count[row[0]] += 1

            avg = rating_count["very useful"] * 2 + \
                  rating_count["useful"] * 1 + \
                  rating_count["useless"] * -1 \

            update_avg_useful = (
                "UPDATE Comment "
                "SET avgUsefulnessScore=%s "
                "WHERE ISBN=%s AND loginName=%s")

            cursor.execute(update_avg_useful, (avg, commentInfo[0], commentInfo[1]))
            
            flash("your usefulness rating has been submitted")

        # if user click the "Trust this user button"
        if "isTrust" in request.form:
            # check if the user is already in the trusted list
            cursor = db.cursor(buffered=True)

            check_if_trusted = (
                "SELECT * "
                "FROM trust "
                "WHERE giver=%s AND receiver=%s")
 
            cursor.execute(check_if_trusted, (session["user"], commentInfo[1]))

            isTrusted = (cursor.rowcount != 0)
            if isTrusted:
                trust_update = (
                    "UPDATE trust "
                    "SET isTrusted=%s "
                    "WHERE giver=%s AND receiver=%s")

                cursor.execute(trust_update, (request.form["isTrust"] == "True", session["user"], commentInfo[1]))

            else:
                trust_insert = (
                    "INSERT INTO trust "
                    "VALUES (%s, %s, %s)")

                cursor.execute(trust_insert, (session["user"], commentInfo[1], request.form["isTrust"] == "True"))

            flash("This user has been labled as: " 
                + ("Trusted" if request.form["isTrust"] == "True" else "Not-trusted"))

        
        if "usefulRating" not in request.form and "isTrust" not in request.form:
            flash("Please provide the trust label or usefulness rating first")
            return render_template("comment.html", values=commentInfo, userInfo=user_info, 
                                                trustcount=trustCount_dic, otherComment=otherComment_list)
        
        db.commit()
        cursor.close()

        return render_template("comment.html", values=commentInfo, userInfo=user_info, 
                                            trustcount=trustCount_dic, otherComment=otherComment_list)
    else:
        return render_template("comment.html", values=commentInfo, userInfo=user_info, 
                                            trustcount=trustCount_dic, otherComment=otherComment_list)


@app.route("/addBook", methods=["POST", "GET"])
def addBook():
    # Customer don't have access to this page
    if "ism" not in session or session["ism"] != True:
        flash("You don't have access to this page")
        return redirect(url_for("home"))

    if request.method == "POST":
        ISBN = title = pub = lang = pubDate = \
        nop = stock = disc = price = author = genre = ""
        if "ISBN" in request.form:
            ISBN = request.form["ISBN"]
        if "title" in request.form:
            title = request.form["title"]
        if "pub" in request.form:
            pub = request.form["pub"]
        if "lang" in request.form:
            lang = request.form["lang"]
        if "pubDate" in request.form:
            pubDate = request.form["pubDate"]
        if "nop" in request.form:
            nop = request.form["nop"]
        if "stock" in request.form:
            stock = request.form["stock"]
        if "disc" in request.form:
            disc = request.form["disc"]
        if "price" in request.form:
            price = request.form["price"]
        if "author" in request.form:
            author = request.form["author"]
        if "genre" in request.form:
            genre = request.form["genre"]

        # if all entries are not empty
        if ISBN and title and pub and \
            lang and pubDate and nop and \
            stock and disc and price and \
            author and genre:

            cursor = db.cursor(buffered=True)

            # Insert into the book table
            book_insert = (
                "INSERT INTO Book "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")

            cursor.execute(book_insert, (ISBN, title, pub, lang, pubDate, nop, stock, disc, price))

            # Insert keywords, if exist
            if "kword" in request.form:
                kword_list = request.form["kword"].split(',')
                for i in range(len(kword_list)):
                    kword_list[i] = (ISBN, kword_list[i])

                kword_insert = (
                    "INSERT INTO has "
                    "VALUES (%s, %s)")

                cursor.executemany(kword_insert, kword_list)

            # Insert genres
            genre_list = genre.split(',')
            for i in range(len(genre_list)):
                genre_list[i] = (ISBN, genre_list[i])

            genre_insert = (
                "INSERT INTO classifiedAs "
                "VALUES (%s, %s)")

            cursor.executemany(genre_insert, genre_list)

            # Insert authors
            author_list = author.split(',')
            author_insert = (
                "INSERT INTO Author(Name) "
                "VALUES (%s)")

            authorship_insert = (
                "INSERT INTO authorship "
                "VALUES (%s, %s)")

            autID_list = []
            for aut in author_list:
                cursor.execute(author_insert, (aut,))
                autID = cursor.lastrowid
                autID_list.append(autID)
                cursor.execute(authorship_insert, (ISBN, autID))

            # Update the separation table
            separation_insert = (
                "INSERT INTO separation "
                "VALUES (%s, %s)")

            for id1 in autID_list:
                for id2 in autID_list:
                    if id1 != id2:
                        cursor.execute(separation_insert, (id1, id2))

            db.commit()
            cursor.close()
            flash("This book has been added!")
        else:
            flash("All entries need to be filled")

        return render_template("addBook.html")

    else:
        return render_template("addBook.html")

@app.route("/changeStock", methods=["POST", "GET"])
def changeStock():

    if "ism" not in session or session["ism"] != True:
        flash("You don't have access to this page")
        return redirect(url_for("home"))

    if request.method == "POST":
        ISBN = delta = ""
        if "ISBN" in request.form:
            ISBN = request.form["ISBN"]
        if "delta" in request.form:
            delta = request.form["delta"]

        if ISBN and delta:
            cursor = db.cursor(buffered=True)

            change_stock = (
                "UPDATE Book "
                "SET stockLevel=stockLevel+%s "
                "WHERE ISBN=%s")

            cursor.execute(change_stock, (int(delta), ISBN))

            db.commit()
            cursor.close()
            flash("Stock level change commited!")
        else:
            flash("All entries need to be filled")

        return render_template("changeStock.html")
    else:
        return render_template("changeStock.html")

@app.route("/addDiscount", methods=["POST", "GET"])
def addDiscount():
    if "ism" not in session or session["ism"] != True:
        flash("You don't have access to this page")
        return redirect(url_for("home"))

    if request.method == "POST":
        ISBN = disc = ""
        if "ISBN" in request.form:
            ISBN = request.form["ISBN"]
        if "disc" in request.form:
            disc = request.form["disc"]

        if ISBN and disc:
            cursor = db.cursor(buffered=True)

            change_discount = (
                "UPDATE Book "
                "SET discountPercentage=%s "
                "WHERE ISBN=%s")

            cursor.execute(change_discount, (float(disc), ISBN))

            db.commit()
            cursor.close()
            flash("Discount percentage change committed!")
        else:
            flash("All entries need to be filled")

        return render_template("addDiscount.html")
    else:
        return render_template("addDiscount.html")


@app.route("/bookStat", methods=["POST", "GET"])
def bookStat():
    if "ism" not in session or session["ism"] != True:
        flash("You don't have access to this page")
        return redirect(url_for("home"))

    if request.method == "POST":
        if "m" not in request.form:
            flash("Please enter m, the number of output you need")
            return render_template("bookStat.html")

        cursor = db.cursor(buffered=True)

        # decide today's quarter (start from 0)
        quarterNum = (date.today().month - 1) // 3

        thisYear = date.today().year
        if quarterNum == 0:
            interval = (date(thisYear, 1, 1), date(thisYear, 3, 31))
        elif quarterNum == 1:
            interval = (date(thisYear, 4, 1), date(thisYear, 6, 30))
        elif quarterNum == 2:
            interval = (date(thisYear, 7, 1), date(thisYear, 9, 30))
        else:
            interval = (date(thisYear, 10, 1), date(thisYear, 12, 31))

        # Find most popular Books
        popBook_query = (
            "SELECT ISBN, SUM(quantity) "
            "FROM OrderTable NATURAL JOIN include "
            "WHERE orderDate BETWEEN DATE(%s) AND DATE(%s) "
            "GROUP BY ISBN "
            "ORDER BY SUM(quantity) DESC "
            "LIMIT %s")

        cursor.execute(popBook_query, interval + (int(request.form["m"]),))

        popBook_result = []
        for row in cursor:
            popBook_result.append(row)

        # Find most popular authors
        popAuthor_query = (
            "SELECT Name, SUM(quantity) "
            "FROM OrderTable NATURAL JOIN include "
            "NATURAL JOIN authorship NATURAL JOIN Author "
            "WHERE orderDate BETWEEN DATE(%s) AND DATE(%s) "
            "GROUP BY Name, authorID "
            "ORDER BY SUM(quantity) DESC "
            "LIMIT %s")

        cursor.execute(popAuthor_query, interval + (int(request.form["m"]),))

        popAuthor_result = []
        for row in cursor:
            popAuthor_result.append(row)

        # Find most poopular publisher
        popPub_query = (
            "SELECT publisher, SUM(quantity) "
            "FROM OrderTable NATURAL JOIN include NATURAL JOIN Book "
            "WHERE orderDate BETWEEN DATE(%s) AND DATE(%s) "
            "GROUP BY publisher "
            "ORDER BY SUM(quantity) DESC "
            "LIMIT %s")

        cursor.execute(popPub_query, interval + (int(request.form["m"]),))

        popPub_result = []
        for row in cursor:
            popPub_result.append(row)

        cursor.close()
        return render_template("bookStat.html", popBook=popBook_result,
                                popAuthor=popAuthor_result, popPub=popPub_result)

    else:
        return render_template("bookStat.html")


@app.route("/userStat", methods=["POST", "GET"])
def userStat():
    if "ism" not in session or session["ism"] != True:
        flash("You don't have access to this page")
        return redirect(url_for("home"))

    if request.method == "POST":
        if "m" not in request.form:
            flash("Please enter m, the number of output you need")
            return render_template("userStat.html")

        cursor = db.cursor(buffered=True)
        cursor2 = db.cursor(buffered=True)

        # Get the top m most trusted users
        # Create temporary table for trust count
        create_tmp_tc = (
            "CREATE TEMPORARY TABLE TrustCount ("
            "loginName VARCHAR(30), "
            "trustCount INT DEFAULT 0, "
            "PRIMARY KEY (loginName))")

        # Insert all users
        user_insert = (
            "INSERT INTO TrustCount (loginName) "
            "SELECT loginName "
            "FROM Customer")

        cursor.execute(create_tmp_tc)
        cursor.execute(user_insert)

        # Add trust count
        trustCount_query = (
            "SELECT receiver, COUNT(*) "
            "FROM trust "
            "WHERE isTrusted=True "
            "GROUP BY receiver")

        cursor.execute(trustCount_query)

        update_trustCount = (
            "UPDATE TrustCount "
            "SET trustCount=trustCount+%s "
            "WHERE loginName=%s")

        for row in cursor:
            cursor2.execute(update_trustCount, (int(row[1]), row[0]))

        # Reduce distrust count
        distrustCount_query = (
            "SELECT receiver, COUNT(*) "
            "FROM trust "
            "WHERE isTrusted=False "
            "GROUP BY receiver")

        cursor.execute(distrustCount_query)

        update_distrustCount = (
            "UPDATE TrustCount "
            "SET trustCount=trustCount-%s "
            "WHERE loginName=%s")

        for row in cursor:
            cursor2.execute(update_distrustCount, (int(row[1]), row[0]))

        # Find the top m most trusted users
        mostTrusted_query = (
            "SELECT loginName, trustCount "
            "FROM TrustCount "
            "ORDER BY trustCount DESC "
            "LIMIT %s")

        cursor.execute(mostTrusted_query, (int(request.form["m"]),))

        mostTrusted_result = []
        for row in cursor:
            mostTrusted_result.append(row)

        cursor.execute("DROP TEMPORARY TABLE TrustCount")

        # Get the top m most trusted users
        # Create temporary table for trust count
        create_tmp_us = (
            "CREATE TEMPORARY TABLE usefulScore ("
            "loginName VARCHAR(30), "
            "score INT DEFAULT 0, "
            "PRIMARY KEY (loginName))")

        # Insert all users
        user_insert = (
            "INSERT INTO usefulScore (loginName) "
            "SELECT loginName "
            "FROM Customer")

        cursor.execute(create_tmp_us)
        cursor.execute(user_insert)

        # Add very useful count
        vuCount_query = (
            "SELECT commentGiver, COUNT(*) "
            "FROM giveUsefulnessRating "
            "WHERE score='very useful' "
            "GROUP BY commentGiver")

        cursor.execute(vuCount_query)

        update_veryUseful = (
            "UPDATE usefulScore "
            "SET score=score+2*%s "
            "WHERE loginName=%s")

        for row in cursor:
            cursor2.execute(update_veryUseful, (int(row[1]), row[0]))

        # Add useful count
        uCount_query = (
            "SELECT commentGiver, COUNT(*) "
            "FROM giveUsefulnessRating "
            "WHERE score='useful' "
            "GROUP BY commentGiver")

        cursor.execute(uCount_query)

        update_useful = (
            "UPDATE usefulScore "
            "SET score=score+%s "
            "WHERE loginName=%s")

        for row in cursor:
            cursor2.execute(update_useful, (int(row[1]), row[0]))

        # Add useless count
        ulCount_query = (
            "SELECT commentGiver, COUNT(*) "
            "FROM giveUsefulnessRating "
            "WHERE score='useless' "
            "GROUP BY commentGiver")

        cursor.execute(ulCount_query)

        update_useless = (
            "UPDATE usefulScore "
            "SET score=score-%s "
            "WHERE loginName=%s")

        for row in cursor:
            cursor2.execute(update_useless, (int(row[1]), row[0]))

        # Find the top m most trusted users
        mostUseful_query = (
            "SELECT loginName, score "
            "FROM usefulScore "
            "ORDER BY score DESC "
            "LIMIT %s")

        cursor.execute(mostUseful_query, (int(request.form["m"]),))

        mostUseful_result = []
        for row in cursor:
            mostUseful_result.append(row)

        cursor.execute("DROP TEMPORARY TABLE usefulScore")

        cursor.close()
        cursor2.close()

        return render_template("userStat.html", mostTrusted=mostTrusted_result, mostUseful=mostUseful_result)

    else:
        return render_template("userStat.html")

@app.route("/separation", methods=["POST", "GET"])
def separation():
    if request.method == "POST":
        if "author" not in request.form:
            flash("please fill in m value first")
            return render_template("separation.html")

        author_query = (
            "SELECT Name, authorID "
            "FROM Author "
            "WHERE Name LIKE %s")

        cursor = db.cursor(buffered=True)
        cursor2 = db.cursor(buffered=True)

        # Fetch author information
        cursor.execute(author_query, ("%" + request.form["author"] + "%",))
        authorName, authorID = cursor.fetchone()

        # Find 1-degree separation books
        oneDS_query = (
            "SELECT ISBN, title "
            "FROM (separation JOIN authorship ON secondAuthorID = authorID) NATURAL JOIN Book "
            "WHERE firstAuthorID=%s "
            "LIMIT 20")

        cursor.execute(oneDS_query, (authorID,))

        oneDS_result = []
        for row in cursor:
            oneDS_result.append(row)

        # Find 2-degree separation books
        twoDS_query = (
            "SELECT S2.secondAuthorID "
            "FROM separation S1 JOIN separation S2 ON S1.secondAuthorID = S2.firstAuthorID "
            "WHERE S1.firstAuthorID=%s AND S2.secondAuthorID!=S1.firstAuthorID AND "
            "S2.secondAuthorID NOT IN "
                "(SELECT secondAuthorID "
                "FROM separation "
                "WHERE firstAuthorID=%s)")

        cursor.execute(twoDS_query, (authorID, authorID))

        book_query = (
            "SELECT ISBN, title "
            "FROM authorship NATURAL JOIN Book "
            "WHERE authorID=%s")

        twoDS_result = []
        for author in cursor:
            cursor2.execute(book_query, author)
            for book in cursor2:
                twoDS_result.append(book)
                if len(twoDS_result) == 20: break

        cursor.close()
        cursor2.close()

        return render_template("separation.html", oneDS=oneDS_result, twoDS=twoDS_result)

    else:
        return render_template("separation.html")

@app.route("/manager")
def manager():
    if "ism" not in session or session["ism"] != True:
        flash("You don't have access to this page")
        return redirect(url_for("home"))

    return render_template("manager.html")