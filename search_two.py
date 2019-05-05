
from collections import defaultdict
import math

def ranking(results, documentFreq, numberOfFiles):                                                      

    listOfDocuments=defaultdict(float)
    
    for key in documentFreq:
        documentFreq[key]= math.log((float(documentFreq[key])/float(numberOfFiles-1)))
        
    for word in results:
        
        fieldWisePostingList= results[word]
        
        for key in fieldWisePostingList:

            # print "key ",key

            if len(key)>0:
                # field=key
                postingList=fieldWisePostingList[key]
                if key=='t':
                    factor=0.3
                if key=='b':
                    factor=0.3
                if key=='i':
                    factor=0.2
                if key=='c':
                    factor=0.1
                if key=='e':
                    factor=0.1

                for i in range(0,len(postingList),2):
                    listOfDocuments[postingList[i]]+=(factor*float(postingList[i+1]))
                
    return listOfDocuments



def findFileNumber(low,high,offset,pathOfFolder,word,f): 

    # print " f ",f                                                   
    while low<high:
        mid=(low+high)/2

        f.seek(offset[mid])

        

        if pathOfFolder=="title":

            testWord = f.readline()
            # print "testWord ",testWord
            # print "testWord[0] ",testWord
            # if word==int(testWord[0]):
            #     # print "word found ",f
            #     return testWord[1:], mid  

            # elif word>int(testWord[0]):
            #     low=mid+1
            # else:
            #     high=mid-1

        else:    

            testWord = f.readline().strip().split(' ')        

            if word==testWord[0]:
                # print "word found ",f
                return testWord[1:], mid  

            elif word>testWord[0]:
                low=mid+1
            else:
                high=mid-1


    return [],-1


def findFile_title(low,high,offset,pathOfFolder,word,fan): 

    # print " f ",f      

    # print "word ",word

    with open('output_title.txt','rb') as f:
        while low<=high:
            # print "test1 ",f.readline().strip().split(' ')[0]

            mid=(low+high)/2

            # f.seek(offset[mid])

            # print "offest ", offset[mid]

            f.seek(offset[mid])

            # print "readline ",mid,f.readline().strip().split(' ')

            temp=f.readline().strip().split(' ')


            # print "temp ",temp

            if temp[0]=='':
                print temp,offset[mid]
                low+=1
                high-=1
                continue

            # print "check",word==temp[0]
            # if 0==int(temp):
            #     print "equal"
            # else:ow
            #     print "not equal"
            # break



            if int(word)==int(temp[0]):
                # print "word found ",f
                return temp[1:], mid  

            elif int(word)>int(temp[0]):
                low=mid+1
            else:
                high=mid-1


    return [],-1




def findFileList(fileName,fileNumber,field,pathOfFolder,word,fieldFile):                                    
    fieldOffset=[]
    tempdf= [] 

    offsetFileName=pathOfFolder+'_o'+field+fileNumber+'.txt'

    with open(offsetFileName,'rb') as fieldOffsetFile:
        
        for line in fieldOffsetFile:
            offset, docfreq = line.strip().split(' ')
            fieldOffset.append(int(offset))
            tempdf.append(int(docfreq))

    fileList, mid = findFileNumber(0,len(fieldOffset),fieldOffset,pathOfFolder,word,fieldFile)
    
    return fileList, tempdf[mid]