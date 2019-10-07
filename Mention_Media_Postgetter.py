from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import base64
import time

#needed variables
urlTarget = input("enter username: ")
baseURL = "https://www.instagram.com/"
userURL = baseURL + urlTarget +"/?__a=1"
postURL = ""
targetUserCommentID = input("enter comment: ")


#post ID to shortcode conversion
def base10_to_base64(num):
    order = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";
    short = "";
    base = len(order)
    while num != 0:
        num, remainder = divmod(num, base);

        short = str(order[remainder]) + short

    return short;

#shortcode to ID conversion
def base64_to_base10(shortcode):
    code = ('' * (12 - len(shortcode))) + shortcode
    print(code)
    return int.from_bytes(base64.b64decode((code + "==").encode(), "-_"), "big")

#gets html of new link
def info_getter(url):
    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser");
    return soup.extract()

#loop to iterate through all user posts
def querying(userID,posts,captions,end_cursor):
    try:
        print(end_cursor)


        for post in range(0, len(posts)):
            if len(end_cursor) != 0 and (len(posts) - 1) == post:

                userURL = baseURL + "graphql/query/?query_id=17888483320059182&id="+str(captions[0])+"&first=50"+"&after="\
                          +str(end_cursor[0])

                userpageINFO = info_getter(userURL)

                posts = re.findall(mediaRegex, str(userpageINFO))
                #mediaID = re.findall(mediaRegex, str(userpageINFO))
                captions = re.findall(captionRegex, str(userpageINFO))
                end_cursor = re.findall(end_cursorRegex, str(userpageINFO))
                querying(userID,posts,captions,end_cursor)


            elif (targetUserCommentID in str(captions[post])):
                print(captions[post])

                postURL = baseURL + "p/" + str(base10_to_base64(int(posts[post]))) + "/"
                print("mention media post URL: " + postURL)
                break

    except(IndexError):
        print("error")

##########################################################################

userpageINFO = info_getter(userURL)

userIDRegex = "\"owner\":{\"id\":\"(\d+?)\","
mediaRegex = "Graph\w+\",\"id\":\"(\d+)\",\""
captionRegex = "\"text\":\"(.+?)\"}"
end_cursorRegex="\"end_cursor\":\"(.+?)\"}"

userID = re.findall(userIDRegex, str(userpageINFO))
mediaID = re.findall(mediaRegex, str(userpageINFO))
captions = re.findall(captionRegex, str(userpageINFO))
posts = re.findall(mediaRegex, str(userpageINFO))

userURL = baseURL+"graphql/query/?query_id=17888483320059182&id="+str(userID[0])+"&first=50"

#update regex format
mediaRegex = "{\"id\":\"(\d+?)\",\"__typename\":\"Graph\w+?\""

userpageINFO = info_getter(userURL)

posts = re.findall(mediaRegex, str(userpageINFO))
mediaID = re.findall(mediaRegex, str(userpageINFO))
captions = re.findall(captionRegex, str(userpageINFO))
end_cursor = re.findall(end_cursorRegex, str(userpageINFO))

start = time.time()
querying(userID,posts,captions,end_cursor);
end = time.time()
elapsed = end - start

print("")
print("Total elapsed time: " + str(elapsed) + " seconds");

