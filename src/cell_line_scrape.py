from bs4 import BeautifulSoup
import requests
import time

# class cellLine:

    # def __init__(self, name, organism, tissue, cell_type, disease):
        # self.name = name
        # self.organism = organism
        # self.tissue = tissue
        # self.cell_type = cell_type
        # self.disease = disease
    
    # def __repr__():
    # # print name, organism, tissue, cell_type, disease
        # name = self.name
        # strings = name + ', '+ self.organism + ', '+ self.tissue + ', '+ self.cell_type + ', '+ self.disease
        # return strings
        
    
#@classmethod  




#Urls will contain a list of the urls for pages 1-121
urls = ['http://www.atcc.org/Products/Cells_and_Microorganisms/Cell_Lines/Human/Alphanumeric.aspx']

def get_soup(url):
    # NOTE: adding 'html.parser' as second argument avoids warning and possible errors
    # related to not explicitly specifying the parser
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    return soup
    
def from_soup(soup, myCellsList):
    cellsList = soup.find_all('li', {'class' : 'product clearfix'}) #finding all cell html into a list
    
    for i in range (len(cellsList)): #iterating through each cell entry html
        ottdDict = {} 
        ottdDict['Name'] = cellsList[i].h3.text.strip() #gets the generic name and ATCC name into the format '10.014 pRSV-T  <ATCCr CRL-11515T> or '143B  (ATCCr CRL-8303T)
        genName = ottdDict['Name'].split('(')[0].strip()
        ATCCName = ottdDict['Name'].split('(')[1]
        ATCCName = ATCCName.split('CRL-')
        ATCCName = ATCCName[1].replace(')','')
        ATCCList = list(ATCCName)
        ATCCList.pop()
        ATCCName = (''.join(ATCCList))
        ATCCName = 'CRL-' + ATCCName
        ottdDict['GenName'] = genName
        ottdDict ['ATCCName'] = ATCCName
        #ottd stands for organ, type, tissue, disease
        
        ottd = cellsList[i].find_all('strong') #grabs values that are present out of org, type, tiss, and dis
        
        k = 1
        ottdList = []
        while k < len(ottd):
            ottdList.append (ottd[k].get_text())
            k += 1
        #ottdList result is in the format['Organism:', 'Cell Type:', 'Tissue:', 'Disease:']    
        
        for l in range(len(ottdList)): #strips the ottdList elements of the colon
            ottdList[l] = ottdList[l].strip(':')#result for ottdList is in the format ['Organism', 'Cell Type', 'Tissue', 'Disease']
         
        abcdList = []     
        abcd = cellsList[i].find_all('em') #grabs values for org, type, tiss, and disease
        
        for item in abcd:
            abcdList.append(item.text.strip()) #result is in the format {'Homo sapiens, human', 'Bone, 'Osteosarcoma'}
 
        
        #start adding to ottdDict 
        
        if len(ottdList) == 4: #all attributes present (ottd)
            ottdDict['Organism'] = abcdList[0]
            ottdDict['Cell Type'] = abcdList[1]
            ottdDict['Tissue'] = abcdList[2]
            ottdDict['Disease'] = abcdList[3]
            
        elif len(ottdList) == 1: #only organism is present
            ottdDict['Organism'] = abcdList[0]
            ottdDict['Cell Type'] = 'N/A'
            ottdDict['Tissue'] = 'N/A'
            ottdDict['Disease'] = 'N/A'
            
        #3 attributes present (-Disease)    
        elif len(ottdList) == 3:

            if 'Organism' in ottdList and 'Cell Type' in ottdList and 'Tissue' in ottdList: 
                ottdDict['Organism'] = abcdList[0]
                ottdDict['Cell Type'] = abcdList[1]
                ottdDict['Tissue'] = abcdList[2]
                ottdDict['Disease'] = 'N/A'
            
        #3 attributes present (-Tissue)    
            
            elif 'Organism' in ottdList and 'Cell Type' in ottdList and 'Disease' in ottdList: 
                ottdDict['Organism'] = abcdList[0]
                ottdDict['Cell Type'] = abcdList[1]
                ottdDict['Disease'] = abcdList[2]   
                ottdDict['Tissue'] = 'N/A'    
            
        #3 attributes present (-Type)    
            
            elif 'Organism' in ottdList and 'Tissue' in ottdList and 'Disease' in ottdList:
                ottdDict['Organism'] = abcdList[0]
                ottdDict['Tissue'] = abcdList[1]
                ottdDict['Disease'] = abcdList[2]   
                ottdDict['Cell Type'] = 'N/A'        
            
        #2 attributes present (Org and Type)    

        elif len(ottdList) == 2:    
            if 'Organism' in ottdList and 'Cell Type' in ottdList: 
                ottdDict['Organism'] = abcdList[0]
                ottdDict['Cell Type'] = abcdList[1]
                ottdDict['Tissue'] = 'N/A'
                ottdDict['Disease'] = 'N/A'
            
        #2 attributes present (Org and Tissue)    
            
            elif 'Organism' in ottdList and 'Tissue' in ottdList: 
                ottdDict['Organism'] = abcdList[0]
                ottdDict['Cell Type'] = 'N/A'
                ottdDict['Disease'] = 'N/A'   
                ottdDict['Tissue'] = abcdList[1]    
            
        #2 attributes present (Org and Disease)    
            
            elif 'Organism' in ottdList and'Disease' in ottdList:
                ottdDict['Organism'] = abcdList[0]
                ottdDict['Tissue'] = 'N/A'
                ottdDict['Disease'] = abcdList[1]   
                ottdDict['Cell Type'] = 'N/A'

        elif len(ottdList) == 0:
            ottdDict['Organism'] = 'N/A'
            ottdDict['Tissue'] = 'N/A'
            ottdDict['Disease'] = 'N/A'   
            ottdDict['Cell Type'] = 'N/A'    
   
        myCellsList.append(ottdDict)  
    
    
    return myCellsList    
    
#def getATCCName (lst):
def print_cell(srchblCL, celValStr, page = 1): #remove page default?
    celValList = [int(e) for e in celValStr.split()]
    str1 = ', '.join(str(e) for e in celValList)
    print()
    print ()
    print ((' Results for search of ' + str1 +' on page ' + str(page) + ' ').center(80, '*'))
    print ()

    
    for item in celValList:
        print (('').center(80, '*'))
        print ('Generic Name: ' + srchblCL[item-1]['GenName'])
        print ('ATCC Name: ' + srchblCL[item-1]['ATCCName'])
        print ('Organism: ' + srchblCL[item-1]['Organism'])
        print ('Cell Type: ' + srchblCL[item-1]['Cell Type'])
        print ('Tissue: ' + srchblCL[item-1]['Tissue'])
        print ('Disease: ' + srchblCL[item-1]['Disease'])
        print ()
        print ()
    
def main():
    print ()
    print ()
    print ((time.strftime('%A, %m/%d/%Y, at %I:%M')).center(80, '*'))
    # Allow for all pages to be printed with the header 
    #for i in len(urls)
    #string = 'Page ' + str(i+1) 
    #print (string.center(80, '*'))
    print ()
    print (('Page 1').center(80,'*')) #will be replaced when scraping all pages
    #go through urls for pages 1-121
    gotSoup = get_soup(urls[0])
    lst = []
    from_soup (gotSoup, lst)
    
    # soup = BeautifulSoup(data)
    # for sup in soup.find_all('sup'):
        # sup.unwrap()

    #print soup.prettify()
    
    for i in range (len(lst)): #main page 
        genName = lst[i]['Name'].split('(')[0].strip()
        ATCCName = lst[i]['Name'].split('(')[1]
        ATCCName = ATCCName.split('CRL-')
        ATCCName = ATCCName[1].replace(')','')
        ATCCList = list(ATCCName)
        ATCCList.pop()
        ATCCName = (''.join(ATCCList))
        ATCCName = (''.join(ATCCList))
        ATCCName = ' (ATCC CRL-' + ATCCName + ')'
        print (str(i+1) + ': ' + genName + ATCCName)
    
    #exceptions
    
    #elif ask1 == 'n': #execute for next page
        # print ('Best')
    #elif ask1 #execute to enter page numbers
    
    
 
    go = True
    
    
    while go:
        print ()
        print ()
        ask1 = input ("Enter numbers separated by spaces, press enter to select all, or type 'esc' to exit: ") #Numbers separated as spaces look like '1 2 3' #, enter 'n' for next page, or return to select all: 
    
        #used to determine if input is string with integer values
        invalid = False
        intStr = ask1.replace(' ', '') #format '15910'
    
        if ',' in ask1:
            print ('Invalid Entry: ' + ask1)
            go = True
            
        elif ask1: #what to do if value is entered     
            if ask1 == 'esc':
                go = False
                break
                
            #elif intStr == 'n'
            
            elif not intStr.isdigit():    
                print ('Invalid Entry: ' + ask1)
                go = True
                
            else: #if string contains integers we search for value 
                checkVals = [int(e) for e in ask1.split()]
                for i in range(len(checkVals)):
                    if checkVals[i] > len(lst) or checkVals[i] < 0:
                        print ('Invalid Entry: ' + str(checkVals[i]))
                        go = True
                        invalid = True
                        
                while not invalid:
                    print_cell (lst, ask1)
                    print()
                    ask2 = input ("Press enter to return to page 1 or type 'esc' to quit: ") #needs to be edited for additional pages
                    print ()
                    if not ask2: #if returning to page 1
                        #print()
                        str1 = ', '.join(str(e) for e in intStr)
                        print ()
                        print ((time.strftime('%A, %m/%d/%Y, at %I:%M')).center(80, '*'))
                        # Allow for all pages to be printed with the header 
                        #for i in len(urls)
                        #string = 'Page ' + str(i+1) 
                        #print (string.center(80, '*'))
                        print ()
                        print (('Page 1').center(80,'*'))
                        for i in range (len(lst)):
                            genName = lst[i]['Name'].split('(')[0].strip()
                            ATCCName = lst[i]['Name'].split('(')[1]
                            ATCCName = ATCCName.split('CRL-')
                            ATCCName = ATCCName[1].replace(')','')
                            ATCCList = list(ATCCName)
                            ATCCList.pop()
                            ATCCName = (''.join(ATCCList))
                            ATCCName = ' (ATCC CRL-' + ATCCName + ')'
                            print (str(i+1) + ': ' + genName + ATCCName)
                        go = True
                        break
                    elif ask2 == 'esc':
                        go = False
                        break
                    
                    else:
                        print ('Invalid Entry: ' + ask2)
                        print ('Goodbye')
                        go = False
                        break  
        
        elif not ask1: #executed for select all
            print_cell(lst, ' '.join([str(e+1) for e in list(range(10))]))
            #ask1 = 
            print ()
            ask2 = input ("Press enter to return to page 1 or type 'esc' to quit: ") #needs to be edited for additional pages
            print ()
            if not ask2:
                #print()
                print ()
                print ((time.strftime('%A, %m/%d/%Y, at %I:%M')).center(80, '*'))
                # Allow for all pages to be printed with the header 
                #for i in len(urls)
                #string = 'Page ' + str(i+1) 
                #print (string.center(80, '*'))
                print ()
                print (('Page 1').center(80,'*'))
                for i in range (len(lst)):
                    genName = lst[i]['Name'].split('(')[0].strip()
                    ATCCName = lst[i]['Name'].split('(')[1]
                    ATCCName = ATCCName.split('CRL-')
                    ATCCName = ATCCName[1].replace(')','')
                    ATCCList = list(ATCCName)
                    ATCCList.pop()
                    ATCCName = (''.join(ATCCList))
                    ATCCName = ' (ATCC CRL-' + ATCCName + ')'
                    print (str(i+1) + ': ' + genName + ATCCName)
                go = True
                
            elif ask2 == 'esc':
                go = False
                break
            else: 
                print ('Invalid Entry: ' + ask2)
                print ('Goodbye')
                go = False
                break
        else: 
            print ('Invalid Entry: ' + ask1)
            go = True
            
            
    
    
    
    
if __name__ == '__main__':
    main()

