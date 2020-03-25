import requests
import re
import os

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


def parsePage(itemList, html):
    try:
        p = r'<img src="([^"]+t\.jpg)"'
        img_address = re.findall(p, html)
        for i in range(len(img_address)):
            itemList.append(img_address[i])
    except:
        print("")


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
    dirName = '并非我的恋人'
    imgList = []
    html = getHTMLText(url)
    parsePage(imgList, html)
    saveImg(imgList, dirName)


if __name__ == '__main__':
    main()