from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import base64
import time
from datetime import datetime

#needed variables:

#regex
timestampRegex = "timestamp\": \"(.+?)\""
usernameRegex = "username\": \"(.+?)\""
userIDRegex = "\"owner\":{\"id\":\"(\d+?)\","
mediaRegex = "Graph\w+\",\"id\":\"(\d+)\",\""
end_cursorRegex="\"end_cursor\":\"(.+?)\"}"

#parsed JSON input
json = input("paste in JSON: \n===========================================================\n")

#convert publish date to timestamp
timestamp = re.findall(timestampRegex, json)
timestamp = int(datetime.strptime(timestamp[0], "%Y-%m-%dT%H:%M:%S%z").timestamp())

urlTarget = re.findall(usernameRegex, json)

baseURL = "https://www.instagram.com/"
userURL = baseURL + urlTarget[0] +"/?__a=1"
postURL = ""

steps =0


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
def querying(userID,posts,timestamps,end_cursor):
    try:

        for post in range(0, len(posts)):
            if len(end_cursor) != 0 and (len(posts) - 1) == post:

                userURL = baseURL + "graphql/query/?query_id=17888483320059182&id="+str(userID[0])+"&first=50"+"&after="\
                          +str(end_cursor[0])

                userpageINFO = info_getter(userURL)

                posts = re.findall(mediaRegex, str(userpageINFO))
                #mediaID = re.findall(mediaRegex, str(userpageINFO))
                timestamps = re.findall(timestampRegex, str(userpageINFO))
                end_cursor = re.findall(end_cursorRegex, str(userpageINFO))
                querying(userID,posts,timestamps,end_cursor)


            elif (str(timestamp) == str(timestamps[post])):

                postURL = baseURL + "p/" + str(base10_to_base64(int(posts[post]))) + "/"
                print("mention media post URL: " + postURL)
                break

    except(IndexError):
        print("error")

##########################################################################

#new content
userpageINFO = info_getter(userURL)

#update regex
timestampRegex = "timestamp\":(.+?),\""

userID = re.findall(userIDRegex, str(userpageINFO))
mediaID = re.findall(mediaRegex, str(userpageINFO))
timestamps = re.findall(timestampRegex, str(userpageINFO))
posts = re.findall(mediaRegex, str(userpageINFO))

userURL = baseURL+"graphql/query/?query_id=17888483320059182&id="+str(userID[0])+"&first=50"

#update regex format
mediaRegex = "{\"id\":\"(\d+?)\",\"__typename\":\"Graph\w+?\""

#new content
userpageINFO = info_getter(userURL)

posts = re.findall(mediaRegex, str(userpageINFO))
mediaID = re.findall(mediaRegex, str(userpageINFO))
timestamps = re.findall(timestampRegex, str(userpageINFO))
end_cursor = re.findall(end_cursorRegex, str(userpageINFO))

start = time.time()
querying(userID,posts,timestamps,end_cursor);
end = time.time()
elapsed = end - start

print("")
print("Total elapsed time: " + str(elapsed) + " seconds");

