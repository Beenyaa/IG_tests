from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import base64
import time


def base10_to_base64(num):
    order = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";
    short = "";
    base = len(order)
    while num != 0:
        num, remainder = divmod(num, base);

        short = str(order[remainder]) + short

    return short;


def base64_to_base10(shortcode):
    code = ('' * (12 - len(shortcode))) + shortcode
    print(code)
    return int.from_bytes(base64.b64decode((code + "==").encode(), "-_"), "big")

urlTarget = "bboyjohnny"
baseURL = "https://www.instagram.com/"
userURL = baseURL + urlTarget +"/?__a=1"
postURL = ""
targetUserComment = "I don't remeber when i felt so freely at such a big event. See you next year"


html = urlopen(userURL)
soup = BeautifulSoup(html, "html.parser");
userpageINFO = soup.extract()

userIDRegex = "\"owner\":{\"id\":\"(\d+?)\","
mediaRegex = "Graph\w+\",\"id\":\"(\d+)\",\""
captionRegex = "\"text\":\"(.+?)\"}"

userID = re.findall(userIDRegex, str(userpageINFO))
captions = re.findall(captionRegex, str(userpageINFO))
posts = re.findall(mediaRegex, str(userpageINFO))

userURL = baseURL + "/graphql/query/?query_id=17888483320059182&id="+str(userID[0])+"&first=50"

html = urlopen(userURL)
soup = BeautifulSoup(html, "html.parser");
userpageINFO = soup.extract()

start = time.time()
for post in range(0,len(posts)):

    if (targetUserComment in str(captions[post])):
        postURL=baseURL+"p/"+str(base10_to_base64(int(posts[post])))+"/"
        print("mention media post URL: " +postURL)


end = time.time()

elapsed = end - start

print("")
print("Total elapsed time: "+str(elapsed));
