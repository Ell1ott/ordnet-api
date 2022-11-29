import requests
from bs4 import BeautifulSoup
import json

baseUrl = "https://ordnet.dk/ddo/ordbog?query="
url = "https://ordnet.dk/ddo/ordbog?query=kat"

def getSoup(url):

    response = requests.request("GET", url)

    # print(response.text)
    # print(response.status_code)
    # print(response.content)
    return BeautifulSoup(response.content, 'html.parser')
    
s = getSoup(url)

def splitSuper(e, d = False):
    try:
        ord = e.getText(strip=True)
        ordversion = e.select_one(".super").getText(strip=True)
        ord = ord.replace(ordversion, '')
        if(d):
            return {"ord": ord,
                    "ordversion": ordversion}
        return ord, ordversion
    except:
        return {"ord": e.getText(strip=True), "ordversion": 0}
def getWordInfo(w = None, s = None, url = None):
    if w != None:
        s = getSoup(baseUrl + w)
    
    elif url != None:
        s = getSoup(url)
    
    d = {}
    artikel = s.find("div", {"class": "artikel"})
    #portal-column-two #opslagsordBox_expanded .searchResultBox a
    boxtop = artikel.find("div", {"class": "definitionBoxTop"}).findAll("span", recursive=False)[1].getText().split(', ')
    d["ord"], d["ordversion"] = splitSuper(artikel.select_one('.definitionBoxTop .match'))
    d["ordklasse"] = boxtop[0]
    if len(boxtop) > 1:
        d["køn"] = boxtop[1]
    else:
        d["køn"] = "unknown"
    
    belem = artikel.select("#id-boj span")
    if(len(belem) > 1):
        d["bøjning"] = artikel.select("#id-boj span")[1].getText().split(', ')
    else:
        d["bøjning"] = []
    
    d["udtale"] = artikel.find("div", { "id" : "id-udt" }).findAll("span")[1].findAll("span")[0].getText(strip=True)
    
    betydningerElem = artikel.find("div", {"id": "content-betydninger"})
    
    betydninger = []
    
    betydning = {}
    betydningElem = betydningerElem.find("div", {"class": "definitionIndent"})
    
    betydning["definition"] = betydningElem.select_one('.definition').getText(strip=True)
    if betydningElem.select_one('.onym'):
        betydning["synonymer"]  = [a.getText(strip=True) for a in betydningElem.select_one('.onym').findAll("a")]
    else:
        betydning["synonymer"]  = None
    
    betydninger.append(betydning)
    
    d["betydninger"] = betydninger    
    print(len(s.select("#portal-column-two #opslagsordBox_expanded .searchResultBox a")))
    d["lignendeOrd"] = [splitSuper(a, True) for a in s.select("#portal-column-two #opslagsordBox_expanded .searchResultBox a")]
    return d

def alleBøjninger(d):
    return [d['ord'] + a.replace('-', '') for a in d['bøjning']]

def prettyPrint(dict):
    print(json.dumps(dict, indent=4, ensure_ascii=False))

def calcString(string):
    for word in string.split(' '):
        prettyPrint(getWordInfo(word))
        
# word = getWordInfo(url=url)
# print(json.dumps(word, indent=4, ensure_ascii=False))

calcString(input("sentence: "))

# print(s.find("div", { "id" : "id-boj" }).findAll("span")[1].getText().split(', '))