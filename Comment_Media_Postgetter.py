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

urlTarget = "bugatti"
baseURL = "https://www.instagram.com/"
userURL = baseURL + urlTarget +"/?__a=1"
postURL = ""
targetUser="behzad_fitness_"
targetCommentID="17855803483567274"

html = urlopen(userURL)
soup = BeautifulSoup(html, "html.parser");
postShortcodes = soup.extract()

mediaRegex = "Graph\w+\",\"id\":\"(\d+)\",\""
targetUserRegex = "\"("+targetUser+")\""
targetCommentIDRegex = "\"("+targetCommentID+")\""



posts = re.findall(mediaRegex, str(postShortcodes))
start = time.time()
for post in range(0,len(posts)):

    postURL = baseURL + "p/" + base10_to_base64(int(posts[post])) + "?__a=1"
    html = urlopen(postURL)
    soup = BeautifulSoup(html, "html.parser");
    postContent = soup.extract()

    foundUser = re.findall(targetUserRegex, str(postContent))
    foundCommentID = re.findall(targetCommentIDRegex, str(postContent))

    if (len(foundUser) + len(foundCommentID)) == 2:
        print(foundUser)
        print(foundCommentID)

        if ((foundUser[0] == targetUser) and (foundCommentID[0] == targetCommentID)):
            print("comment post URL: https://www.instagram.com/p/" + str(base10_to_base64(int(posts[post])))+"/")
            break

end = time.time()

elapsed = end - start

print("")
print("Total elapsed time: "+str(elapsed));