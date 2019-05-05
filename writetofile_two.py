import sys
import bz2
import heapq
import os
import operator
from collections import defaultdict
from createfinalindex_three import createFinalIndex
import threading





def writetoIntermediateFile(pathOfFolder, index, dict_Id, countFile, titleOffset):                                        
    data=[]                                                                            
    previousTitleOffset=titleOffset

    for key in index:
        string= str(key)+' '
        temp=index[key]
        string+=' '.join(temp)
        data.append(string)


    filename=pathOfFolder+'_index_'+str(countFile)+'.txt.bz2'                            
    

    with bz2.BZ2File(filename, 'wb', compresslevel=9) as f:
        f.write('\n'.join(data))
     


    data=[]

    for key in dict_Id:
        data.append(str(key)+' '+dict_Id[key])
       
        
    filename=pathOfFolder+'_title.txt'

    with open(filename,'ab') as f:
        f.write('\n'.join(data))


    return  previousTitleOffset






def mergeallIntermediateFiles(pathOfFolder, countFile):                                                 
    listOfWords={}
    indexFile={}
    topOfFile={}

    print "countFile ",countFile

    flag=[0]*countFile
    data=defaultdict(list)
    heap=[]
    countFinalFile=0
    offsetSize = 0
    for i in xrange(countFile):
        fileName = pathOfFolder+'_index_'+str(i)+'.txt.bz2'
        
        indexFile[i]= bz2.BZ2File(fileName, 'rb')
        flag[i]=1
        
        topOfFile[i]=indexFile[i].readline().strip()
        listOfWords[i] = topOfFile[i].split(' ')
        
        if listOfWords[i][0] not in heap:
            heapq.heappush(heap, listOfWords[i][0])        

    count=0        
    while any(flag)==1:
        
        temp = heapq.heappop(heap)
        count+=1

        # if count==1000001:
        # 	break

        for i in xrange(countFile):
            if flag[i]:
                if listOfWords[i][0]==temp:
                    data[temp].extend(listOfWords[i][1:])

                    if count==1000000:
                        
                        oldCountFile=countFinalFile
                       
                        countFinalFile, offsetSize = createFinalIndex(data, countFinalFile, pathOfFolder, offsetSize)                        
                        
                        if oldCountFile!=  countFinalFile:
                            data=defaultdict(list)
                        
                    topOfFile[i]=indexFile[i].readline().strip()   
                    
                    if topOfFile[i]=='':
                            flag[i]=0
                            indexFile[i].close()
                            os.remove(pathOfFolder+'_index_'+str(i)+'.txt.bz2')
                    else:
                        listOfWords[i] = topOfFile[i].split(' ')
                        if listOfWords[i][0] not in heap:
                            heapq.heappush(heap, listOfWords[i][0])
                            
    countFinalFile, offsetSize = createFinalIndex(data, countFinalFile, pathOfFolder, offsetSize)
   








     
  




