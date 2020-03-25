import requests
import re
import os
from bs4 import BeautifulSoup

def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.text
    except:
        return ""


def getHTMLResponse(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r
    except:
        return ""


#改用bs4解析找href 拼接一下，再把所有的url存起来
def parsePageFirst(hrefList, html, url):
    soup = BeautifulSoup(html, "html.parser")
    hlist = soup.find_all("a", class_= "gallerythumb")
    for x in hlist:
        hrefList.append(url + x.get('href'))


def parsePage(itemList, html):
    try:
        p = r'<img src="([^"]+\.jpg)"'
        img_address = re.findall(p, html)
        itemList.append(img_address[0])
    except:
        print("")


def parsePageSecond(imgList, hrefList):
    for i in hrefList:
        html = getHTMLText(i)
        parsePage(imgList, html)


def saveImg(itemList, dirName):
    x = 1000
    dirPath = 'C:\\'+dirName
    os.mkdir(dirPath)
    os.chdir(dirPath)
    for i in itemList:
        filename = str(x) + ".jpg"
        x = x+1
        with open(filename, 'wb') as f:
            img = getHTMLResponse(i).content
            f.write(img)


def main():
    url = 'https://nhentai.net/g/231690/'
    url_home = 'https://nhentai.net'
    dirName = '并非我的恋人大图'
    hrefList = []
    imgList = []
    html = getHTMLText(url)
    parsePageFirst(hrefList, html, url_home)
    parsePageSecond(imgList, hrefList)
    print(imgList)
    saveImg(imgList, dirName)


if __name__ == '__main__':
    main()