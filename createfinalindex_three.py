
import sys
import bz2
import heapq
import os
import operator
from collections import defaultdict
import threading


import time

class createFinalIndexforfield(threading.Thread):                                                             
    
    def __init__(self, field, data, offset, countFinalFile,pathOfFolder):
        threading.Thread.__init__(self)
        self.data=data
        self.field=field
        self.count=countFinalFile
        self.offset=offset
        self.pathOfFolder=pathOfFolder
        
    def run(self):
        filename= self.pathOfFolder+'_'+self.field+str(self.count)

        with bz2.BZ2File(filename+'.bz2', 'wb', compresslevel=7) as f:
            f.write('\n'.join(self.data))

        with open(filename+'.txt', 'wb') as f:
            f.write('\n'.join(self.data))

        filename= self.pathOfFolder+'_o'+self.field+str(self.count)+'.txt'

        with open(filename, 'wb') as f:
            f.write('\n'.join(self.offset))
    
def createFinalIndex(data, countFinalFile, pathOfFolder,offsetSize):                   
    
    title=defaultdict(dict)
    text=defaultdict(dict)
    info=defaultdict(dict)
    category=defaultdict(dict)
    externalLink=defaultdict(dict)
    
    uniqueWords=[]
    offset=[]

    check=0

    for key in sorted(data.keys()):
        
        listOfDoc=data[key]

        temp=[]
        flag=0
        
        for i in range(0,len(listOfDoc),6):
           word=listOfDoc
           docid=word[i]
           if word[i+1]!='0.0':
               title[key][docid]=float(word[i+1])
               flag=1
           if word[i+2]!='0.0':
               text[key][docid]=float(word[i+2])
               flag=1
           if word[i+3]!='0.0':
               info[key][docid]=float(word[i+3])
               flag=1
           if word[i+4]!='0.0':
               category[key][docid]=float(word[i+4])
               flag=1
           if word[i+5]!='0.0':
               externalLink[key][docid]=float(word[i+5])
               flag=1

        if flag==1:

            if (len(listOfDoc)/6)>=20:
                print "length _vocabularyList",(len(listOfDoc)/6)
                check+=1

            string = key+' '+str(countFinalFile)+' '+str(len(listOfDoc)/6)
            uniqueWords.append(string)
            offset.append(str(offsetSize))
            offsetSize=offsetSize+len(string)+1
    

    titleData=[]
    textData=[]
    infoData=[]
    categoryData=[]
    externalLinkData=[]

    titleOffset=[]
    textOffset=[]
    infoOffset=[]
    categoryOffset=[]
    externalLinkOffset=[]

    previousTitle=0
    previousText=0
    previousInfo=0
    previousCategory=0
    previousExternalLink=0


    print "check value ",check
    # time.sleep(5)

    for key in sorted(data.keys()):                                                                     
        #print key
        if key in title:
            string=key+' '
            sortedField=title[key]

            sortedField = sorted(sortedField, key = sortedField.get, reverse=True)

            if(len(sortedField)>20):
                sortedField=sortedField[:20]
            
            i=0
            for doc in sortedField:
                string+=doc+' '+str(title[key][doc])+' '
                i+=1
                if i==20:
                    break

            titleOffset.append(str(previousTitle)+' '+str(len(sortedField)))
            previousTitle = len(string)+1
            titleData.append(string)

        if key in text:
            string=key+' '
            sortedField=text[key]
            sortedField = sorted(sortedField, key = sortedField.get, reverse=True)


            if(len(sortedField)>20):
                sortedField=sortedField[:20]

            i=0
            for doc in sortedField:
                string+=doc+' '+str(text[key][doc])+' '
                i+=1
                if i==20:
                    break


            textOffset.append(str(previousText)+' '+str(len(sortedField)))
            previousText+=len(string)+1
            textData.append(string)       

        if key in info:
            string=''
            string+=key+' '
            sortedField=info[key]
            sortedField = sorted(sortedField, key = sortedField.get, reverse=True)

            # print "info sortedField length before ",len(sortedField)

            # time.sleep(.300)

            # print "info sortedField all befor",sortedField

            if(len(sortedField)>20):
                sortedField=sortedField[:20]
                # print "####info sortedField length after",len(sortedField)

                # print "info sortedField all after",sortedField
                # time.sleep(5)

            
            i=0
            for doc in sortedField:
                string+=doc+' '+str(info[key][doc])+' '
                i+=1
                if i==20:
                    break
            

            infoOffset.append(str(previousInfo)+' '+str(len(sortedField)))
            previousInfo+=len(string)+1            
            infoData.append(string)

        if key in category:
            string=key+' '
            sortedField=category[key]
            sortedField = sorted(sortedField, key = sortedField.get, reverse=True)


            if(len(sortedField)>20):
                sortedField=sortedField[:20]

            i=0
            for doc in sortedField:
                string+=(doc+' '+str(category[key][doc])+' ')
                i+=1
                if i==20:
                    break

            categoryOffset.append(str(previousCategory)+' '+str(len(sortedField)))
            previousCategory+=len(string)+1
            categoryData.append(string)

        if key in externalLink:
            string= key+' '
            sortedField=externalLink[key]
            sortedField = sorted(sortedField, key = sortedField.get, reverse=True)

            if(len(sortedField)>20):
                sortedField=sortedField[:20]

            i=0
            for doc in sortedField:
                string+=doc+' '+str(externalLink[key][doc])+' '
                i+=1
                if i==20:
                    break

            externalLinkOffset.append(str(previousExternalLink)+' '+str(len(sortedField)))
            previousExternalLink+=len(string)+1
            externalLinkData.append(string)

    try:
        if os.path.getsize(pathOfFolder+'_b'+str(countFinalFile)+'.bz2') > 10485760:
            countFinalFile+=1
    except:
        pass

    thread1 = createFinalIndexforfield('t', titleData, titleOffset, countFinalFile,pathOfFolder)
    thread2 = createFinalIndexforfield('b', textData, textOffset, countFinalFile,pathOfFolder)
    thread3 = createFinalIndexforfield('i', infoData, infoOffset, countFinalFile,pathOfFolder)
    thread4 = createFinalIndexforfield('c', categoryData, categoryOffset, countFinalFile,pathOfFolder)
    thread5 = createFinalIndexforfield('e', externalLinkData, externalLinkOffset, countFinalFile,pathOfFolder)

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()
     
    with open(pathOfFolder+"_vocabularyList.txt","ab") as f:
      f.write('\n'.join(uniqueWords))
      
    with open(pathOfFolder+"_offset.txt","ab") as f:
      f.write('\n'.join(offset))
      
    return countFinalFile, offsetSize
 