from urllib.request import urlopen
import urllib.request
import requests
from bs4 import BeautifulSoup
URL = "http://marumaru.in/?r=home&mod=search&keyword="+input("검색 : ")
#html = urlopen("http://marumaru.in/?r=home&mod=search&keyword=")

req = requests.get(URL)
html = req.text
searchData = BeautifulSoup(html,"html.parser")
selectedData = searchData.select("div.sbjbox > b")
mangaUrls = searchData.select("a.subject")

j = 0;
for i in selectedData:
    j+=1
    print(str(j)+". "+i.get_text())


URL = "http://marumaru.in"+mangaUrls[int(input("\n번호를 선택하여 주세요 : "))-1].get('href')
req = requests.get(URL)
html = req.text

fires = BeautifulSoup(html,"html.parser")
firesData = fires.find_all("a",{"target":"_blank"})

for i in firesData:
    print(i.get_text())

