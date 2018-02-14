from bs4 import BeautifulSoup as BS
import requests,random

def get_quotes():
    quotesurl="https://www.brainyquote.com/top_100_quotes"
    res=requests.get(quotesurl)
    soup=BS(res.text,"html.parser")
    result=soup.find_all('span',{'class':'block-quote'})
    return random.choice(result).text