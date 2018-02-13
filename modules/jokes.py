from bs4 import BeautifulSoup as BS
import requests,random

def get_jokes():
 jokeurl = 'http://www.santabanta.com/jokes/'
 res = requests.get(jokeurl)
 soup = BS(res.text,'html.parser')
 result = soup.find_all('td')
 # for joke in result:
 #     print (joke.text,'\n')

 return random.choice(result).text

