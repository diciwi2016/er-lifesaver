#! /usr/bin/python
#print "Content-type: text/html\n\n"
import urllib2, json, urllib
from bs4 import BeautifulSoup, SoupStrainer
#from cookielib import CookieJar


def showContent(urlz):
      html = urllib2.build_opener(urllib2.HTTPCookieProcessor).open(urlz)

      soup = BeautifulSoup(html, "html.parser")
      #texts=soup.findAll(text=True)
      # kill all script and style elements

      for script in soup(["script", "style"]):
          script.extract()    # rip it out
      # get text
      
      text = soup.get_text()
      # break into lines and remove leading and trailing space on each

      lines = (line.strip() for line in text.splitlines())
      # break multi-headlines into a line each

      chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
      # drop blank lines

      text = '\n'.join(chunk for chunk in chunks if chunk)
      #print(soup.get_text("|", strip=True))

      #tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
      #return '\n-----\n'.join(tokenizer.tokenize(text))
      return text

##the extracted hospital data of average waiting times
info= showContent("https://projects.propublica.org/emergency/state/NY")
info= info[1835:20207].split("\n")

hd={}
for i in info[:]:
    
    if len(i)>3 and i!="Broken Bone" and i!="Time Until Sent Home" and i!="'Waiting Time'" and i!="of port jefferson":
        hd[i]=str(info[info.index(i)+2])
        if info.index(i)>len(info):
            break
        
#print hd
