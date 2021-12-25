How to deploy? (Windows)

1. Open the command prompt
2. enter the directory (Bookstore_Project)
3. Activate the virtual environment:
>>> venv\Scripts\activate
4. Set the entrance of the application
>>> set FLASK_APP=FlaskCore.py
5. Run the application
>>> flask run
6. You should see a prompt "Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)"
Now copy and paste the url into the browser and you should be able to use it just like
any other websites.

Database Setup:
If you already have MySQL Python Connector downloaded
and installed, change the db = mysql.connector.connect
on top of the FlaskCore.py to connect to an existing
MySQL account.

Database Schema Setup:
Open the dbSetUP.py. Uncomment all codes and run the script. 

Data Population:
Run the dataPopulation.py to parse the data in book.csv
into the database and create first manager. 

How to use different functionalities?

1. Customer Registration
On the navigation bar, click the Sign-up button. 
Fill in all the entries and click login.

2. Multiple Managers
(a) Login as a manager
On the navigation bar, click the login button.
The interface for manager login and user login
is exactly the same. Just fill in all entries 
and click "Login"
(b) register for a new manager
Once login, choose the "manager" tab on navigation
bar. Then you should see a block with title "create
manager accounts". Use the block to go to the manager
sign-up page.

Also, the login information for super user is:
Origin, 123456

3. Ordering
In general, there are two steps for ordering.
First, enter a book page by url or clicking the
link in book browsing page. Add the desired quantity
to you shopping cart. Next, click the "shopping
cart" tab on navigation bar, enter the shopping cart,
and click "place order" to order everything in the
shopping cart. If you want to change books' quantity 
in the shopping cart, simply add the book
into the shopping cart again with the desired 
quantity. The new value will overwrite the old
value.

4. New book
Once sign in as a manager, click manager tab on
navigation bar, and use the "Add new books" block
to access this functionality.

5. Arrivals of more copies
Once sign in as a manager, click manager tab on
navigation bar, and use the "Arrivals of more copies" block
to access this functionality.

6. Comments
Enter a book page, scroll down to "your comment"
section. If it's empty, that means you haven't leave
a comment yet. You can write down you score and comment
message and click submit. If it's not empty,
it will show the comment you put before. You can simply 
edit it and hit submit again to update your comment.
You can also see other user's comment in a book page.

7. Usefulness Rating
When you see a comment, click it to enter the comment page.
In this page you can see more detailed information about
this comment as well as the user who gives this comment.
You can give it a usefulness rating and give the
user who wrote this comment a trust or distrust label.

8. Trust Recording
When you see a comment, click it to enter the comment page.
In this page you can see more detailed information about
this comment, give it a usefulness rating, and give the
user who wrote this comment a trust or distrust label.

9. Book Browsing
On navigation bar, choose "Search tab". Type in your search
keyword and preferred order, hit "Apply Filter". You should 
see a list of results (at most 80). If you don't find the
book you are looking for, simply type more search keywords
to narrow down the search result. Click each search result
to enter the corresponding book page. Notice that sorted by
average numerical score and by average numerical score from
trusted users is not implemented.

10. Useful Comment
In a book page's other users' comment section, you can
type in the desired n value and click OK button to view
the top n most useful comments

11. Buying suggestions
When enter a bookpage, there is a "Other user also buy"
section, which gives you the buying suggestions

12. Degrees of separation
On navigation bar, click the "separation search"
tab to enter the page.

13. Book Statistics
Once sign in as a manager, click manager tab on
navigation bar, and use the "Book Stat" block
to access this functionality.

14. User Awards
Once sign in as a manager, click manager tab on
navigation bar, and use the "User Stat" block
to access this functionality.

Additional functionalities
---------------------------------------------------

15. Change Discount Percentage
Once sign in as a manager, click manager tab on
navigation bar, and use the "Add discount" block
to access this functionality.

16. Check Lowest Price in History
In the book Page, right next to the price, you
can see "(lowest: xx.xx)", which is the lowest price
in history. Notice that a lowest price is only recorded
when someone buy this product at this price. If it drops
to a low point but no one bought it, then it doesn't
count.

17. Show Discounted Books Only
In the book browsing page, there is a check box called
"Only show books with discount". Click that before
hitting "Apply Filter", the search result should only
contain discounted Books.
