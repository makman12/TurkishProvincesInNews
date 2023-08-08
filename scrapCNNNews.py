import requests
import json
import bs4
import concurrent.futures as cf

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}

# read CNNLinks.json
with open("CNNLinks.json", "r") as f:
    dataLinks=json.load(f)

def scrapNews(link):
    # get l1
    res=requests.get(link, headers=headers)
    soup=bs4.BeautifulSoup(res.text, "html.parser")
    # find p
    p=soup.find_all("p")
    # find text
    date=p[0].text.strip()
    text=p[1:-1]
    text=[t.text for t in text]
    text=" ".join(text)
    h2=soup.find("h2")
    subtitle=h2.text.strip()
    h1=soup.find("h1")
    title=h1.text.strip()
    return {
        "date":date,
        "text":text,
        "subtitle":subtitle,
        "title":title
    }

count=0
NewsData=[]
def conCurScrapNews(link):
    global count
    result=scrapNews(link)
    # append results to csv delimeter is ||
    NewsData.append(result)
    count+=1
    if count % 100 == 0:
        # save to json
        print("Count: {}".format(count))
        with open("NewsData.json", "w") as f:
            json.dump(NewsData, f)
    return result

with cf.ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(conCurScrapNews, dataLinks)
