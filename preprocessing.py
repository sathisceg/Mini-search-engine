
import re                                                          
from collections import defaultdict
# from porter2stemmer import Porter2Stemmer

# from stemming.porter2 import stem

from Stemmer import Stemmer


stopwords=defaultdict(int)                                          
with open('stopwords.txt','r') as f:
  for line in f:
    line= line.strip()
    stopwords[line]=1

def tokenise(data): 
  # return re.findall(\"[A-Z\\-\\.']{2,}(?![a-z])|[A-Z\\-\\'][a-z\\-\\']+(?=[A-Z])|[\\'\\w\\-.]+\",sentence) \n",                                                
  tokenisedWords=re.findall("\d+|[\w]+",data)
  tokenisedWords=[key.encode('utf-8') for key in tokenisedWords]
  return tokenisedWords

def stopWords(listOfWords):                                         
  temp=[key for key in listOfWords if stopwords[key]!=1]
  return temp

def stemmer(listofTokens):                                          

  stemmer = Stemmer("english");

  stemmedWords=[ stemmer.stemWord(key) for key in listofTokens ]
  return stemmedWords
  
def findExternalLinks(data):
  links=[]
  lines = data.split("==external links==")
  if len(lines)>1:
    lines=lines[1].split("\n")
    for i in xrange(len(lines)):
      if '* [' in lines[i] or '*[' in lines[i]:
        word=""
        temp=lines[i].split(' ')
        word=[key for key in temp if 'http' not in temp]
        word=' '.join(word).encode('utf-8')
        links.append(word)
  links=tokenise(' '.join(links))
  links = stopWords(links)
  links= stemmer(links)

  temp=defaultdict(int)
  for key in links:
    temp[key]+=1
  links=temp
  return links

def findInfoBoxTextCategory(data):                                        
  info=[]
  bodyText=[]
  category=[]
  links=[]
  flagtext=1
  lines = data.split('\n')
  for i in xrange(len(lines)):
    if '{{infobox' in lines[i]:
      flag=0
      temp=lines[i].split('{{infobox')[1:]
      info.extend(temp)
      while True:
            if(i>=len(lines)):
              break

            if '{{' in lines[i]:
                count=lines[i].count('{{')
                flag+=count
            if '}}' in lines[i]:
                count=lines[i].count('}}')
                flag-=count
            if flag<=0:
                break
            i+=1

            if(i>=len(lines)):
              break

            info.append(lines[i])
            
    elif flagtext:
      if '[[category' in lines[i] or '==external links==' in lines[i]:
        flagtext=0
      bodyText.append(lines[i])
            
    else:
      if "[[category" in lines[i]:
        line = data.split("[[category:")
        if len(line)>1:
            category.extend(line[1:-1])
            temp=line[-1].split(']]')
            category.append(temp[0])
  
  category=tokenise(' '.join(category))
  category = stopWords(category)
  category= stemmer(category)
           
  info=tokenise(' '.join(info))
  info = stopWords(info)
  info= stemmer(info)
  
  bodyText=tokenise(' '.join(bodyText))
  bodyText = stopWords(bodyText)
  bodyText= stemmer(bodyText)

  temp=defaultdict(int)
  for key in info:
    temp[key]+=1
  info=temp

  temp=defaultdict(int)
  for key in bodyText:
    temp[key]+=1
  bodyText=temp

  temp=defaultdict(int)
  for key in category:
    temp[key]+=1
  category=temp
  
  return info, bodyText, category
     
    
def processTitle(data):                                             
  data=data.lower()                                                 
  tokenisedTitle=tokenise(data)                                     
  stopWordsRemoved = stopWords(tokenisedTitle)                      
  stemmedWords= stemmer(stopWordsRemoved)                           
  temp=defaultdict(int)
  for key in stemmedWords:
    temp[key]+=1
  stemmedWords=temp
  return stemmedWords

def processText(data):                                              
  data = data.lower()                                               
  externalLinks = findExternalLinks(data)
  data = data.replace('_',' ').replace(',','')
  infoBox, bodyText, category = findInfoBoxTextCategory(data)                      
  return bodyText, infoBox, category, externalLinks
