
from preprocessing import tokenise,stopWords,stemmer
from collections import defaultdict

from search_two import ranking,findFileNumber,findFile_title,findFileList

import threading
import sys
import bz2
import re
import math
import timeit

offset=[]





def queryMultiplefield(queryWords, listOfFields,pathOfFolder,filealluniquevocabulary):                                         
    fileList=defaultdict(dict)
    df={}
    for i in range(len(queryWords)):
        
        word=queryWords[i]
        key=listOfFields[i]
        
        returnedList, mid= findFileNumber(0,len(offset),offset,"output",queryWords[0],filealluniquevocabulary)

        # print "queryMultifield ",returnedList

        print "searching for result"

        if len(returnedList)>0:
            
            fileNumber = returnedList[0]
            fileName= pathOfFolder+'_'+key+str(fileNumber)+'.bz2'
            fieldFile=bz2.BZ2File(fileName,'rb')

            returnedList, docfreq= findFileList(fileName,fileNumber,key,pathOfFolder,word,fieldFile)
           
            fileList[word][key] = returnedList

            df[word]=docfreq

        # print "#####df    ",df

    return fileList,df
            
    
def querySimple(queryWords, pathOfFolder, filealluniquevocabulary):                                                         
    fileList=defaultdict(dict)
    df={}
    listOfField=['t','b','i','c','e']
    for word in queryWords:
        
        returnedList, _= findFileNumber(0,len(offset),offset,"output",word,filealluniquevocabulary)
        
        if len( returnedList)>0:
            
            fileNumber = returnedList[0]
            
            df[word] = returnedList[1]

            for key in listOfField:
                
                fileName= pathOfFolder+'_'+key+str(fileNumber[0])+'.bz2'
                fieldFile=bz2.BZ2File(fileName,'rb')

                returnedList, _ = findFileList(fileName,fileNumber[0],key,pathOfFolder,word,fieldFile)
              
                fileList[word][key] = returnedList

    return fileList,df

def main():

    
    # if len(sys.argv)!= 2:                                             
    #     print "Usage :: python wikiIndexer.py pathOfFolder"
    #     sys.exit(0)
     
   
    with open("output"+'_offset.txt','rb') as f:
        for line in f:
            offset.append(int(line.strip()))
    

    print offset[:5]


    titleOffset=[]
    with open("output"+'_titleoffset.txt','rb') as f:
        for line in f:
            titleOffset.append(int(line.strip()))


    print titleOffset[:5]
    
    while True:

        print "search for......."

        query=raw_input()    

        start = timeit.default_timer()

        # print "query ",query[:2]
                                                                 
        flag=0
        
        filealluniquevocabulary = open("output"+'_vocabularyList.txt','r')
        
        if re.search(r'[t|b|c|e|i]:',query[:2]):
            
            # print "multiple query"

            flag=1

            queryWords=query.strip().split(' ')

            print "queryWords ",queryWords

            listOfFields=[]

            temp=[]

            for key in queryWords:
                listOfFields.append(key[:1])
                temp.append(key[2:])

            # print "listOfFields ",listOfFields
            
            # print "temp ",temp

            key=stopWords(temp)
            temp=stemmer(key)

            results, documentFrequency = queryMultiplefield(temp, listOfFields, "output",filealluniquevocabulary)
        else:

            print "simple query"

            print "searching for result"

            queryWords=tokenise(query)
            queryWords=stopWords(queryWords)
            queryWords=stemmer(queryWords)
            results, documentFrequency = querySimple(queryWords, "output",filealluniquevocabulary)
            
        f=open('output_numberOfFiles.txt','r')
        numberOfFiles=int(f.read().strip())
        f.close()

        results = ranking(results, documentFrequency,numberOfFiles)
        titleFile=open('output_title.txt','rb')
        dict_Title={}

        # dict_Title['1711']="Alcoholism"


        print "finding title"

        print ""

        for key in sorted(results.keys()):                                                                  
            
            title, _ = findFile_title(0,len(titleOffset),titleOffset,"title",key,"output_title.txt")

            # sprint "title",key,title

            dict_Title[key] = ' '.join(title)

            # dict_Title['1711']="Alcoholism"

            # print "dict_title ",key,dict_Title[key]
            # break




        # with open('output_title.txt','rb') as f:
        #     for line in f:
        #         temp=line.split(' ');
        #         dict_Title[temp[0]]=' '.join(temp[1:])



        stop = timeit.default_timer()

        print "time taken ",stop - start

        print ""


        if len(results)>0:
            results = sorted(results, key=results.get, reverse=True)

            if len(results)>10:
                results=results[:10]

            # print "result ",results[0]

            for key in results:
                print key,dict_Title[key]

            # print "last dict_Title",dict_Title
        else:
            print "Sorry not found Retry..."
            print ""
      
    
if __name__ == "__main__":                                            
    main()
    
   
