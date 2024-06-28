# amazon-review-scraper
The scraper program build on Python to get all reviews under all products of a search keyword. Use chrome to work

Tips:
Please make sure your computer has Chrome since this scrapper need chrome to work.
The program will create a folder name 'cache' that contains html of scrapped websites.

This is a scrapper of reviews on amazon.com based on Python, which is not allowed by Amazon API. It will output two tables. One with the information of the products. One with the comment of the products. Two tables are connected with a column named "id".

Output:

A csv file of "keyword + Product.csv", which includes keys of [id, Name, Rating, Price] 
A csv file of "your_title + Comment.csv", which includes keys of [id, Comments-Title, Comments-Rating, Comments-Body, Comments-Date] 

How to use:
Make sure your computer has Chrome.
Download the file and unzip it
Run the "amazon.py" file
It will open the amazon website. It might have a captcha. Just solve it manually.
Type your keyword in the search bar and hit enter.
Once the search page appears, the scrapper will start working. Wait until it complete.
Then it will ask you about your keyword to use for title of the file. Enter your keyword.
Finally, it will appear two files: "keyword+Product.csv" and "keyword+Comment.csv"

Based on how many comments are there in your search, it might take 5 to 15 minutes to complete. The wait is long but what you get is worth it.

Future to do: Formalize this Project to let people use pip install to use
