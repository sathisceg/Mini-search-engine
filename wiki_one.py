
import xml.sax.handler                                                  
from preprocessing import processText,processTitle
from writetofile_two import writetoIntermediateFile,mergeallIntermediateFiles
from collections import defaultdict
import sys
import timeit

index=defaultdict(list)
count = 0
countFile=0
dict_Id={}
offset = 0


class DataHandler(xml.sax.handler.ContentHandler):                     
  
  flag=0
  
  def createIndex(self, title, text, infoBox, category, externalLink):    

    global index
    global dict_Id
    global countFile
    global offset
    global count
    
    vocabularyList= list(set(title.keys()+text.keys()+infoBox.keys()+category.keys()+externalLink.keys()))
    t=float(len(title))
    # print t
    b=float(len(text))
    i=float(len(infoBox))
    c=float(len(category))
    e=float(len(externalLink))
    for key in vocabularyList:
      string= str(count)+' '
      try:
        string+=str(round(title[key]/t,4))+' '
      except ZeroDivisionError:
        string+='0.0 '
      try:
        string+=str(round(text[key]/b,4))+' '
      except ZeroDivisionError:
        string+='0.0 '
      try:
        string+=str(round(infoBox[key]/i,4))+' '
      except ZeroDivisionError:
        string+='0.0 '
      try:
        string+=str(round(category[key]/c,4))+' '
      except ZeroDivisionError:
        string+='0.0 '
      try:
        string+=str(round(externalLink[key]/e,4))
      except ZeroDivisionError:
        string+='0.0'
      index[key].append(string)       

    count+=1


    if count%5000==0:
      print count

      print "writetoIntermediateFile ",count

      offset = writetoIntermediateFile("output",index, dict_Id,countFile,offset)
      
      index=defaultdict(list)

      dict_Id={}
      
      countFile+=1


      
  def __init__(self):                                                           
    self.inTitle = 0
    self.inId=0
    self.inText=0
 
  def startElement(self, name, attributes):                           
    if name == "id" and DataHandler.flag==0:                          
      self.bufferId = ""
      self.inId = 1        
      DataHandler.flag=1
    elif name == "title":                                             
      self.bufferTitle = ""
      self.inTitle = 1
    elif name =="text":                                               
      self.bufferText = ""
      self.inText = 1
        
  def characters(self, data):                                        
   
    global count
    global dict_Id

    if self.inId and DataHandler.flag==1:                             
        
        self.bufferId += data
    
    elif self.inTitle:                                               
        
        self.bufferTitle += data
        
        dict_Id[count]=data.encode('utf-8')

        # title_file.write(data.encode('utf-8'))
        # print count

    elif self.inText:                                                 
        self.bufferText += data 
        
  def endElement(self, name):                                         
    
    if name == "title":   
                                                
      DataHandler.titleWords=processTitle(self.bufferTitle)          
      
      # title_file.write(DataHandler.titleWords)

      self.inTitle = 0
        
    elif name == "text":                                              
      DataHandler.textWords, DataHandler.infoBoxWords, DataHandler.categoryWords, DataHandler.externalLinkWords=processText(self.bufferText)              
      
      # with open('somefile.txt', 'a') as demo:
      #   demo.write(DataHandler.textWords+"\n")

      DataHandler.createIndex(self, DataHandler.titleWords, DataHandler.textWords, DataHandler.infoBoxWords, DataHandler.categoryWords, DataHandler.externalLinkWords)
      self.inText = 0
        
    elif name == "id":                                                
      self.inId = 0
        
    elif name == "page":                                              
      DataHandler.flag=0
    

def main():

    global offset
    global countFile

    # if len(sys.argv)!= 3:                                             
    #     print "Usage :: 
    #     sys.exit(0)
  
    parser = xml.sax.make_parser(  )                                  
    handler = DataHandler(  )
    parser.setContentHandler(handler)
    parser.parse("wiki_search_small.xml")



    with open("output_numberOfFiles.txt",'wb') as f:
      f.write(str(count))

    print "writetoIntermediateFile outside ",count
    
    offset = writetoIntermediateFile("output",index, dict_Id,countFile,offset)
    countFile+=1
    
    mergeallIntermediateFiles("output", countFile)

    titleOffset=[]

    # print(sys.argv[2])

    prevtitleOffset=0
    with open("output"+'_title.txt','rb') as f:
      # titleOffset.append('0')
      for line in f:
        titleOffset.append(str(prevtitleOffset))
        prevtitleOffset=prevtitleOffset+len(line)

    titleOffset.append(str(prevtitleOffset))



    with open("output"+'_titleoffset.txt','wb') as f:
      f.write('\n'.join(titleOffset))


    
if __name__ == "__main__":                                            
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    print stop - start
