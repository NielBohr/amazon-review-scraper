from splinter import Browser
import time
import requests
import csv
import re
from datetime import datetime
import os
import random
import shutil

def captcha():
    try:
        element = browser.find_by_css('.a-last')
        if "Sorry" in element.text:
            return True
        else:
            return False
    except:
        return False

def nextpagebutton():
    next_page_button = browser.find_by_css('li.a-last a')

    # Click the button if found
    if next_page_button:
        return next_page_button
    else:
        return False
def searchsingle(start,end,content):
    try:
        if end != "" and start != "":
            pattern = re.compile(f'{re.escape(start)}(.*?){re.escape(end)}', re.DOTALL)
        elif end == "":
            pattern = re.compile(f'{re.escape(start) + r'\s*(.*)'}')
        elif start == "":
            pattern = re.compile(f'{r'^(.*?)' + re.escape(end)}')
        result=re.search(pattern, content).group(1)
        return result
    except:
        raise Exception("line not found")
def searchmultiple(start,end,content):
    if end != "" and start != "":
        pattern = re.compile(f'{re.escape(start)}(.*?){re.escape(end)}', re.DOTALL)
    elif end == "":
        pattern = re.compile(f'{re.escape(start) + r'\s*(.*)'}')
    elif start=="":
        pattern = re.compile(f'{r'^(.*?)' + re.escape(end)}')
    matches = pattern.findall(content)
    result = {}
    reslist=[]
    for i, match in enumerate(matches, 0):
        result[i] = match
    for i in result.values():
        reslist.append(i)
    return reslist
def writehtml(html,title):
    # Write HTML content to file
    with open(os.path.join('cache',title+".txt"), "w", errors="ignore",encoding="utf-8") as fp:
        fp.write(html)
    print("Great!")
#Input: string
#ourput: string
#Use: read and return the content of a file named input
def readhtml(title):
    with open(os.path.join('cache',title+'.txt'),"r",encoding="utf-8") as fp:
        content=fp.read()
    return content

#Input: string of title, dictionary of information, list of keys
#Output: None
#Use: append the information to a csv named of string of title
def append_csv(title, information,keys):
    with open(title, "a", encoding="utf_8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=keys)
        writer.writerows(information)

def products(url, browser):
    browser.visit(url)
    while captcha():
        time.sleep(10)
    html=browser.html
    productlist=searchmultiple('<a class="a-link-normal s-no-outline" tabindex="-1" href="','">',html)
    for i in range(0,len(productlist)):
        productlist[i]="https://www.amazon.com"+productlist[i]
    return productlist



def comment(url,browser,index):
    #browser = Browser('chrome')
    #url = "https://www.amazon.com/Discourse-Method-Meditations-First-Philosophy/product-reviews/0872204200/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
    browser.visit(url)
    while captcha():
        time.sleep(10)
    i=0
    html=browser.html
    writehtml(html,str(index)+'comment'+str(i))
    i+=1
    while True:
        try:
            new_url=searchsingle('<link rel="next" href="','">',html)
            browser.visit(new_url)
            time.sleep(random.uniform(0.5,1))
            while captcha():
                time.sleep(10)
            html=browser.html
            writehtml(html,str(index)+'comment'+str(i))
            i+=1
        except:
            break
    return i

def commentmining(index, pagenumber):
    allcomment=[]
    for i in range(0,pagenumber):
        try:
            commenthtml=readhtml(str(index)+'comment'+str(i))
            comments=searchmultiple('-review-card" class="a-row a-spacing-none">','<div class="a-row review-comments comments-for',commenthtml)
        except:
            print("Comment not got")
            continue
        for i in range(0,len(comments)):
            productcomment={}
            try:
                commentstitle=searchsingle('<span class="a-letter-space"></span>','</a>',comments[i])
                titlewash=["\n",'<span class="cr-original-review-content">','</span><span class="cr-translated-review-content aok-hidden"></span>','']
                for a in titlewash:
                    commentstitle=commentstitle.replace(a,"")
            except:
                commentstitle=''
                print('Title not get')
            try:
                commentsrating=searchsingle('review-rating"><span class="a-icon-alt">','</span>',comments[i])

            except:
                commentsrating=''
                print('Rating not get')
            try:
                commentsbody=searchsingle('<span data-hook="review-body" class="a-size-base review-text review-text-content">','</span>',comments[i])
                bodywash = ["\n", '<span class="cr-original-review-content">','<br>',"</br>"]
                for b in bodywash:
                   commentsbody=commentsbody.replace(b,"")
            except:
                commentsbody=''
                print('Body not get')
            try:
                commentsdate=searchsingle('<span data-hook="review-date" class="a-size-base a-color-secondary review-date">','</span>',comments[i])
            except:
                commentsdate=''
                print('Date not get')
            productcomment['id']=index
            productcomment['Comments-Title']=commentstitle.lstrip()
            productcomment['Comments-Rating']=commentsrating
            productcomment['Comments-Body']=commentsbody.lstrip()
            productcomment['Comments-Date']=commentsdate
            allcomment.append(productcomment)
    return allcomment

def information(index,url,browser):
    browser.visit(url)
    while captcha():
        time.sleep(10)
    html=browser.html
    writehtml(html,str(index)+'information')
    return html

def informationmining(index):
    information={}
    html=readhtml(str(index)+'information')
    try:
        name = searchsingle('<meta name="title" content="', '"/>', html)
    except:
        print("Name not got")
        name=''
    try:
        rating = searchsingle('class="reviewCountTextLinkedHistogram noUnderline" title="', '">', html)
    except:
        print("Rating not get")
        rating=''
    try:
        price = searchsingle('<span class="a-offscreen">US$', '</span>', html)
    except:
        print("Price not get")
        price=''
    information['id']=index
    information['Name'] = name
    information['Rating'] = rating
    information['price'] = price
    return information


if os.path.exists('cache'):
    shutil.rmtree('cache')
os.makedirs('cache',exist_ok=True)
productlist=[]
browser = Browser('chrome')
browser.visit('https://www.amazon.com')

while True:
    url=str(browser.url)
    if 's?k=' in url:
        productlist=products(url,browser)
        listlength=len(productlist)
        if listlength>48:
            continue
        else:
            break
        print(listlength)


pagenumbers=[]
for i in range(0, listlength):
    try:
        html=information(i,productlist[i],browser)
        commenturl=searchsingle('<a data-hook="see-all-reviews-link-foot" class="a-link-emphasis a-text-bold" href="','">',html)
        index=comment('https://www.amazon.com'+commenturl, browser,i)
        pagenumbers.append(index)
    except:
        pagenumbers.append(0)
        continue

print(pagenumbers)

listlength=48
commentkey=['id','Comments-Title','Comments-Rating','Comments-Body','Comments-Date']
allcomment=[]
allinformation=[]
keys=[]
for i in range(0,listlength):
    try:
        allinformation.append(informationmining(i))
        allcomment+=commentmining(i,int(pagenumbers[i]))
    except:
        continue
for i in allinformation:
    for a in i.keys():
        if a not in keys:
            keys.append(a)
keyword=input("What is your keyword?: ")
with open(keyword+"Product.csv", "w", encoding="utf-8", newline="") as fp:
    writer = csv.DictWriter(fp, fieldnames=keys)
    writer.writeheader()
append_csv(keyword+"Product.csv",allinformation,keys)
with open(keyword+"Comment.csv", "w", encoding="utf-8", newline="") as fp:
    writer = csv.DictWriter(fp, fieldnames=commentkey)
    writer.writeheader()
append_csv(keyword+"Comment.csv",allcomment,commentkey)
browser.quit()
